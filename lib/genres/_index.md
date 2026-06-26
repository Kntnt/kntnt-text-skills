# Genre index

Static index of every genre file in `lib/genres/`. One block per genre, carrying the fields needed for trigger matching: `name`, `swedish_term`, `default_technique`, `default` (where set), `triggers` and – where present – `not_triggers` and `disambiguation`.

Match a user's prompt against this file directly. Do not read each genre file in full to compare. Once the matching genre is decided, read only the corresponding `lib/genres/<name>.md` file for the full rules.

When no trigger matches and no semantic likeness lands clearly, fall back to the genre whose block carries `default: true`.

When adding, renaming or removing a genre file, update this index to match. The plugin does not regenerate it automatically.

---

## article

- name: `article`
- swedish_term: `artikel`
- default_technique: `abt`
- triggers:
  - `artikel`
  - `article`
  - `reportage`
- not_triggers:
  - `'report' or 'rapport' as the first word of a quoted working title (reportage from a conference, etc.)`
- disambiguation:
  - `blogginlägg`: ask article-or-column
  - `blog_post`: ask article-or-column
  - `skriv för bloggen`: ask article-or-column
  - `write for the blog`: ask article-or-column

---

## case-study

- name: `case-study`
- swedish_term: `kundcase`
- default_technique: `abt`
- triggers:
  - `kundcase`
  - `case`
  - `case study`
  - `kundreferens`
  - `referenscase`

---

## column

- name: `column`
- swedish_term: `krönika`
- default_technique: `abt`
- triggers:
  - `krönika`
  - `column`
  - `kåseri`
  - `personal essay`
- disambiguation:
  - `blogginlägg`: ask article-or-column
  - `blog_post`: ask article-or-column
  - `skriv för bloggen`: ask article-or-column
  - `write for the blog`: ask article-or-column

---

## general

- name: `general`
- swedish_term: `allmän text`
- default_technique: `none`
- default: `true`
- triggers:
  - `allmän text`
  - `general text`
  - `mejl`
  - `email`
  - `e-mail`
  - `brev`
  - `letter`
  - `PM`
  - `promemoria`
  - `memo`
  - `memorandum`

---

## opinion

- name: `opinion`
- swedish_term: `opinionstext`
- default_technique: `abt`
- triggers:
  - `opinionstext`
  - `opinion`
  - `debattartikel`
  - `debattinlägg`
  - `åsiktstext`
  - `op-ed`
  - `opinion piece`
  - `debate article`

---

## press-release

- name: `press-release`
- swedish_term: `pressmeddelande`
- default_technique: `none`
- triggers:
  - `pressmeddelande`
  - `press release`
  - `press-release`

---

## report

- name: `report`
- swedish_term: `rapport`
- default_technique: `pac`
- triggers:
  - `rapport`
  - `report`
  - `whitepaper`
  - `white paper`
  - `vitbok`
- not_triggers:
  - `'rapport' inside a quoted working title for an article (reportage)`
  - `'skriv en analys' / 'write an analysis' without 'rapport'/'report' – too broad`
  - `styrelseprotokoll`
  - `mötesprotokoll`
  - `board minutes`
  - `meeting minutes`

---

## teaser

- name: `teaser`
- swedish_term: `puff`
- default_technique: `abt`
- triggers:
  - `puff`
  - `teaser`
  - `standfirst`
  - `ingress`
  - `meta description`
  - `metabeskrivning`

---

## web-copy

- name: `web-copy`
- swedish_term: `webbcopy`
- default_technique: `abt`
- triggers:
  - `webbcopy`
  - `web copy`
  - `webbtext`
  - `web text`
