use anyhow::Context;
use clap::Parser;
use serde::Deserialize;
use std::fs;
use std::path::PathBuf;

use crate::classification::{engine, scoring};

const TOKEN_PATH: &str =
    r"C:\Users\SMAD Inc\AppData\Local\personal_mail\google_oauth\token.json";

#[derive(Debug, Parser)]
#[command(name = "personal_mail-test-recent", about = "Classify recent messages for review")]
struct Cli {
    /// Path to config file
    #[arg(long, default_value = "config/personal_mail.local.yaml")]
    config: PathBuf,
    /// Number of recent messages to inspect
    #[arg(long, default_value_t = 5)]
    limit: usize,
}

fn load_cfg(path: &PathBuf) -> anyhow::Result<scoring::ClassificationConfig> {
    let content = fs::read_to_string(path)
        .with_context(|| format!("failed to read config: {}", path.display()))?;
    let cfg: Config = serde_yaml::from_str(&content)
        .with_context(|| format!("failed to parse config: {}", path.display()))?;
    Ok(cfg.classification)
}

#[derive(Debug, Deserialize)]
struct Config {
    #[serde(default)]
    classification: scoring::ClassificationConfig,
}

fn main() -> anyhow::Result<()> {
    let cli = Cli::parse();
    let class_cfg = load_cfg(&cli.config)?;

    let data = fs::read_to_string(TOKEN_PATH)
        .with_context(|| format!("missing token at {TOKEN_PATH}"))?;
    let token: serde_json::Value = serde_json::from_str(&data)
        .with_context(|| "invalid token json")?;
    let access_token = token["access_token"]
        .as_str()
        .context("no access_token in token file")?;

    let messages = engine::fetch_recent_messages(access_token, cli.limit)?;

    println!("CLASSIFICATION_REVIEW n={}", messages.len());
    for msg in &messages {
        let subject = msg.subject.as_deref().unwrap_or("<no subject>");
        let from = msg.from.as_deref().unwrap_or("<unknown>");
        let snippet = msg.snippet.as_deref().unwrap_or("");

        let mut text_parts: Vec<String> = Vec::new();
        text_parts.push(subject.to_string());
        text_parts.push(from.to_string());
        text_parts.push(snippet.to_string());
        let text = text_parts.join(" ");
        let signals: Vec<String> = text.split_whitespace().map(|t| t.to_lowercase()).collect();

        let proposed: Option<String>;
        let confidence: u8;
        if let Some((rule, conf)) = class_cfg.best_category(&signals) {
            proposed = rule.label.clone();
            confidence = conf;
        } else {
            proposed = class_cfg.default_label.clone();
            confidence = 0;
        }

        let proposed = proposed.unwrap_or_else(|| "<none>".to_string());
        if proposed == "<none>" || confidence < 50 {
            continue;
        }

        println!(
            "MESSAGE id={} subject={} from={} snippet={} proposed={} confidence={}",
            msg.id, subject, from, snippet, proposed, confidence
        );
    }

    Ok(())
}
