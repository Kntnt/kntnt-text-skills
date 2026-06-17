<!--
Synthetic transcript fixture for the /eval capture command (issue #45).

A fabricated mini /edit session with planted maintainer feedback. It is NOT a
real session; it exists only so the capture tool can be unit-verified against a
known set of faults and a known before/after diff. Names here (Anna Lindqvist,
Volvo, Spotify) are deliberate so the anonymiser has something to scrub.

The format is the wire the capture tool reads: a frontmatter-style header
naming the skill, language and invoked prompt, then the agent's run, then the
maintainer's running feedback (the primary fault source, one quoted remark per
bullet), then the before/after diff (the corroborating evidence).
-->
skill: edit
language: sv
prompt: /edit sv

# Session

Maintainer invoked `/edit sv` on a short Swedish marketing paragraph. The agent
ran its three phases and returned a polished draft. The maintainer then gave
running feedback on what the pass missed.

## Maintainer feedback

- "Du missade *adressera* — det är en anglicism, byt till *ta upp* eller *behandla*."
- "*leverera värde* ska bli *ge värde*; *leverera* metaforiskt är en anglicism."
- "Tusentalsavgränsaren *1,234,567* måste bli *1 234 567* med tunt mellanslag."
- "*Marx's teorier* ska vara *Marx teorier* — apostrof-s är engelsk interferens."
- "Bra att du behöll citattecknen som ”…” — inga ändringar där behövs."

## Diff

```diff
- Vi vill adressera era behov och leverera värde till 1,234,567 kunder.
+ Vi vill ta upp era behov och ge värde till 1 234 567 kunder.
- Anna Lindqvist på Volvo citerade Marx's teorier i sin Spotify-podd.
+ Anna Lindqvist på Volvo citerade Marx teorier i sin Spotify-podd.
```
