# Primary-Source Retrieval Fallbacks

Use these when a publisher landing page is blocked, dynamic, or paywalled. The goal is to recover verifiable evidence, not to bypass access controls.

## DOI metadata and abstracts

1. Query OpenAlex by DOI:
   `https://api.openalex.org/works/https://doi.org/<DOI>`
2. Read `publication_date`, `primary_location`, `open_access`, and `best_oa_location`.
3. If `abstract_inverted_index` is present, reconstruct the abstract by sorting every `(position, word)` pair. This provides exact abstract wording even when the publisher page is inaccessible.
4. Treat reconstructed abstracts as abstract-only evidence: they support reported sample, headline effects, and dates, not unreported methods or limitations.

## arXiv

- Query the Atom API at `https://export.arxiv.org/api/query` by title or keywords.
- Use the returned title, first-posted date, stable `abs` URL, and verbatim abstract.
- Download `https://arxiv.org/pdf/<id>` when methods or tables are needed.
- Preserve both manuscript date and arXiv posting/revision date if they differ.

## Working papers and institutional copies

- Prefer direct NBER, university, author, central-bank, or research-institute PDFs over news coverage.
- Convert PDFs with `pdftotext -layout` so table labels and nearby qualifiers remain visible.
- Search extracted text for the exact statistic, then read surrounding paragraphs and table notes before citing it.
- Record whether the version is peer reviewed, a working paper, or a preprint.

## Authoritative secondary pages

Use an institutional news or research page only when primary full text cannot be retrieved. It may support only claims literally present there. Link the primary DOI alongside the secondary page where possible, and label which source supplied which detail.

## Study-card extraction

For each source capture:

- stable URL and title;
- initial and revision/publication dates;
- design label and randomization unit;
- sample and setting;
- treatment/comparator and duration;
- exact outcome, baseline, effect size, units, and uncertainty;
- ITT versus active-user/TOT status;
- null or adverse outcomes;
- funding/vendor authorship and publication status;
- explicit transfer limitations.

## Verification traps

- A DOI proves bibliographic identity, not that full text was inspected.
- Search snippets are discovery aids, not full-source evidence.
- “Improved completion time by 34%” must be checked before rewriting as “34% more output.”
- Percent changes and percentage-point differences are not interchangeable.
- An unchanged duration does not establish unchanged quality.
- Active-user estimates may reflect selection; report ITT separately.
