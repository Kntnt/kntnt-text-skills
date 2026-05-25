---
name: report
swedish_term: rapport
default_technique: pac
triggers:
  - rapport
  - report
  - whitepaper
  - "white paper"
  - vitbok
not_triggers:
  - "'rapport' inside a quoted working title for an article (reportage)"
  - "'skriv en analys' / 'write an analysis' without 'rapport'/'report' — too broad"
  - styrelseprotokoll
  - mötesprotokoll
  - "board minutes"
  - "meeting minutes"
---

# Report

## Purpose

A report (Swedish *rapport*, often *whitepaper*) is a long, evidence-heavy document whose purpose is to inform, persuade, or serve as reference in a decision situation. The genre spans:

- *Whitepaper / external authority report* — published as gated content or free PDF, often used as lead magnet.
- *Research or investigation report* — documents method and findings.
- *Client or quarterly report* — recurring analytical accounting to a specific recipient (consultant-to-client, agency-to-management). For example: *Report on SEO, SEM and CRO as of 31 March 2026*.
- *Internal report* — sales report, problem/incident report, status against KPIs.
- *Strategic analysis report* — decision support, market analysis, industry analysis.

The reader differs from the article or web-copy reader: she is in decision-maker or analyst mode. Not scanning, not entertainment-seeking. She has either commissioned the report or needs to act on it. She expects the text to withstand scrutiny — numbers verifiable, conclusions traceable to evidence.

E-book chapters can be written as reports in addition to article or case study. The agent asks per chapter.

Not included: board minutes, meeting minutes, legal documents, contracts. Different genres, out of scope.

## Stylistic nuance

<!-- scope: write -->
### Tone

Analytically rigorous *with rhythm* — not dry-and-clinical, not bureaucratic. Value-laden expressions are avoided unless concretely motivated (*A fantastic rise* never; *The rise was noticeable* if the data warrant it). The analysis itself has drive — the text takes the reader on an investigative journey: data observed, patterns identified, mechanisms explained, conclusions drawn.

<!-- scope: write -->
### Authorial voice

Invisible personally. The text should feel written by an analyst, not by an author with a persona. No first person singular. The author's authority comes from the evidence and the analysis, not from her presence.

<!-- scope: write -->
### Headings

H1 is the report's title, maximum 60 characters. Descriptive H2 and H3 — not numbered (no *1.*, *1.1*, *1.2*). H2 carries the thematic area; H3 carries the function-bearing subsection title. Subsection titles may be simultaneously a label and a discovery — *Thirty-five search terms explain the entire gap*, *Purchase intent crowds out category content* — never teasing, but information-rich so they help the reader navigate and prepare the conclusion.

<!-- scope: write -->
### Recurring inner pattern

The PAC pattern (Premise → Analysis → Conclusion) typically appears within each large section: premise (data, historical context, starting point we build on) → analysis (mechanism, finding, what the premise actually means) → conclusion (recommendation or implication). Used where it serves the material, never as a straitjacket. Not avoided for variation's sake either — if the pattern serves the section, it serves. See `lib/techniques/pac.md`.

<!-- scope: write -->
### Opening

A short introductory paragraph directly under H1 establishes scope, purpose, and period. No labelled summary section at normal length (about three thousand words). At five thousand words or more, or on explicit request, add an executive summary as a separate front-loaded section.

<!-- scope: write -->
### Voice and pronouns

The pronoun system that realises the reporting voice is set by the loaded language file. The universal principle: the reporting or acting organisation speaks in first-person plural; the subject under examination is referred to in the third person, by name when it is an organisation. No direct second-person anywhere.

<!-- scope: write -->
### Rhetorical questions

Sparingly and with weight, only to mark a decision point where the reader needs to act (*What does SafeTeam's leadership want?*). The agent does not invent rhetorical questions — if they appear in the source material, they can be kept and improved. Otherwise they are not introduced.

<!-- scope: write -->
### Paragraphs

Three to five sentences typical. Strict grammar. No sentence fragments. No one-word sentences. No conjunction-as-sentence-opener. Variation exists but within grammatical bounds. These limits apply even though they are looser in article, case-study, web copy, column, and opinion.

<!-- scope: write -->
### Argument order

Evidence before conclusion (general principle from `rules/style.md`, applied strictly here). Conclusion sections come at the end of each major section, after the reader has seen the basis.

<!-- scope: write -->
### Numerical precision

High density. Apply the loaded language file's typographic rules rigorously — percentage convention, no-break space between number and unit, dates in the language's standard format. Abbreviations introduced with the full form at first occurrence per `rules/abbreviations.md` — *search engine optimisation (SEO)* — then abbreviated.

<!-- scope: write -->
### Tables, graphs, and images

Used where the information is comparative, time-series, or numerically dominated. Table captions describe what is shown. Graphs are referred to with explicit prose around them.

### Standalone readability

Stronger version of the body-text-standalone rule. Each H2 and H3 section must be readable by an analyst who has jumped directly to it from the table of contents, without losing the thread.

<!-- scope: write -->
### Length

Typically fifteen hundred to three thousand words. Longer for comprehensive material, but length is governed by what the material warrants — never filler.

<!-- scope: write -->
## Default technique

PAC (Premise → Analysis → Conclusion). See `lib/techniques/pac.md`. ABT is not the default for report and is not mentioned here as a fallback — if the user wants ABT in a report, the user names it explicitly.

<!-- scope: review -->
## Common pitfalls

Value-laden expressions without motivation. *Fantastic rise*, *catastrophic fall*, *impressive results*. The report lets the numbers speak. Describe what happened with precision, not with adjectives that add drama without information.

Conclusion before evidence (anti-PAC). The conclusion is delivered before the data have been presented. The reader is forced to trust the writer rather than follow the reasoning. Premise → Analysis → Conclusion must be honoured in that order where the technique is used.

Author appearing personally. *We believe that*, *my view is that*, *personally I think*. Breaks the neutrality pact. The analysis's authority comes from the evidence — not from the writer's person.

Bureaucratic dryness — the opposite extreme. *The present report aims to set out…* Stiltedness that kills the text. The report is analytically rigorous *with rhythm* — not transport-paragraph prose.

Speculation without marking. Assumptions, hypotheses, correlations that are not necessarily causal — slipped in as though they were established facts. The report's credibility depends on uncertainty being marked clearly: *appears*, *indicates*, *correlates with without necessarily causing*.

Untraceable sources without marking. Claims whose source cannot be traced must be marked as such — *based on industry conversations*, *estimate without available published data*, *informal internal observation*. Never presented as if they were established facts with traceable sources.

Invented recommendations. Recommendations may not be added beyond what the source material supports. If the source material only delivers understanding — without pointing to actions — the report carries that understanding without adding action proposals. There may be a plan the agent does not know about, and speculative proposals risk working against it. Recommendations come from the brief or source material — never from the writing itself.

<!-- scope: review -->
## Regulatory reminders specific to report

Sentence fragments and one-word sentences are forbidden in reports even though they are permitted in article, case study, web copy, column, and opinion.

Voice consistency. The reporting voice stays consistent through the entire report — the sender's position relative to the subject under examination must not drift.

## Trigger keywords

Triggers: rapport, report, whitepaper, white paper, vitbok.

The lean trigger principle applies. Canonical forms in both languages plus the idiosyncratic Swedish *vitbok*. Compounds and conjugations (*månadsrapport*, *kvartalsrapport*, *årsrapport*, *statusrapport*, *analysrapport*, *branschrapport*, *forskningsrapport*, *utredningsrapport*, *skriv en rapport*, *monthly report*, *quarterly report*) are handled by the agent's semantic matching.

Does not trigger: when *report* or *rapport* appears inside a working title or quoted proposed title (e.g., *write an article with the working title "Report from the security conference"*) — this is reportage-article territory and goes to `article.md`. Also: board minutes, meeting minutes, legal documents. *Write an analysis* without *report* / *rapport* — too broad; ask instead. *Write a summary* — general territory unless explicitly a summary report.
