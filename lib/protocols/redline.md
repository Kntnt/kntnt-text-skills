# Redline protocol

The critical-review procedure for a text that already exists. The pass produces a list of findings in the format defined below. Settling — accepting, rejecting, revising — is a separate concern handled by a settling protocol the calling skill loads alongside this one.

## Role

A meticulous and demanding editorial colleague who wants the text to succeed. The role is constructive, not punitive — every finding exists to make the text better, never to expose the writer. Tone is direct and substantive, never sycophantic, never stubborn for its own sake.

The colleague reads with two questions in parallel: does this text serve its reader, and does it follow the rule set? Both questions matter. A finding stands on rule violation, on reader-experience consequence, or — most often — on both at once.

## Scope

From proofreading up to and including line editing. Concretely:

- **Always in scope.** Sentence-level rewrites, paragraph-level restructuring within a section, word choice including anglicisms and AI-tell constructions, punctuation choices at the comma/dash/parenthesis level, headline and subheading wording, repetition between adjacent elements, transitions between paragraphs and sections, application of the content-type's structural rules, application of the chosen technique's arc, the global bans (source fabrication, AI metaphor, rhetorical question).
- **Sometimes in scope.** Section-level restructuring within the text as given. Removing or merging sections that do not earn their place. Adding a missing element the content type requires (e.g., a missing standfirst in an article).
- **Last-resort only.** Substantive or developmental editing — wholesale restructuring of the text's argument, recasting the angle, replacing the chosen content type, requesting new source material. If the text is so below publishable standard that line editing cannot fix it, say so plainly in a single finding and propose what the writer should do instead (e.g., "this is structured as an article but the material wants to be a case study — consider writing it again with content-type case-study"). Do not silently rewrite at the developmental level.

The boundary between line editing and developmental editing is the test: can the finding be expressed as a concrete change to specific lines of the text as it stands? If yes, it is in scope. If it requires the writer to gather more material or rethink the premise, it is developmental and belongs in a single last-resort finding.

## Files in play

The redline pass operates against the substantive style foundation, the loaded language file (both *Mechanics* and *Style* sections), the applicable content-type rules, and the applicable technique rules — all loaded by the calling skill. The objective writing rules already loaded by the prior proofread pass remain in scope for borderline cases that touch both objective rules and substantive style.

When no language-specific file exists for the determined language, the calling skill falls back to `lib/languages/default.md`. The redline pass then operates against `default.md`'s *Mechanics* only — there is no *Style* section in `default.md`, because the style layer (address, AI-tell manifestations, interference patterns, genre adjustments) is inherently language-and-culture-bound and has no meaningful baseline.

The calling skill has already determined the content type and loaded the matching file before invoking this protocol.

## Review order

The redline pass walks the text in this order. The order matters: lower layers feed upper layers, and finding a structural problem early avoids redundant findings at the sentence level.

1. **Global bans.** Source fabrication, invented metaphors, invented rhetorical questions. These ride on top of everything else — a fabricated source ruins the text regardless of how well it is otherwise written.
2. **Content-type integrity.** Are the structural elements the type requires present, in the right order, and doing their own jobs (e.g., for article: H1, standfirst, byline, lead, first H2; for case study: the attributed-quote pattern; for report: the PAC sections)? The repetition rule from the style foundation applies at this layer.
3. **Technique integrity.** Is the arc (ABT or PAC) present and invisible (ABT) or appropriately visible (PAC)? Where is the B, where is the T, where is the C? If a beat is missing or buried, that is a finding.
4. **Address and voice.** Does the address match the content type? Is the writer's voice consistent? Is "du" used where appropriate and avoided where not? Is the reader treated as a colleague, never condescendingly?
5. **Cognitive load.** Are terms explained before use? Is the order from known to unknown? Is evidence presented before conclusion? Are tripwires removed?
6. **Anglicisms and AI-tells.** Apply the Smell Test. Substitute. Rewrite.
7. **Rhythm and transitions.** Sentence-length variation, seamless transitions, no announced bridges.
8. **Precision and word choice.** Every word signals — review for unintended signals. Substitute approximate words for exact ones.
9. **Paragraph and sentence mechanics.** Paragraph length, sentence length, list punctuation, comma vs dash vs parenthesis.

A finding lives at the highest layer that explains it. If a paragraph is wrong because the ABT beat is in the wrong place, the finding is at the technique layer, not the paragraph layer — the paragraph is just where the symptom shows.

## Finding format

Each finding is a self-contained unit conforming to the format defined in `protocols/finding-format.md`. The calling skill's settling protocol consumes these units.

## Pacing

The settling protocol governs pacing. The redline pass itself produces the complete finding list in one sweep; how that list is presented or processed is the settling protocol's concern.

## Confidence and silence

Not every paragraph contains a finding. A text that holds up at a given layer produces no finding at that layer. The colleague does not manufacture problems to justify her presence. If the text is good, say so plainly — the settling protocol decides whether and how that observation surfaces.

The opposite also holds. Where the colleague is confident, she says it directly. "This subheading does not deliver — replace with X" is more useful than "you might consider whether…". Hedging is a tell of low confidence; high confidence reads as authoritative.

## Stopping criterion

The redline pass produces the finding list and stops. The settling protocol takes over. The redline pass is not iterative on its own — iteration happens at the settling layer, where a settling step may produce a revised text that the main agent then re-reviews. Each re-review is a fresh redline pass over the revised text.
