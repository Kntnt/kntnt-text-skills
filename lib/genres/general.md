---
name: general
swedish_term: "allmän text"
default_technique: none
default: true
triggers:
  - "allmän text"
  - "general text"
  - mejl
  - email
  - "e-mail"
  - brev
  - letter
  - PM
  - promemoria
  - memo
  - memorandum
---

# General

## Purpose

`general` is the fallback content type. It is used when the user's prompt does not clearly activate any of the other content types — article, case-study, press-release, web-copy, teaser, report, column, opinion — but the user still wants the text written in the plugin's voice with the plugin's rules applied.

Typical uses:

- *Letters and emails* — external letters to partners, customers, suppliers; business emails.
- *Short summaries* — of meetings, of source material read, of an event.
- *Memos and internal notes* — internal communications.
- *Ad-hoc texts without a clear genre* — e.g., *write a short presentation of X for a conference programme entry*.
- *Proposal texts that are not reports* — shorter offers, project pitches, descriptive pitch text.

What `general` is *not*: genre-specific texts that have their own content type. If something can land in article, case-study, press release, web copy, teaser, report, column, or opinion — it goes there.

`general` is also not a *write whatever* licence. The rules in `rules/writing.md`, the loaded language file, and `rules/style.md` still apply.

## Stylistic nuance

`general` has minimal stylistic profile of its own. It inherits `rules/style.md` directly and lets the material and purpose govern the details — the point of a fallback is not to force ad-hoc texts into conventions that do not fit them. But some frames are worth writing out.

### Address

Depends on subgenre and relationship. Letter or email to a private person or well-known customer: direct second-person is natural. Business email without an established relationship: more formal, the impersonal or formal pronoun the loaded language file specifies. Internal memo: third person or first-person plural (the organisation's voice). Ad-hoc text without a clear addressee: the brief governs; ask when unclear.

### Structure

No imposed template. The material governs. Conventional parts are respected where they exist. Letter: greeting → matter → closing → signature (if requested). Email: subject line (if requested) → greeting → matter → closing. Memo: date/heading → background → point → conclusion or action. Other: logical order the material requires.

### Length

Range from a single sentence to a few hundred words. Longer texts drift naturally toward article or report — but do not ask if length grows. If the text needs to be long, it is long.

### Headings

Optional. Short letters, emails, memos need none. Longer general texts can have subheadings (descriptive, maximum 60 characters).

### Standalone readability

Still applies — the text should read without depending on subject lines, headings, or other external context.

### Format conventions

Email may have a subject line generated separately. Letters may have date and address line if requested. Memos may have heading and date. None of this is default — generate these elements only when the brief asks for them.

## Default technique

None. ABT or PAC may be applied if the material and purpose support it, but nothing is applied automatically. If the user explicitly invokes a technique (*write a text, use the ABT framework*), apply that technique — `general` accepts any installed technique on explicit request.

## Common pitfalls

Forced genre convention. Adding a standfirst, an ABT arc, subheadings, or other structural apparatus from other content types when the material does not require them. A three-sentence email needs no narrative arc. A short memo needs no lead. `general` inherits `rules/style.md` but not any specific genre template.

Over-furnished short text. An ad-hoc message must not be structured like a document. No headings when the text is two paragraphs. No closing section when the text naturally ends with its last concrete statement.

Wrong address register. Direct second-person to an unknown business recipient who expects formal address; or formal tone to a private person who would have expected direct address. `general` must match relationship and context — ask when it is not clear which is right.

Invented content beyond the brief. Same principle as in report: the agent does not add information, actions, conclusions, or opinions that are not in the source material or requested in the brief. Empty calories in an email are worse than brevity.

Falling back to `general` instead of the correct content type. Do not fall back to `general` when the material is clearly an article, case study, or report just because the explicit trigger word was missing. If the material shows clear genre — ask the user which type they want.

## Trigger keywords

Triggers: allmän text, general text, mejl, email, e-mail, brev, letter, PM, promemoria, memo, memorandum.

The lean trigger principle applies. Idiosyncratic Swedish terms (*mejl*, *PM*, *promemoria*) are listed explicitly. Compounds and conjugations (*skriv en text*, *skriv ett mejl*, *skriv ett PM*, *skriv ett brev*, *skriv en sammanfattning*, *write an email*, *write a letter*, *write a memo*, *write a summary*, *plain text*, *vanlig text*) are handled by the agent's semantic matching. Edit/proofread equivalents (*redigera den här texten*, *rätta det här mejlet*, *snygga till PM:et*, *edit this text*, *proofread this email*, *polish the memo*) are handled similarly.

Does not trigger: when any other content type's triggers fire (article, case-study, press-release, web-copy, teaser, report, column, opinion). *Write an analysis* or *skriv en analys* without *rapport*/*report* — ask instead.
