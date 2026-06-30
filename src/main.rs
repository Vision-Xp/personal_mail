use anyhow::{Context, Result};
use clap::{Parser, ValueEnum};
use serde::Deserialize;
use std::fs;
use std::path::PathBuf;

const TOKEN_PATH: &str =
    r"C:\Users\SMAD Inc\AppData\Local\personal_mail\google_oauth\token.json";

#[derive(Debug, Parser)]
#[command(
    name = "personal_mail",
    version,
    about = "Personal Mail CLI - dry-run first, apply later.",
    propagate_version = true
)]
struct Cli {
    /// Path to config file
    #[arg(long, default_value = "config/personal_mail.local.yaml")]
    config: PathBuf,

    /// Run mode
    #[arg(long, value_enum)]
    mode: Option<Mode>,

    /// List Gmail labels
    #[arg(long)]
    labels_list: bool,

    /// Show account info
    #[arg(long)]
    whoami: bool,
}

#[derive(Debug, Clone, Copy, ValueEnum)]
enum Mode {
    DryRun,
    SafeRun,
    ApplyRun,
    AuditRun,
}

impl std::fmt::Display for Mode {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Mode::DryRun => write!(f, "dry-run"),
            Mode::SafeRun => write!(f, "safe-run"),
            Mode::ApplyRun => write!(f, "apply-run"),
            Mode::AuditRun => write!(f, "audit-run"),
        }
    }
}

#[derive(Debug, Deserialize)]
struct Config {
    accounts: Vec<Account>,
    modes: Modes,
    logging: Logging,
}

#[derive(Debug, Deserialize)]
struct Account {
    #[serde(rename = "account_id")]
    account_id: String,
    #[serde(rename = "gmail_email")]
    gmail_email: String,
    enabled: bool,
}

#[derive(Debug, Deserialize)]
struct Modes {
    #[serde(default = "default_default_mode")]
    default_mode: String,
    #[serde(default)]
    allow_modes: Vec<String>,
}

fn default_default_mode() -> String {
    "dry-run".into()
}

#[derive(Debug, Deserialize, Default)]
struct Logging {
    directory: Option<String>,
    filename: Option<String>,
    max_bytes: Option<u64>,
    max_files: Option<usize>,
    format: Option<String>,
}

fn load_config(path: &PathBuf) -> Result<Config> {
    let content = fs::read_to_string(path)
        .with_context(|| format!("failed to read config: {}", path.display()))?;
    let cfg: Config = serde_yaml::from_str(&content)
        .with_context(|| format!("failed to parse config: {}", path.display()))?;
    Ok(cfg)
}

fn default_config() -> Config {
    Config {
        accounts: vec![],
        modes: Modes {
            default_mode: default_default_mode(),
            allow_modes: vec![],
        },
        logging: Logging::default(),
    }
}

fn run_skeleton(cli: &Cli, cfg: Config) -> Result<()> {
    let mode = match cli.mode.unwrap_or_else(|| {
        Mode::from_str(&cfg.modes.default_mode, true).unwrap_or(Mode::DryRun)
    }) {
        Mode::DryRun => "dry-run",
        Mode::SafeRun => "safe-run",
        Mode::ApplyRun => "apply-run",
        Mode::AuditRun => "audit-run",
    };

    println!("STATUS=phase3_gmail_proof");
    println!("CONFIG={}", cli.config.display());
    println!("MODE={}", mode);
    println!("ACCOUNTS={}", cfg.accounts.len());
    if let Some(account) = cfg.accounts.first() {
        println!("ACCOUNT_ID={}", account.account_id);
        println!("GMAIL_EMAIL={}", account.gmail_email);
    }

    if mode != "dry-run" {
        anyhow::bail!("only dry-run is allowed in Phase 3 proof");
    }

    println!("DRY_RUN_COMPLETE");
    Ok(())
}

fn labels_list() -> Result<()> {
    let data = fs::read_to_string(TOKEN_PATH)
        .with_context(|| format!("missing token at {}", TOKEN_PATH))?;
    let token: serde_json::Value = serde_json::from_str(&data)
        .with_context(|| "invalid token json")?;
    let access_token = token["access_token"]
        .as_str()
        .context("no access_token in token file")?;

    let labels: serde_json::Value = reqwest::blocking::Client::new()
        .get("https://gmail.googleapis.com/gmail/v1/users/me/labels")
        .bearer_auth(access_token)
        .send()?
        .json()?;

    println!("LABELS_OK {}", labels);
    Ok(())
}

fn whoami(cfg: &Config) -> Result<()> {
    let account = cfg
        .accounts
        .first()
        .context("no account configured (copy config/personal_mail.example.yaml)")?;
    println!("ACCOUNT_ID={}", account.account_id);
    println!("GMAIL_EMAIL={}", account.gmail_email);
    Ok(())
}

fn main() -> Result<()> {
    let cli = Cli::parse();
    let cfg = if cli.config.exists() {
        load_config(&cli.config)?
    } else {
        default_config()
    };

    if cli.labels_list {
        labels_list()?;
        return Ok(());
    }

    if cli.whoami {
        whoami(&cfg)?;
        return Ok(());
    }

    run_skeleton(&cli, cfg)?;
    Ok(())
}
