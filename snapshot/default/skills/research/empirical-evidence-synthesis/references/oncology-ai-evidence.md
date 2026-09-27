# Oncology AI evidence synthesis

Use this note when evaluating AI for prognosis, treatment selection, toxicity, surgery, radiotherapy, or drug discovery in oncology.

## Evidence ladder

1. **Prospective AI-guided randomized trial:** patients are assigned to AI-guided versus standard decisions; report patient outcomes, harms, calibration, and workflow failures.
2. **Locked biomarker tested on randomized-trial specimens:** useful for treatment-by-biomarker interaction, but label it retrospective/post-hoc unless prespecified. It does not prove that deploying the AI improves outcomes.
3. **Prospective external validation:** validates discrimination/calibration in new patients but not clinical utility.
4. **Retrospective external validation:** hypothesis-strengthening only; inspect site, scanner, staining, treatment-era, and selection shifts.
5. **Internal cross-validation/development cohort:** experimental, regardless of high AUC/C-index.

Never treat regulatory clearance for diagnosis, segmentation, or workflow automation as approval to predict recurrence or select therapy. Separate:
- **prognostic** association (outcome risk regardless of treatment),
- **predictive** effect modification (treatment-by-biomarker interaction), and
- **clinical utility** (better outcomes when care is actually guided by the test).

## Primary-source retrieval pattern

- PubMed/Europe PMC search APIs are effective for exact titles, DOI/PMID discovery, and abstracts. For exact numerical claims, retrieve PubMed XML via `eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=<PMID>&retmode=xml` rather than relying on snippets.
- FDA De Novo/510(k) decision summaries often state the intended use, adjunctive-use restrictions, reader-study deltas, and per-biopsy versus per-patient caveats more precisely than marketing pages.
- ClinicalTrials.gov API v2 (`clinicaltrials.gov/api/v2/studies/<NCTID>`) exposes current status, enrollment, sponsor, and `whyStopped`. Use it to distinguish completed, recruiting, and terminated AI-associated drug programs; trial registration is not efficacy evidence.

## Extraction card

For every model record:
- cancer, stage, modality, and intended decision;
- development, lock, and validation cohorts separately;
- prospective/retrospective and randomized/non-randomized status;
- exact endpoint and follow-up;
- AUC/C-index **and calibration**, or HR/absolute risk difference with CI;
- treatment-by-model interaction for therapy-selection claims;
- missing samples/failed scans and unit of analysis (slide, lesion, patient);
- comparator (clinician, clinical score, established biomarker);
- funding, vendor role, regulatory status, and whether the model is commercially available;
- explicit boundary: what the evidence does **not** establish.

## Recurring pitfalls

- Calling an archival analysis of phase III trial specimens a prospective validation or a new randomized AI trial.
- Interpreting “no statistically significant benefit” in a model-negative subgroup as proof that treatment can safely be omitted; wide CIs may include meaningful benefit or harm.
- Confusing response prediction among treated patients with a predictive treatment biomarker; favorable prognosis can produce the same association.
- Comparing slide-level sensitivity gains with patient-level benefit when each patient contributes multiple slides or lesions.
- Reporting only discrimination. Dataset shift can leave AUC apparently acceptable while calibration is unsafe.
- Treating gene-expression assays as modern adaptive AI without qualification; many are fixed classifiers, though their treatment evidence can be stronger than newer neural networks.
- Treating an AI-discovered molecule entering phase I as validation of drug-discovery productivity. Check therapeutic index, termination reasons, phase transition, and published human efficacy.
- Omitting negative external validations. In high-stakes synthesis, modest or null prospective results are especially valuable counterevidence.

## Recommended output structure

1. Scope/date and non-medical-advice boundary.
2. Regulatory/clinical availability table, with exact intended use.
3. Evidence by decision domain: recurrence/survival, radiomics/pathomics, genomics, systemic therapy/immunotherapy, radiotherapy, surgery, toxicity.
4. Separate drug-discovery section.
5. Cross-cutting limitations and bottom-line maturity tiers.

Use direct URLs to primary papers, FDA summaries, and trial records. Preserve absolute effects alongside relative effects whenever available.