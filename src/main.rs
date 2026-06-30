use anyhow::{Context, Result};
use clap::{Parser, ValueEnum};
use serde::Deserialize;
use std::path::PathBuf;

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
    let content = std::fs::read_to_string(path)
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

fn main() -> Result<()> {
    let cli = Cli::parse();
    let cfg = if cli.config.exists() {
        load_config(&cli.config).with_context(|| {
            format!(
                "config invalid: {} (copy config/personal_mail.example.yaml)",
                cli.config.display()
            )
        })?
    } else {
        default_config()
    };

    let mode = match cli.mode.unwrap_or_else(|| {
        Mode::from_str(&cfg.modes.default_mode, true)
            .unwrap_or(Mode::DryRun)
    }) {
        Mode::DryRun => "dry-run",
        Mode::SafeRun => "safe-run",
        Mode::ApplyRun => "apply-run",
        Mode::AuditRun => "audit-run",
    };

    println!("STATUS=phase2_skeleton");
    println!("CONFIG={}", cli.config.display());
    println!("MODE={}", mode);
    println!("ACCOUNTS={}", cfg.accounts.len());
    if let Some(account) = cfg.accounts.first() {
        println!("ACCOUNT_ID={}", account.account_id);
        println!("GMAIL_EMAIL={}", account.gmail_email);
    }

    if mode != "dry-run" {
        anyhow::bail!("only dry-run is allowed in Phase 2 skeleton");
    }

    println!("DRY_RUN_COMPLETE");
    Ok(())
}
