# Antenatal prediction of fetal death in MIMIC-IV

Can a high risk of fetal death be seen **before** the delivery admission, using only what was known about the woman beforehand? This project is the antenatal model of the thesis outcome *perinatal death before birth*. It is return R3 (another prediction point) of the staged framework, opened because the model at admission + 6 h (`PerinatalMortality_MIMIC-IV`) found that most fetal deaths were already present at its prediction point.

> **Status (2026-11-18): count audit done.** Outcome card written; the audit of the information available before the admission was run (task A1). Next: predictor table.

[Versión en español](README_es.md)

## Scope

- **Outcome:** fetal death identified from the mother's ICD codes (strict definition, 129 events in 19,440 delivery hospitalizations), always labelled a proxy. Same label as `PerinatalMortality_MIMIC-IV`.
- **Prediction point:** admission time of the delivery hospitalization.
- **Information:** only what was recorded at least 7 days before the admission (earlier admissions, outpatient measurements, outpatient laboratory values) plus patient attributes (age, race and ethnicity, insurance, language, marital status). Nothing of the current admission.
- **Framework:** [`framework.md`](framework.md) (Spanish: [`framework_es.md`](framework_es.md)), version 1.0. Outcome card: [`docs/outcome_card_antenatal.md`](docs/outcome_card_antenatal.md) (Spanish: [`docs/outcome_card_antenatal_es.md`](docs/outcome_card_antenatal_es.md)).

The count audit of the information available before the admission (run 2026-11-18) is written up in [`count_audit.md`](count_audit.md) (Spanish: [`count_audit_es.md`](count_audit_es.md)): every query, what it showed and what it means for the predictors.

## Prerequisites

The cohort and the label are built by the companion projects and read from the same local MIMIC-IV database:

| Table | Built by |
|---|---|
| `mimiciv.cohort_obstetric_v2`, `mimiciv.hadm_delivery_v2` | `MaternalMortality_MIMIC-IV_Cureus` |
| `mimiciv.fetal_death_label_v2` | `PerinatalMortality_MIMIC-IV` (task T16) |

## Repository structure

```
sql/01_audit_counts/   Counts of the information available before the admission (read-only, aggregate output)
sql/02_predictors/     Predictor table of the information window
notebooks/             Models, validation and classification
libraries/             Database connection (environment variables) and helpers
scripts/               check_sql_pair.py: every SQL script and its _es version must have identical code
data/                  Aggregate outputs outputs_*.txt only (counts and metrics)
docs/                  Outcome card, framework figure, reporting documents
```

Every SQL script has a Spanish version with the suffix `_es` and identical code. Only aggregate outputs are published; no `subject_id`, `hadm_id` or patient-level rows, and counts under 5 are shown as "<5".

## Data access

MIMIC-IV is available to credentialed users from PhysioNet under its data use agreement. Copy `.env.example` to `.env` with your local database credentials; `.env` is never committed.

*Confidential: internal use of the research project.*
