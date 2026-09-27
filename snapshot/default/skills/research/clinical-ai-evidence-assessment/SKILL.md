---
name: clinical-ai-evidence-assessment
description: "Use when assessing clinical AI safety and evidence claims."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [research, clinical-ai, medical-devices, regulation, bias, validation]
    category: research
---

# Clinical AI Evidence Assessment

## When to Use

Use for clinical or marketing claims that an AI system detects, diagnoses, predicts, triages, prognosticates, or recommends treatment; for reviews of medical-AI safety, bias, fairness, transferability, drift, clinical utility, regulatory status, or accountability; and for due diligence on AI medical devices and clinical decision support. The workflow applies across specialties, with oncology-specific detail in the linked reference.

Assess claims that an AI system diagnoses, predicts, stratifies, or guides treatment in medicine. Use an evidence ladder that keeps technical performance, external validity, clinical utility, regulation, and legal accountability separate.

Pair with `grounded-citations` for primary-source retrieval and evidence verification. For oncology-specific endpoints and a reusable claim checklist, read `references/oncology-prediction-claims.md`.

## Core rule

Never treat any of the following as interchangeable:

1. transparent reporting;
2. low risk of bias;
3. internal predictive performance;
4. external or prospective validity;
5. regulatory authorization for an exact intended use;
6. improved clinical decisions;
7. improved patient outcomes.

A high AUROC, conformity with a reporting guideline, or FDA/CE status does not by itself establish clinical utility or population-wide safety.

## Procedure

### 1. Normalize the claim

Rewrite the marketing or scientific claim into a testable target:

- current diagnosis, future incidence, recurrence/progression, treatment response, toxicity, or prognosis;
- target population and exclusions;
- intended user and care setting;
- index time and prediction horizon;
- input modality and required equipment;
- exact output and locked decision threshold;
- clinical action expected from each output.

Flag vague uses of “predicts,” “accuracy,” “validated,” and “clinically proven.”

### 2. Identify the applicable evidence framework

Choose by study purpose rather than by the word “AI”:

- prediction-model development/evaluation: TRIPOD+AI;
- risk of bias and applicability: PROBAST+AI;
- diagnostic-accuracy study: STARD-AI;
- trial protocol: SPIRIT-AI;
- completed randomized trial: CONSORT-AI;
- early live clinical evaluation: DECIDE-AI;
- imaging AI: add CLAIM where relevant.

Reporting compliance is not a quality score. Appraise design and analysis independently.

### 3. Establish regulatory scope precisely

Record jurisdiction, regulator, product, manufacturer, model/version, decision identifier, intended use, population, user, inputs, contraindications, and authorization pathway.

- For FDA, inspect the actual database decision or public summary, not only an AI-device list or vendor press release.
- Distinguish final guidance from draft guidance.
- In the EU, separate MDR/IVDR conformity, AI Act classification and staged application dates, and medicinal-product oversight by EMA.
- WHO ethics guidance is a governance framework, not product authorization.

Never generalize authorization for one indication, version, modality, or workflow to another.

### 4. Audit data provenance and leakage

Require a patient flow diagram, source sites and dates, inclusion/exclusion rules, reference standard, blinding, missingness, follow-up, prevalence, and event count.

Check that splits are independent by patient and, when needed, site and time. Look for duplicated patients, lesions, slides, derivative images, temporal leakage, post-outcome variables, treatment leakage, and test-set-driven preprocessing or threshold selection.

### 5. Apply the validation ladder

Classify evidence explicitly:

1. resampling or internal validation;
2. temporal validation;
3. geographic/vendor external validation;
4. prospective silent validation with a frozen model;
5. early live human–AI evaluation;
6. comparative impact study;
7. patient-important outcome trial and post-market effectiveness.

Random splitting within one source is not external validation. A local recalibration is a model change and requires separate evaluation.

### 6. Evaluate performance in clinically meaningful units

Do not accept a single aggregate “accuracy.” Extract:

- sensitivity, specificity, PPV, NPV at prespecified thresholds;
- prevalence and denominators;
- AUROC and, for rare outcomes, precision–recall measures;
- calibration plot, calibration-in-the-large/intercept, slope, and Brier score;
- confidence intervals and paired/cluster-aware analysis;
- comparison with current care on the same cases;
- decision-curve/net benefit or an equivalent threshold justification;
- abstention/OOD rate and performance after abstentions.

### 7. Assess bias and transportability

Examine selection/spectrum, verification, label, measurement, missingness, historical, access, treatment, and temporal bias. Test transfer across sites, countries, scanners, laboratories, protocols, EHR systems, prevalence, staging rules, and care pathways.

For prespecified and clinically relevant subgroups, require sample size, event count, threshold metrics, calibration, confidence intervals, and worst-group errors. Include intersectional groups when feasible. Lack of statistical significance is not evidence of equivalence when subgroup power is low.

### 8. Assess human factors and clinical utility

Describe the full human–AI pathway, not the model alone. Look for automation bias, overrides, alert fatigue, deskilling, interface ambiguity, workload, downtime, and fallback procedures.

Clinical utility requires evidence that using the output improves decisions, workflow, resource use, or patient-important outcomes while accounting for false-positive downstream procedures, false-negative delay, overdiagnosis, anxiety, radiation, and overtreatment.

### 9. Assess drift and lifecycle controls

Distinguish input/data, prevalence, concept, label, workflow, intervention, and software/version drift. Require predefined metrics, baselines, thresholds, review frequency, ground-truth delay handling, owners, incident reporting, recalibration/retraining rules, independent update validation, audit logs, rollback, and safe shutdown.

### 10. Map accountability without giving jurisdiction-free legal conclusions

Identify who controls development, deployment, updates, monitoring, interpretation, and incident response. Review contracts, labeling, audit retention, override documentation, insurance/indemnity, and local professional standards.

State that liability depends on jurisdiction and facts. Regulatory authorization and “human in the loop” are not universal liability shields. Recommend qualified local counsel for a concrete legal conclusion.

## Primary-source hierarchy

1. statutes, regulations, regulator decisions, official guidance;
2. original reporting/appraisal guideline publications;
3. prospective registrations, protocols, statistical analysis plans, and trial reports;
4. manufacturer documentation and public summaries;
5. systematic reviews and independent replication;
6. press releases and marketing only as claims to be tested.

For current regulatory status, verify dates and whether a document is draft, final, in force, or subject to transition. Quote exact wording for load-bearing claims.

## Output format

Deliver:

1. a one-paragraph bottom line;
2. a table separating claim, evidence, and what remains unproved;
3. regulatory status with exact identifiers and scope;
4. safety/bias/transportability findings;
5. validation and clinical-utility evidence ladder;
6. lifecycle/drift and accountability findings;
7. a yes/no/unclear checklist;
8. red flags and evidence gaps;
9. numbered primary-source URLs.

Label assumptions and unavailable documents. Do not infer “safe,” “fair,” or “clinically useful” from absence of reported problems.

## Pitfalls

- Treating reporting-guideline adherence as validation.
- Calling a random split “external validation.”
- Reporting AUROC without calibration or threshold performance.
- Ignoring prevalence when interpreting PPV/NPV.
- Using a curated case-control dataset to support population screening.
- Hiding subgroup uncertainty behind overall averages.
- Calling a retrospective accuracy study “prospective clinical validation.”
- Treating authorization as proof of mortality benefit.
- Ignoring model version, software updates, and post-deployment drift.
- Conflating EMA medicinal-product guidance with EU medical-device authorization.
- Giving a universal liability conclusion across jurisdictions.

## Verification

Before delivery, confirm:

- the claim type, population, horizon, threshold, and clinical action are explicit;
- every regulatory claim is backed by a current primary source;
- draft versus final status and transition dates are correct;
- patient-level/site-level independence and leakage were assessed;
- calibration, subgroup performance, external/prospective validation, and clinical utility are each addressed separately;
- harms, drift, human factors, and accountability are not omitted;
- the conclusion does not outrun the highest completed rung of evidence.