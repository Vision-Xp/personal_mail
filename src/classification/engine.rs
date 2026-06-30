use anyhow::{Context, Result};
use reqwest::blocking::Client;
use serde::Deserialize;
use std::fs;

use crate::classification::scoring::ClassificationConfig;

#[derive(Debug, Deserialize, Clone)]
pub struct MessageMeta {
    pub id: String,
    pub subject: Option<String>,
    pub from: Option<String>,
    pub snippet: Option<String>,
}

#[derive(Debug, Deserialize)]
struct GmailMessage {
    id: String,
    payload: Option<Payload>,
    snippet: Option<String>,
}

#[derive(Debug, Deserialize, Clone)]
struct Payload {
    headers: Vec<Header>,
}

#[derive(Debug, Deserialize, Clone)]
struct Header {
    name: String,
    value: String,
}

impl MessageMeta {
    pub fn from_gmail(msg: GmailMessage) -> Self {
        let mut subject = None;
        let mut from = None;
        if let Some(payload) = &msg.payload {
            for h in &payload.headers {
                match h.name.as_str() {
                    "Subject" => subject = Some(h.value.clone()),
                    "From" => from = Some(h.value.clone()),
                    _ => {}
                }
            }
        }
        Self {
            id: msg.id,
            subject,
            from,
            snippet: msg.snippet,
        }
    }
}

pub fn load_token(path: &str) -> Result<String> {
    let data = fs::read_to_string(path)
        .with_context(|| format!("missing token at {}", path))?;
    let token: serde_json::Value = serde_json::from_str(&data)
        .with_context(|| "invalid token json")?;
    let access_token = token["access_token"]
        .as_str()
        .context("no access_token in token file")?;
    Ok(access_token.to_string())
}

pub fn fetch_recent_messages(access_token: &str, limit: usize) -> Result<Vec<MessageMeta>> {
    let url = format!(
        "https://gmail.googleapis.com/gmail/v1/users/me/messages?maxResults={}",
        limit
    );
    let client = Client::new();
    let resp = client.get(&url).bearer_auth(access_token).send()?;
    let response: serde_json::Value = match resp.json() {
        Ok(v) => v,
        Err(e) => {
            if let Ok(text) = resp.text() {
                eprintln!("gmail list decode error: {}\nbody: {}", e, text);
            } else {
                eprintln!("gmail list decode error: {}", e);
            }
            anyhow::bail!("gmail list decode error");
        }
    };

    let messages = response["messages"]
        .as_array()
        .context("expected messages array")?
        .iter()
        .filter_map(|m| m["id"].as_str().map(|s| s.to_string()))
        .collect::<Vec<_>>();

    let mut out = Vec::new();
    for id in messages {
        let msg_url = format!(
            "https://gmail.googleapis.com/gmail/v1/users/me/messages/{}?format=metadata",
            id
        );
        let raw: GmailMessage = client.get(&msg_url).bearer_auth(access_token).send()?.json()?;
        out.push(MessageMeta::from_gmail(raw));
    }

    Ok(out)
}
