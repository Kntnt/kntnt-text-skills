# Finding format

The shared format for a critical-review finding. A finding is the atomic unit produced by the redline pass and consumed by a settling protocol.

Each finding is a self-contained unit with four parts.

1. **Marking.** A concrete pointer into the text — either a short quote (the offending span as it appears in the text, no longer than necessary to identify it unambiguously) or a structural reference ("the third paragraph under the first H2", "the standfirst", "the closing section"). The recipient must be able to find the location without searching.
2. **Problem.** What is wrong, expressed in one or two sentences, with explicit rule reference where one applies — the relevant section of the loaded style, content-type, technique, writing, or language file. When the finding rests on reader-experience consequence rather than a named rule, name the consequence concretely (*the reader has no way to tell whether the quotation is exact or paraphrased*).
3. **Solution.** A concrete proposal — the rewritten span, the restructured paragraph order, the new headline, the deleted word. The proposal is specific enough that "accept" applies it without further interpretation. If the finding is at a layer where a single concrete rewrite is not possible (e.g., the article needs an in medias res opening that does not yet exist), the solution describes the intended shape with sufficient precision that the writer can produce it.
4. **Prompt.** Form depends on the settling protocol. A user-dialogue settling protocol attaches a short prompt inviting the user to engage with the finding. A subagent-driven settling protocol omits the prompt — the subagent receives the marking, problem, and solution as material to react to.
