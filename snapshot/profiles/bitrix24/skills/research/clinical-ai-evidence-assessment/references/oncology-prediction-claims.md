# Oncology AI prediction claims: evidence notes and checklist

Use this reference when a system claims to detect or predict cancer, recurrence, progression, response, toxicity, or survival. It condenses a reusable oncology-specific review; always re-check current regulatory status and source text.

## Authoritative source bank

- WHO, *Ethics and governance of artificial intelligence for health* (2021): https://www.who.int/publications/i/item/9789240029200
- FDA, AI-Enabled Medical Devices list and scope: https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-enabled-medical-devices
- FDA draft, *AI-Enabled Device Software Functions: Lifecycle Management and Marketing Submission Recommendations* (2025): https://www.fda.gov/regulatory-information/search-fda-guidance-documents/artificial-intelligence-enabled-device-software-functions-lifecycle-management-and-marketing
- FDA final, PCCP for AI-enabled device software functions (2024): https://www.fda.gov/regulatory-information/search-fda-guidance-documents/marketing-submission-recommendations-predetermined-change-control-plan-artificial-intelligence
- FDA/Health Canada/MHRA, GMLP guiding principles: https://www.fda.gov/medical-devices/software-medical-device-samd/good-machine-learning-practice-medical-device-development-guiding-principles
- EMA, *Reflection paper on the use of AI in the medicinal product lifecycle* (2024): https://www.ema.europa.eu/en/documents/scientific-guideline/reflection-paper-use-artificial-intelligence-ai-medicinal-product-lifecycle_en.pdf
- EU AI Act, Regulation (EU) 2024/1689: https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng
- EU Product Liability Directive, Directive (EU) 2024/2853: https://eur-lex.europa.eu/eli/dir/2024/2853/oj/eng
- TRIPOD+AI (2024): https://pmc.ncbi.nlm.nih.gov/articles/PMC11019967/
- CONSORT-AI (2020): https://pmc.ncbi.nlm.nih.gov/articles/PMC7490784/
- SPIRIT-AI (2020): https://pmc.ncbi.nlm.nih.gov/articles/PMC7490785/
- DECIDE-AI (2022): https://pmc.ncbi.nlm.nih.gov/articles/PMC9116198/
- PROBAST+AI (2025): https://pmc.ncbi.nlm.nih.gov/articles/PMC11931409/
- STARD-AI (2025; check subsequent corrections): https://pubmed.ncbi.nlm.nih.gov/40954311/

## Exact distinctions worth preserving

- FDA's AI-device list says listed devices met applicable premarket requirements for their intended use, but the list is not comprehensive and public summaries are not all-inclusive. Inspect the device-specific database record.
- FDA's final PCCP framework has three components: Description of Modifications, Modification Protocol, and Impact Assessment.
- The 2021 GMLP principles explicitly call for representative populations, independent training/test data, clinically relevant testing including important subgroups, user disclosure, and monitoring deployed models for unintended bias, degradation, and dataset drift.
- EMA's reflection paper covers AI/ML in the medicinal-product lifecycle. It is not a substitute for MDR/IVDR conformity of an AI medical device. For high-impact settings, it emphasizes prospectively generated data representative of future use.
- Under the EU AI Act, medical-device AI may be high-risk when Article 6(1) conditions are met. Re-check staged application dates before every current-status answer.
- TRIPOD+AI has 27 main items and 52 subitems; it is for reporting prediction-model studies, not certification.
- PROBAST+AI separates model development quality/applicability from model evaluation risk of bias/applicability and uses four domains: participants/data sources, predictors, outcome, and analysis.
- CONSORT-AI adds 14 items; SPIRIT-AI adds 15. They emphasize version, inputs, poor-quality/unavailable data, human–AI interaction, outputs, workflow, and error cases.
- DECIDE-AI covers early, small-scale evaluation in live clinical settings and emphasizes clinical utility, safety, human factors, and preparation for larger comparative trials.
- STARD-AI adds or modifies 18 items beyond STARD 2015 and emphasizes dataset practices, the AI index test, bias, fairness, applicability, and generalizability.

## Oncology-specific harms and biases

Assess explicitly:

- spectrum bias from tertiary-center, biopsy-confirmed, advanced-stage, or operable-only cohorts;
- verification bias when only positives receive pathology or long follow-up;
- pathology/report labels that reproduce access or diagnostic practice;
- scanner, staining, assay, reconstruction, laboratory, and EHR domain shift;
- stage, histology, molecular subtype, treatment-era, and prevalence shift;
- lead-time bias, length bias, overdiagnosis, competing risks, informative censoring;
- treatment leakage and post-index variables;
- repeated patients, lesions, slides, patches, and derivative-image leakage;
- downstream false-positive biopsies, surgery, radiation, anxiety, and overtreatment;
- false-negative diagnostic delay and missed treatment opportunity.

## Reusable checklist

### Claim and pathway
- [ ] Prediction target is explicit: current cancer, future incidence, recurrence, progression, response, toxicity, or prognosis.
- [ ] Population, exclusions, setting, index time, horizon, outcome, user, threshold, and downstream action are defined.
- [ ] “Accuracy,” “validated,” and “clinical” are used with operational definitions.

### Regulation
- [ ] Regulator, manufacturer, product/version, decision identifier, exact intended use, user, modality, and limitations are verified.
- [ ] Draft guidance is not presented as final law.
- [ ] FDA/CE status is not treated as proof of mortality or quality-of-life benefit.
- [ ] Update authority and any PCCP/change-control limits are known.

### Data and bias
- [ ] Source sites, dates, selection, flow diagram, reference standard, blinding, missingness, follow-up, prevalence, and event count are reported.
- [ ] Splits are independent by patient and, where needed, site and time.
- [ ] Test data did not influence preprocessing, feature selection, hyperparameters, threshold, or recalibration.
- [ ] Predictors were available at the intended prediction time.
- [ ] Case-control enrichment is not used to infer screening PPV without correction and external testing.

### Performance
- [ ] Sensitivity, specificity, PPV, NPV, prevalence, denominators, and confidence intervals are shown at a prespecified threshold.
- [ ] Calibration plot/intercept/slope and overall prediction error are reported.
- [ ] Precision–recall performance is considered for rare outcomes.
- [ ] Comparison with current care uses the same cases and appropriate paired/cluster-aware analysis.
- [ ] Decision/net benefit and the harms of downstream actions are assessed.

### Transfer and equity
- [ ] Temporal and geographic/vendor external validation exist.
- [ ] Prospective silent validation used a frozen model and analysis plan.
- [ ] Subgroups include age, sex/gender where relevant, race/ethnicity/ancestry or skin tone where relevant, geography/access, comorbidity, tumor type/stage/histology/molecular subtype, and site/equipment.
- [ ] Each subgroup has N, events, threshold metrics, calibration, confidence intervals, and false-negative analysis.
- [ ] OOD detection, abstention, and fallback are evaluated.

### Utility and lifecycle
- [ ] Live human–AI evaluation covers overrides, automation bias, alert fatigue, workload, and error cases.
- [ ] A comparative impact study assesses patient-important benefit and harm.
- [ ] Drift monitoring covers input, prevalence, concept, label, workflow, treatment era, and software/version change.
- [ ] Metrics, thresholds, owners, review frequency, incident response, update validation, rollback, and safe shutdown are predefined.

### Accountability
- [ ] Developer, deployer, clinic, and user's responsibilities are documented.
- [ ] Model version, output, overrides, updates, and incidents are auditable.
- [ ] Contracts, insurance/indemnity, labeling, informed disclosure, and local professional law were reviewed.
- [ ] Any legal conclusion is scoped to the jurisdiction and facts.

## High-signal red flags

- “95% accurate” without metric, denominator, prevalence, threshold, or confidence interval.
- AUROC alone; no calibration or PPV at real-world prevalence.
- Random split from one archive called “external validation.”
- Retrospective accuracy called “prospective clinical validation.”
- Screening claim based on a curated case-control dataset.
- Overall performance without subgroup event counts and uncertainty.
- FDA/CE mention without decision number and intended use.
- Mutable model without versioning, change control, or drift plan.
- Earlier diagnosis or longer survival-from-diagnosis presented as reduced mortality.
- Guideline adherence presented as low risk of bias or clinical utility.
