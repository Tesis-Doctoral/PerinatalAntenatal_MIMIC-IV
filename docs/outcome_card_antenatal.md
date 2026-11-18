# Outcome card — antenatal prediction of fetal death, MIMIC-IV

Version 1, 2026-11-18. Third application of the staged framework ([`../framework.md`](../framework.md), version 1.0). It is return **R3** (another prediction point) of the outcome *perinatal death before birth*, whose first model (`PerinatalMortality_MIMIC-IV`, prediction at admission + 6 h) found that 73 of 129 fetal deaths were already present at the prediction point (count audit group G, task T45). Fields marked **pending** are fixed, and recorded in the decision log, before the gate that needs them. Spanish version: [`outcome_card_antenatal_es.md`](outcome_card_antenatal_es.md).

## 1. The question

At admission, the fetal death has often already happened: a model at admission + 6 h recognizes it (early identifier). This model asks a different question: **with what was known about the woman before this admission, could a high risk of fetal death be seen?** Only information recorded before the admission enters the model, so the event happens after the information that predicts it.

## 2. Identity

| Field | Value | Source |
|---|---|---|
| Outcome | Perinatal death before birth (fetal death or stillbirth), always labelled a proxy | perinatal D2 |
| Rung | Same outcome; new prediction point (return R3) | — |
| Data source | MIMIC-IV v3.1; tables of the maternal and perinatal projects (section 7) | — |
| Unit and group | Delivery hospitalization; patient as grouping unit | perinatal D4 |
| Population | Population of perinatal D3: delivery flag (v2) or stillbirth code, 19,440 admissions | perinatal D3 |
| Main label | Strict code at any gestational age (`fetal_death_label_v2.label_main`): 129 events (0.66%) | perinatal D5, T16 |
| Sensitivity labels | Strict plus partial; 22 and 28 weeks or more (ICD-10 only); without early-loss codes | perinatal D5 |

## 3. Prediction point and information window (S6)

| Field | Value |
|---|---|
| Time zero and prediction point | Admission time of the delivery hospitalization |
| Information window | Everything recorded **at least 7 days before** the admission: earlier MIMIC-IV admissions discharged by then, outpatient measurements (OMR) and outpatient laboratory values dated by then |
| Why 7 days | A fetal death diagnosed at an outpatient visit is usually followed by an admission within days. A buffer keeps information recorded after the death out of the model. Sensitivity: 1 and 30 days |
| Also allowed | Patient attributes of the current admission that do not depend on how she arrived: age, race and ethnicity, insurance, language, marital status |
| Excluded | Anything of the current admission: diagnoses, procedures, laboratory values, admission type and admission location (they reflect how she presented, which the event itself can cause), emergency department data |

## 4. Candidate predictors (S7)

Chosen by clinical rationale before any model; the final list depends on coverage (counts of section 8, coverage rule of 10% of the population). Each block has an indicator of whether any information exists: **absence of a record is not absence of the condition**, because many women have no earlier encounter in this hospital.

| Block | Variables |
|---|---|
| Registration | Age; race and ethnicity (5 groups); insurance; language; marital status |
| Encounter history | Any earlier admission; number of earlier admissions; any earlier obstetric admission; days since the last discharge |
| Obstetric history (earlier admissions) | Earlier fetal death or stillbirth; earlier preterm delivery; earlier cesarean; earlier preeclampsia, eclampsia or gestational hypertension; gestational diabetes in an earlier pregnancy |
| Chronic conditions (earlier admissions) | Chronic hypertension; pregestational diabetes; obesity; chronic kidney disease; thyroid disease; systemic lupus or antiphospholipid syndrome; thrombophilia; tobacco, alcohol or drug use; HIV or syphilis |
| Outpatient measurements (OMR) | Last body mass index, weight, systolic and diastolic blood pressure in the window |
| Outpatient laboratory values | Last hemoglobin A1c, hemoglobin and creatinine in the window |

## 5. Sample size and learner (G3, S8)

| Field | Value |
|---|---|
| Candidate parameters | **Pending** (count every category and indicator) |
| Supported parameters | About 17 to 25, from the perinatal pre-estimate (same events and prevalence); the gate uses the observed Cox-Snell R² |
| Primary learner | Penalized logistic regression (events per parameter below 20); tree models and the ensemble as comparisons |
| Reduced predictor set | Fixed before G3: registration, encounter-history indicator, the three obstetric-history variables with most coverage, chronic hypertension, pregestational diabetes, last blood pressure and body mass index with their indicators. Never chosen by association with the outcome |

## 6. Classification criteria (G4)

| Criterion | How it applies | Status |
|---|---|---|
| C1, events already present | The information window closes 7 days before admission, so a death after that point is after the information. A death before it cannot be excluded with codes; the 1-day and 30-day buffers test how much this matters | Applicable through the buffer sensitivity |
| C2, outcome with time | The event is after the information window by design | Applicable |
| C3, detection bias | The outcome is not defined from a test | Not applicable |
| C4, stability over time | Development before 2017, a single test from 2017 onward | Applicable |

**Stated before the results.** Antenatal models of stillbirth built on maternal characteristics usually reach an AUROC of about 0.60 to 0.75. The framework classifies a model as a predictor only with an AUROC of 0.75 or more, so this model may be classified as *neither* if it falls below that. The threshold is not changed for this outcome; any proposal to change it must be decided with the supervisor before the first model is fitted.

## 7. Prerequisites (built by the other projects)

`mimiciv.cohort_obstetric_v2`, `mimiciv.hadm_delivery_v2` (MaternalMortality_MIMIC-IV_Cureus) and `mimiciv.fetal_death_label_v2` (PerinatalMortality_MIMIC-IV, task T16), plus the MIMIC-IV tables `admissions`, `patients`, `diagnoses_icd`, `omr`, `labevents`.

## 8. Next tasks

1. Count audit A1: how many admissions of the population have any information in the window (earlier admission, OMR, outpatient laboratory value), in events and non-events, by era and buffer.
2. Coverage of each candidate predictor; fix the final list and the candidate parameters.
3. Predictor table; sample-size check (G3).
4. Nested grouped validation, criteria C1, C2 and C4, classification.

*Confidential: internal use of the research project.*
