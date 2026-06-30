use super::category::CategoryRule;
use serde::Deserialize;

#[derive(Debug, Deserialize, Default, Clone)]
pub struct ClassificationConfig {
    #[serde(default)]
    pub categories: Vec<CategoryRule>,
    #[serde(default)]
    pub quarantine_label: Option<String>,
    #[serde(default)]
    pub default_label: Option<String>,
}

impl ClassificationConfig {
    pub fn best_category<'a>(
        &'a self,
        signals: &[String],
    ) -> Option<(&'a CategoryRule, u8)> {
        let mut best: Option<(&CategoryRule, u8)> = None;

        for rule in &self.categories {
            let mut matches: u8 = 0;
            for signal in signals {
                if rule.signals.iter().any(|s| s == signal) {
                    matches += 1;
                }
            }
            let confidence = if rule.signals.is_empty() {
                0u8
            } else {
                ((matches as f32 / rule.signals.len() as f32) * 100.0).clamp(0.0, 100.0) as u8
            };

            if let Some(min) = rule.min_confidence {
                if confidence < min {
                    continue;
                }
            }

            match best {
                Some((_, bc)) if confidence > bc => best = Some((rule, confidence)),
                None => best = Some((rule, confidence)),
                _ => {}
            }
        }

        best
    }
}
