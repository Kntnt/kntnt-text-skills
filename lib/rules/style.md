# General style

The substantive style foundation: word choice, voice, structure, the global bans and the technique-orientation that shapes the writing. This is what a critical editorial pass applies against, on top of the objective writing rules and the loaded language file. Language-specific manifestations of these principles – calque lists, anglicism substitutions, pronoun systems – live in the language file.

## The organising principle

The plugin's writing reflects a genuine intent to convey knowledge and help the reader. Every rule below serves that intent. When two rules collide, the one that better serves the reader's understanding wins.

The text gives the reader the experience of being on an intellectual adventure where the writer with a sure hand leads from starting point to destination. The reader should feel cared for – right information at the right moment, objections anticipated, no loose ends. But that care must never be visible explicitly. It shows through the text's structure and flow, not through the writer saying *I am thinking of you*.

**Never write condescendingly about the reader – not even implicitly.** Start from the reader's natural impulse, show why it leads astray and give the alternative. Never *you are doing it wrong*, always *this is how it gets better*. Constructions that point fingers (*there is a pattern in the industry…*), imply problems (*the problem is not that you lack ambition…*) or wag a finger (*make sure to…*) are consistently turned into constructive constructions.

## Repetition rule

Every element in a text must have its own job. This applies throughout – not just to the opening. If a bridge and an attributed quote say the same thing, strike one. If a paragraph and a subheading express the same point, rewrite. Specifically for the opening: when the title, standfirst, lead and first H2 section are read in sequence, the reader must never feel the same thing is being repeated. Each part has its own distinct job. Rule of thumb: if you can strike the title, standfirst or lead without the reader missing any new information, you have repeated yourself.

Content-type files with distinct element structures (article, case study) refer back to this rule for their specific elements.

## Techniques

Structural techniques carry the text. The two installed initially are ABT (And, But, Therefore – narrative arc) and PAC (Premise, Analysis, Conclusion – analytical arc). See `lib/techniques/abt.md` and `lib/techniques/pac.md` for the full descriptions and examples. Each content-type file names its default technique.

The technique should be invisible to the reader. If the text feels as if it is following a pattern, the technique has failed.

When the user names a technique that has no corresponding file in `lib/techniques/`, do not apply it from training data. Either use an installed technique, add the file first or proceed without a technique.

## Reducing cognitive load

Minimise the reader's cognitive load. This is about removing friction – not about adding explanations.

**Mental tripwires** are anything that makes the reader start thinking about something other than what she is reading. The most common example: a term used before it has been explained. Tripwires must be eliminated.

In concrete terms:

- Explain terms before they are used in reasoning. Specialist terms may be used but must be explained at first occurrence unless generally established.
- Present things in the order that builds on what the reader already knows. Avoid unanswered questions that are answered later.
- Sort enumerations logically (small to large, simple to complex, chronological – whatever fits the context).
- When alternatives are presented in a progression (e.g., from own responsibility to full service, or from simple to complex), hold the direction. Returning to an earlier alternative after moving on creates a loop that increases cognitive load.
- Each new point should follow logically from the previous.
- Give concrete examples before abstract principles when possible.
- Use everyday words rather than jargon. Not to simplify, but to reduce unnecessary load.
- **Evidence before conclusion, not the other way round.** If the text is to lead the reader to a conclusion, present first the material that makes the conclusion inevitable. A conclusion that comes before the evidence forces the reader to trust the writer – that is a tripwire because the reader cannot assess the claim and must choose between trusting blindly or questioning. A conclusion that comes after the evidence lets the reader reach it herself. The second variant is stronger – and the only one that works in texts published by a party with self-interest (e.g., a supplier's knowledge magazine). This means, for example, that a checklist of requirements should come after the explanation of what the requirements rest on, and that arguments against a particular behaviour should come after the reader has the material that makes the arguments self-evident.

## Understatement

The hardest principle to get right, and where AI models consistently fail.

The plugin's voice favours measured expression over performative emphasis. Where many writers (and most AI models trained heavily on American English business and marketing prose) would write *This is a game-changer!*, the plugin's text says perhaps nothing at all – but structures the prose so that the reader draws the conclusion herself.

Humour exists as an undertone that never points at itself. The texts contain no jokes – but the reader still gets a feeling that the text is quietly cheerful. Similes and metaphors are used very sparingly and deliberately.

The reader should not experience the text as private or even personal. Yet she should sense that the writer is along on the journey, holding her hand, thinking about her.

**Rule of thumb:** if the text *feels* as though it is trying to be warm, humorous or personal, you have overdone it. Pull back. Let the structure and word choices do the work silently.

## Precision

Approximate wording is not accepted. Three principles:

**Draw the right conclusions from the material.** Analyse what the source material actually says – not what it *almost* says. A different cause means a different implication. If the problem is that the customer gets quotations they cannot compare, do not write that *the process drags on* – that is a different conclusion with different consequences.

**Be exact about what you mean.** Do not use a term unless you know what it means. *Tone dialling* is correct but unnecessary when you can write *press a digit on the keypad*. *Electric locks* and *electric strikes* are not the same thing. Choose the word that actually describes what you mean, not the word that *approximately* describes it.

**Every word signals.** Word choice has consequences beyond its literal meaning. *Sometimes he offers* signals that the person differentiates between customers. *Tailoring the quotation work* signals that it is done for one's own sake rather than the customer's. Review word choices for unintended signals.

## Rhythm and sentence variation

Varying sentence lengths create natural rhythm. Short sentences for emphasis – used sparingly. Sentence fragments and conjunctions as sentence-openers are permitted in column, opinion, web copy and casual sections of article and case study – used for rhythm, not as licence to write loosely. They are not permitted in press release or report, where strict grammar applies.

## Transitions

Aim for seamless transitions. Paragraphs follow naturally from each other without explicit bridges – the logical jump must not be too great. If a seamless transition does not work, write a bridge either at the end of the first paragraph or at the start of the second.

Between sections, larger jumps are tolerated. Common techniques: end a section with a question that the next section answers, or refer back at the start of the next section.

**Avoid at all costs:** (i) paragraphs and sections that feel stacked on top of each other – clumsy and amateurish. (ii) Overused explicit bridges – also amateurish. If the writer needs to write *furthermore* or *moreover*, that is a sign that the structure needs to be redone.

## Address and voice

The text always sounds as if writer and reader are on an adventure together. The feeling that the writer is talking to the reader is always present – even without explicit second-person address.

The pronoun system that realises this – direct second-person, first-person plural inviting the reader, third-person impersonal, when each is appropriate – is language-specific. See the loaded language file for the pronoun realisation. The per-genre guidance below names the *effect* in language-neutral terms.

- **Web copy, article.** Sometimes direct second-person, more often the feeling of address without explicit pronoun (*What is this supposed to be good for?* instead of *You are probably wondering…*). First-person plural can invite the reader (*Let us look more closely at…*).
- **Column and personal articles.** Almost always direct second-person. The writer can be visible without explicit first person. When motivated, first person is used. Language can be freer – sentence fragments, conjunctions as sentence openers, a more direct tone. The writer can use rhetorical repetition as a structural device – the same phrase returning through the text after each argument, building cumulative effect. This technique is used only in opinion-driven texts – never in fact-based articles or press releases.
- **Reports, e-book chapters.** Second-person does not appear. First-person plural is more prominent – author and reader are on a journey together.
- **Case study.** The writer is almost invisible. The interviewees carry the narrative through long, authentic quotes. The writer contributes structure and context.
- **Press release.** No second-person at all. Neutral, journalistic tone. Should be publishable straight into a newspaper.

## Pedagogy

- Often begin with historical or theoretical context before practical application.
- Explain *why* before *how*.
- Integrate practical tools, models and matrices the reader can use.
- Use concrete examples and case studies.
- Build systematically from broad context to specific application.
- Combine theory and practice.
- Support claims with source references. Never invent facts or sources.

## Narrative technique

Standard approach: direct, clear, fact-based pedagogy. Dramaturgical elements only when they genuinely make the text better:

- Rhetorical questions: sparingly, only for pedagogical value (see the rhetorical question rule below).
- Analogies: sparingly, only when they simplify understanding – not just entertain.
- Cultural references: very sparingly. Most texts need none.
- Scenographic elements and dramatic tension: avoid in most cases.

## Attributed quotes in articles

If an article contains interviewees, choose one of two modes – nothing in between:

- **Carrying voices.** The interviewees drive the narrative. The reader gets to know them. The article is built around quotes, with running text providing structure and context. Each section other than opening and closing should have a quote.
- **No quotes at all.** The article is carried entirely by the writer's voice.

The half-measure – a couple of attributed quotes as garnish while the rest is *Martin maintains that…* – does not work. If quotes are introduced, make them the text's backbone.

Attributed quotes should sound like speech, not summaries. No one speaks in bullet lists. Keep attributed quotes short and pointed and let the running text take the examples and details. The bridge before an attributed quote and the quote itself must never say the same thing: if the bridge states *what*, the quote should explain *why* or *how*.

Review each quote from the reader's perspective. Ask: what does this quote signal about the quoted person? An interviewee who describes a customer-friendly action can – through an unfortunate phrasing – come across as lazy, calculating or uninterested. The reader has no access to the full interview and judges the person solely on the quote. If the quote risks giving the wrong impression, rewrite the bridge so the context is clear, or choose a different part of the interview.

The typographic realisation of attribution – quotation marks vs. speech dash – is set by the loaded language file.

## Tone adapts to content

- Technical / pedagogical articles (most common): professional, direct, minimal dramaturgy.
- Societal perspective / future vision (uncommon): more narrative, analogies and historical perspectives can add value.
- News / updates: concise, fact-based, to the point.

## AI-tell constructions (Smell Test)

Avoid constructions that reveal AI authorship. A single sentence that reads like an AI fingerprint can ruin a whole text's credibility.

The principle is universal; the specific manifestations are language-specific. The loaded language file lists the calques and tics that commonly betray AI authorship in that language. Apply the language file's Smell Test on every sentence: *would a writer at a leading editorial outlet in this language write this?*

## Interference from the model's training-dominant language

AI models are trained disproportionately on American English. When writing in another language, the model's prose can carry the syntactic and lexical fingerprint of its training data – calques, anglicisms, idioms that read as imported. When writing in non-American English varieties, similar interference from American constructions can creep in.

The principle is universal; the specific substitution lists are language-specific. The loaded language file lists the common interference patterns in that language and the preferred local substitutions. Apply them deliberately.

## Source fabrication ban (global rule)

Every source cited in a text – book, article, study, author, interview subject, dataset, statistic with attribution – must exist and must be verified before use. The only exception is when the user explicitly requests a fictional source (for instance a hypothetical interview subject as part of a thought experiment). In that case the decision belongs to the user, not the agent's initiative.

This applies to all content types without exception. A fabricated source ruins the credibility of the entire text, and once published, the consequences are not recoverable.

## AI metaphor ban (global rule)

Do not invent metaphors. If a metaphor exists in the source material or brief, use and deepen it by staying with that one metaphor. AI-generated metaphors are typically flat and undermine the text – they read as decorative rather than illuminating, and they expose the writer as not having lived inside the subject matter.

When source material offers one metaphor, use it consistently throughout the text rather than introducing variants or competing metaphors. A single metaphor developed across a piece carries authority; a string of unrelated metaphors signals padding.

## Rhetorical question rule

Do not invent rhetorical questions. If they appear in the source material, they can be kept and improved. Otherwise they are not introduced. The rule is strict in reports; looser in column and opinion (where rhetorical address is part of the genre) but still no fabrication as filler.
