---
name: readme-github
swedish_term: "README för GitHub"
default_technique: none
triggers:
  - "readme.md"
  - "readme for github"
  - "github readme"
not_triggers:
  - "bare 'readme' / 'readme file' / 'readme-fil' without 'github' or a '.md' filename – too broad; ask instead"
---

# README for GitHub

## Purpose

A `README.md` is the front page of a GitHub repository – the first, and often the only, document a visitor reads before deciding whether the project is worth their time. GitHub renders it directly on the repository landing page, so it carries orientation, persuasion and instruction at once. It is documentation, not marketing copy: the reader has come to evaluate and use a piece of software, not to be sold to.

The README serves three audiences, and they arrive in a fixed order of commitment.

- **Users** want a solution to a problem. They do not care about extensibility or about contributing. They want to know whether this project solves their problem and, once they are convinced it does, how to install it, configure it and use it – nothing more.
- **Extenders** are users who additionally want to bend the project to their own needs: through built-in extension mechanisms (hooks, events, filters), through advanced configuration beyond what an ordinary user touches or by integrating the project with other systems. Beyond what a user needs, they need documentation of those mechanisms.
- **Contributors** are extenders who additionally want to give their time and knowledge back to the project – through issues and pull requests, translations and documentation or project stewardship. They need to know how.

The document is laid out so each audience finds what it needs and can stop reading where its interest ends. A user never has to scroll past contributor instructions to reach the installation steps; a contributor finds the deeper material lower down, where the user has already left. This audience layering – Users, then Extenders, then Contributors – is the organising principle of the whole document, and every structural decision serves it.

## Stylistic nuance

<!-- scope: write -->
### Audience layering

The section order runs from the least committed audience to the most committed, so each reader can stop where their interest ends:

- **Users** are served by everything from the opening paragraph down to *Questions, bugs, and feature requests*: the description, the feature list, the problem-and-solution framing, requirements, installation, usage and the FAQ.
- **Extenders** are served by *Extending*, the first section that addresses readers who want more than ordinary use.
- **Contributors** are served by *Development* and *How you can contribute*.
- The closing sections – *Acknowledgements*, *License*, *Changelog* – serve everyone and end the document.

Never invert this order. Contributor and extender material placed above the user's installation and usage instructions forces the largest audience to wade through what it does not need.

<!-- scope: write -->
### Document structure

The canonical section order. Headings are given in their literal form; optional sections are marked as such and are included only when the project warrants them.

1. **`# <repository name>`** – the H1, the repository's name, exactly once.
2. **Badges** – a short row of shields.io badges summarising, at a glance, what a reader needs in order to decide whether to use the project: licence, runtime or platform requirements (e.g. minimum PHP and WordPress versions) and the latest release; optionally a CI or build status. One badge per concern, never one per dependency – the full dependency list belongs in `composer.json` / `package.json`.
3. **Opening paragraph** – one short paragraph stating the repository's purpose, so a visitor can decide within seconds whether the project is for them.
4. **`## Description`** – a couple of paragraphs giving a concise, high-level account of what the repository is for and whom it serves.
   - **`### Key Features`** – a list of three to twelve points naming the most important features.
   - **`### The problem`** – a plain, concrete statement of the problem the code addresses.
   - **`### How this <plugin|library|api|…> helps`** – a plain statement of how the code addresses that problem. The noun in the heading names the actual artefact.
   - **`### Limitations`** *(optional)* – an honest account of where the solution stops.
5. **`## Requirements`** – the list of requirements. Optionally a short note on installing non-trivial dependencies (tools that are not installed automatically).
6. **`## Installation`** – the simplest route to download and install the part of the repository a user wants. This may be `npm` or `composer`, or downloading a release ZIP at `https://github.com/<owner>/<repo>/releases/latest/download/<repo>.zip`. Present a numbered list once there are more than two steps. One-time setup that never needs revisiting – adding an API key to a config file, for instance – belongs here.
7. **`## Usage`** – everything a user needs to make full use of what they installed: configuration not already covered above, settings and how to update to the latest release. Split into `H3` subsections when complexity warrants.
8. **`## Frequently asked questions (FAQ)`** *(optional)* – a reasonable number of reasonable questions a user might still have after reading the above, each as an `H4` heading with a concise answer beneath. Phrase the questions as plainly as possible; keep the answers short and to the point.
9. **`## Questions, bugs, and feature requests`** – where a reader turns when the documentation did not answer them. Points to Discussions for usage questions, and to Issues for bugs and feature requests, with a note to search existing issues first to avoid duplicates. This section is fixed boilerplate – emit the exact wording in *Fixed wording* below, substituting only `<owner>` and `<repo>`.
10. **`## Extending`** *(optional)* – the first section for extenders. Documents every supported way to influence how the code runs, beyond ordinary use: hooks, events, filters, integration points, subclassing and similar mechanisms an advanced user – but not an ordinary one – would reach for. This section can grow very long; give each construct its own `H3` subsection.
11. **`## Development`** – the first section for contributors.
    - **`### Build from source`** – how to clone the repository and build it.
    - **`### Build a release artefact`** *(optional)* – how to build a distributable artefact, e.g. a ZIP.
    - **`### Run tests`** *(optional)* – the kinds of tests (unit, smoke, end-to-end) and how to write and run them.
    - **`### Technical documentation`** – together with the documents under `docs/`, the full technical record: code, file structure, architecture, coding standards, known pitfalls. For a non-trivial repository, keep as little here as possible and push as much as possible into `docs/`.
12. **`## How you can contribute`** – a short, welcoming invitation. Explains that contributions can be small or large: opening an issue to report a bug or request a feature, submitting a pull request, contributing localisation (l10n) or documentation or joining the project's community. References `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md` and `SECURITY.md` where they exist.
13. **`## Acknowledgements`** *(optional)* – a courtesy thank-you to the libraries, tools, prior art and people behind the project. Licence-required attribution goes in `NOTICE`, not here.
14. **`## License`** – points to `LICENSE.md` and, where applicable, `NOTICE.md`.
15. **`## Changelog`** – points to `CHANGELOG.md`, followed by the fixed boilerplate line naming Keep a Changelog and Semantic Versioning (see *Fixed wording* below).

### Fixed wording

Two sections are boilerplate: their wording is constant across every repository, and only the `<owner>` and `<repo>` values are substituted. Emit them exactly as written below – do not paraphrase, reformat or turn the prose into a list.

*Questions, bugs, and feature requests* – the section body is, verbatim:

```
Have a usage question or something to discuss? Please use [Discussions](https://github.com/<owner>/<repo>/discussions).

Found a bug or want to request a feature? Please [open an issue](https://github.com/<owner>/<repo>/issues). Search the existing issues first to avoid duplicates.
```

*Changelog* – after a one-line pointer to `CHANGELOG.md`, the section carries this sentence, verbatim:

```
The project follows [Keep a Changelog](https://keepachangelog.com/) and [Semantic Versioning](https://semver.org/).
```

<!-- scope: write -->
### Register and prose

The register is technical documentation: plain, direct, instructional. Direct second person to the user is natural and expected here – *install the plugin*, *you can configure this in…* – unlike in the more impersonal genres. Instructions are written in the imperative. Commands, code, paths, filenames and option names are set in backticks or fenced code blocks, with a language hint on the fence where it helps rendering.

Prose is scannable. A reader skims headings and code blocks before reading any paragraph in full, so each section must declare its contents in its heading and get to the point in its first sentence. GitHub-Flavoured Markdown affordances – tables for genuinely comparative information, callouts (`> [!NOTE]`, `> [!WARNING]`) for true asides, collapsible `<details>` blocks for long optional material – are used where they carry information, never as decoration.

<!-- scope: write -->
### Headings

`H1` is the repository name and appears exactly once, at the very top. `H2` carries each top-level section. `H3` carries subsections (the *Description* sub-parts, *Usage* subsections, each *Extending* construct, the *Development* sub-parts). `H4` is reserved for individual FAQ questions. Headings are descriptive content declarations, not teasers.

<!-- scope: write -->
### Project specifics and placeholders

Wherever the structure references a project-specific value – `<owner>`, `<repo>`, the artefact noun in *How this `<plugin|library|api|…>` helps* – substitute the real value when it is known. The angle-bracket placeholder form is a documentation convention, not literal output: it survives into the finished README only for values the author genuinely cannot yet supply. The release-asset URL `https://github.com/<owner>/<repo>/releases/latest/download/<repo>.zip` follows GitHub's own latest-release convention and is filled in with the actual owner and repository names.

<!-- scope: write -->
## Default technique

None. A README is carried by the documentation structure above – the audience layering and the canonical section order – not by a narrative or analytical arc. ABT and PAC are not applied as a structural backbone. If the brief explicitly asks for a narrative hook in the opening paragraph or the *Description*, follow the brief; otherwise the prose stays plain and declarative.

<!-- scope: review -->
## Common pitfalls

Audience order inverted. Contributor or extender material – *Development*, *How you can contribute*, *Extending* – placed above the user's installation and usage instructions. The largest audience is forced to scroll past what it does not need. The order is Users, then Extenders, then Contributors; a section out of that order is a finding.

Sections out of canonical order or missing where the project needs them. A real project's README needs at least an opening orientation, *Description*, *Requirements*, *Installation*, *Usage*, *License* and *Changelog*; software with extension points needs *Extending*; a project that accepts contributions needs *Development* and *How you can contribute*. A present section that sits in the wrong position, or a needed section that is absent, is a finding. *Limitations*, *FAQ*, *Build a release artefact*, *Run tests* and *Acknowledgements* are genuinely optional and their absence is not a fault.

Badge spam. A badge per dependency, or a wall of decorative badges. The badge row summarises what a reader needs to make the use-or-not decision – licence, runtime or platform requirements, latest release, optionally CI status – and nothing more. The dependency list lives in `composer.json` / `package.json`.

Marketing tone. *Revolutionary*, *blazing-fast*, *the best* without concrete substance. A README documents; it lets the capabilities and the feature list speak. Value-laden adjectives without evidence read as noise to a reader evaluating software.

Headings that tease instead of declare. *Getting started the fun way*, cliffhanger subheadings. A reader scanning for the installation steps needs each heading to say plainly what its section contains.

Unsubstituted placeholders in finished output. `<owner>`, `<repo>` or `<plugin|library|api|…>` left literal where the real value is known. The angle-bracket form is for values the author cannot yet supply, not a default to ship.

Boilerplate paraphrased. The *Questions, bugs, and feature requests* body and the *Changelog* Keep-a-Changelog / Semantic-Versioning line are fixed wording (see *Fixed wording*), not free prose. A README that rewords them, reformats them or turns the two sentences into a list has drifted from the canonical text – restore it exactly, substituting only `<owner>` and `<repo>`.

Wrong heading levels. FAQ questions at anything other than `H4`; *Extending* constructs not each given their own `H3`; a second `H1` anywhere below the title. The level scheme is `H1` title, `H2` sections, `H3` subsections, `H4` FAQ questions.

Technical documentation bloated into the README. For a non-trivial repository, architecture and internals dumped into *Technical documentation* instead of the `docs/` directory. Keep as little as possible in the README and as much as possible in `docs/`.

Installation or usage that omits the one-time setup. Configuration a user must perform once – an API key, a settings file – left out of *Installation*, or recurring configuration left out of *Usage*. A user who follows the steps and still cannot run the software has been failed by the document.

## Trigger keywords

Triggers: readme.md, readme for github, github readme.

The lean trigger principle applies. README and GitHub are English-rooted technical terms used in both languages; the canonical English forms are listed, and the agent's semantic matching handles variants and compounds in either language (*github-readme*, *readme för github*, *write a readme for my github repo*, *skriv en readme för mitt github-repo*, *en README-fil till GitHub*).

Does not trigger on the bare word *readme* / *readme file* / *readme-fil* on its own, without *github* or a `.md` filename – too broad, since a README may be destined for a package registry, a GitLab project or an internal tool with different conventions. When the platform is unstated, ask rather than assume GitHub.
