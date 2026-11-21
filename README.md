# Antenatal prediction of fetal death in MIMIC-IV

> **Framework.** This repository applies the thesis's staged framework for clinical prediction models. The framework (stages, gates, criteria and literature) and the catalogue of models with their status are in [StagedFramework_ClinicalPrediction](https://github.com/khem777/StagedFramework_ClinicalPrediction).

Can a high risk of fetal death be seen **before** the delivery admission, using only what was known about the woman beforehand? When the woman arrives at the hospital, the fetal death has often already happened; so this model uses only information from before the admission, and the event happens after the information that predicts it. It follows the staged framework for clinical prediction models.

> **Status (2026-11-19): predictor table built and verified** ([`predictor_table.md`](predictor_table.md)). Sample-size gate (G3) **not passed**: cross-validated Cox-Snell R² of −0.00054 (minimum for 27 parameters: 0.0124; for 17: 0.0078). The antenatal model is reported as a feasibility analysis ([`data/outputs_01_sample_size_gate.txt`](data/outputs_01_sample_size_gate.txt)).

[Versión en español](README_es.md)

## Scope

- **Outcome:** fetal death identified from the mother's ICD codes (strict definition, 129 events in 19,440 delivery hospitalizations), always labelled a proxy.
- **Prediction point:** admission time of the delivery hospitalization.
- **Information:** only what was recorded at least 7 days before the admission (earlier admissions, outpatient measurements, outpatient laboratory values) plus patient attributes (age, race and ethnicity, insurance, language, marital status). Nothing of the current admission.
- **Framework:** [`framework.md`](framework.md) (Spanish: [`framework_es.md`](framework_es.md)), version 1.0. Outcome card: [`docs/outcome_card_antenatal.md`](docs/outcome_card_antenatal.md) (Spanish: [`docs/outcome_card_antenatal_es.md`](docs/outcome_card_antenatal_es.md)).

The count audit of the information available before the admission (run 2026-11-18) is written up in [`count_audit.md`](count_audit.md) (Spanish: [`count_audit_es.md`](count_audit_es.md)): every query, what it showed and what it means for the predictors.

## Requirements and run order

A local PostgreSQL database with MIMIC-IV v3.1 (hosp module). Every table of the model is built from this repository, with names starting with `antenatal_`, so no other table of the database is modified. Run each script as a whole in one connection (DBeaver: Alt+X), in this order:

| Order | Script | Creates | Framework stage |
|---|---|---|---|
| 1 | `sql/00_cohort_and_label/01_obstetric_universe.sql` | `antenatal_obstetric_universe` (obstetric universe, delivery flag) | S2 |
| 2 | `sql/00_cohort_and_label/02_fetal_death_label.sql` | `antenatal_fetal_death_codes`, `antenatal_fetal_death_label` (label by admission) | S3, G1 |
| 3 | `sql/01_audit_counts/01_prior_information.sql` | Nothing (read-only): count audit | S4 |
| 4 | `sql/02_predictors/01_predictor_table.sql` | `antenatal_predictors_v1` (predictor table read by the models) | S6, S7 |
| 5 | `notebooks/01_sample_size_gate.ipynb` | `data/outputs_01_sample_size_gate.txt` (sample-size gate) | G3 |

Reference counts to reproduce: 25,736 obstetric admissions; 19,440 admissions in the population of the model, of 13,735 patients; 129 strict events and 142 with partial codes.

## Repository structure

```
sql/00_cohort_and_label/ Obstetric universe, delivery flag, code catalogue and fetal-death label
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
