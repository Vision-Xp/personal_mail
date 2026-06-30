use serde::Deserialize;

#[derive(Debug, Deserialize, Clone)]
pub struct CategoryRule {
    #[serde(default)]
    pub name: Option<String>,
    #[serde(default)]
    pub label: Option<String>,
    #[serde(default)]
    pub description: Option<String>,
    #[serde(default)]
    pub signals: Vec<String>,
    #[serde(default)]
    pub score_bonus: i32,
    #[serde(default)]
    pub min_confidence: Option<u8>,
}
