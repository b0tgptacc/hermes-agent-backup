---
name: empirical-evidence-synthesis
description: "Use when synthesizing measured effects across studies."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [research, experiments, causal-inference, evidence-synthesis, productivity]
    category: research
---

# Empirical Evidence Synthesis

Build concise, decision-ready syntheses of experiments and measured real-world effects without flattening unlike designs into one headline number.

## When to Use

Use for requests asking what research *shows* about an intervention, especially when the answer must compare field experiments, RCTs, production rollouts, surveys, effect sizes, and limitations. Pair with `grounded-citations` for citation-ledger verification and with domain search skills where available.

## Procedure

1. **Define the outcome and evidence boundary.** Separate task speed, output quality, throughput, adoption, time saved, errors, retention, and organization-level output. Do not silently substitute one for another.
2. **Prioritize primary evidence.** Prefer peer-reviewed articles and author/institutional full texts, then registered working papers or preprints. Use authoritative summaries only when the primary page is inaccessible, and identify them as secondary.
3. **Classify each design before summarizing it.** Record whether it is a preregistered online experiment, randomized field trial, staggered production rollout, quasi-experiment, observational study, or self-reported survey.
4. **Extract a study card.** Capture publication/revision date, sample size, setting, treatment, comparator, duration, exact outcome definition, effect size and units, uncertainty/significance when reported, heterogeneity, and external-validity limits.
5. **Distinguish estimands.** Keep intent-to-treat effects separate from treatment-on-treated or active-user estimates. Do not compare percent changes with percentage-point changes as if equivalent.
6. **Check the denominator.** A 30-minute weekly saving, a 12% faster document cycle, and a 12% increase in total worker output are different claims. Preserve baselines and exposure shares when available.
7. **Search actively for counterexamples.** Include null and negative results, tasks outside the tool's capability boundary, and settings where users misperceive their own performance.
8. **Synthesize, do not average blindly.** State where effects replicate, which tasks/settings differ, and why a universal productivity coefficient is unsupported.
9. **Deliver 6–10 findings when requested.** Each finding should include the design, date, sample, exact figure, direct URL, and one explicit limitation.
10. **Verify every number against retrieved text.** Abstracts support only what they explicitly report. Retrieve full text for methods, subgroup definitions, confidence intervals, and nuanced limitations.

## Output Pattern

For each finding:

- **Decision-relevant conclusion.** Design and setting; `N`; date.
- Exact effect size with metric and comparator.
- Main limitation or boundary condition.
- Inline citation to a direct primary or authoritative URL.

End with a short synthesis separating task-level efficacy, realized workplace adoption/effectiveness, and evidence gaps or transfer limits.

## High-Stakes Medical Screening and Diagnostic AI

For cancer screening, radiology, pathology, endoscopy, and other diagnostic-AI syntheses, add the following checks:

1. **Use a clinical-maturity ladder.** Keep retrospective test-set validation, simulated reader studies, prospective diagnostic cohorts, real-world implementation studies, RCTs, and patient-outcome/mortality trials in separate evidence tiers. Regulatory authorization is evidence of a reviewed intended use, not proof of prospective clinical utility.
2. **Preserve screening denominators and outcome definitions.** Report sensitivity, specificity, PPV, false-positive/recall rates, detection per 1,000, interval cancers, and workload in their original units. Do not treat AUC, lesion-level sensitivity, adenoma detection rate, or stage shift as interchangeable with mortality benefit.
3. **Track downstream burden.** Extract repeat imaging, recalls, non-neoplastic resections, biopsies, invasive procedures, diagnostic-resolution time, reading/procedure time, and workload changes—not only added detections.
4. **Separate per-lesion, per-slide, per-biopsy, per-examination, and per-patient effects.** If a regulator warns that a per-biopsy gain will likely be smaller per patient, carry that limitation into the conclusion.
5. **Check for interval disease and overdiagnosis.** Higher screen detection is not enough; look for interval cancers, advanced-stage incidence, false reassurance after negative results, and eventual mortality. Label surrogate endpoints explicitly.
6. **Handle newly disclosed trial results conservatively.** When current results exist only as an abstract, conference presentation, sponsor release, or editorial before the primary peer-reviewed report, cite both the disclosure and an independent source, identify prespecified primary versus secondary/exploratory endpoints, and state that the figures remain preliminary.
7. **Report population transfer limits.** Record age, referral versus population-screening setting, enrichment, race/ethnicity or skin phototype, center count, device/scanner constraints, and whether clinicians self-selected AI use.

For an 8–12 finding brief, aim to cover all requested modalities while reserving at least one finding for a null, adverse, or failed-primary-endpoint result. End with a compact maturity ranking and a sentence on whether mortality benefit has actually been shown.

## Pitfalls

- Calling every controlled or causal study a “field experiment.”
- Reporting active-user gains as the average effect of granting access.
- Treating self-reported time saved as verified output growth.
- Omitting null/negative outcomes from the same study.
- Converting “19 percentage points less likely to be correct” into “19% slower.”
- Using a search snippet for claims not present in the snippet.
- Inferring meeting quality from unchanged meeting duration, or vice versa.
- Presenting a vendor-authored field study without disclosing authorship and preprint status.
- Treating a DOI landing page as proof that the full methods were inspected.

## Retrieval Support

See `references/primary-source-retrieval.md` for resilient retrieval of abstracts and full text when publisher pages are blocked.

For oncology AI—prognosis versus treatment prediction, regulatory intended-use checks, post-hoc trial-specimen analyses, toxicity, surgery, and AI drug discovery—use `references/oncology-ai-evidence.md`.

## Verification Checklist

- Every numerical claim maps to retrieved source text.
- Dates distinguish initial publication from later revision where relevant.
- Sample sizes and settings are explicit.
- Percent and percentage-point units are preserved.
- Experimental design labels are accurate.
- Null and adverse effects are represented.
- The conclusion does not outrun the studied task, population, or duration.
