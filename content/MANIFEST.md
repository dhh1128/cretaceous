# Content manifest

One file per scene, named `BB.S.md` where `BB` is the zero-padded beat and `S` the scene within it, matching `plan/scene-list-v4.md`. Zero-padding keeps beats 10–15 sorting after 09.

## `superseded/` — NOT canon, NOT a style exemplar

**Status changed 2026-09-09.** These ten scenes were previously treated as canon and as the style exemplar set. Both were wrong.

They are **edited AI drafts, not Daniel's composition** — the git history is a sequence of *improved*, *revised*, *wordsmithing*, *apply rule to ch 4* passes over generated text. And measured against his actual novels they are not close:

| | these scenes | viking | cordimancy |
|---|---|---|---|
| mean sentence | **7.7** | 11.2 | 11.0 |
| median | **6** | 9 | 9 |
| ≤5 words | **43%** | 26% | — |
| ≥30 words | **0.4%** | 2.8% | 2.2% |

Over-corrected into staccato — the exact failure `writing-style-v2.md` warns about, at 43% short sentences where "rare" was the instruction.

**Their worldbuilding has been harvested into the canon docs** (`.ignored/content-harvest.md`) and survives without them. They are retained for reference during redrafting only. **Do not draw voice, rhythm, or scene boundaries from them.**

Two contradictions found between these scenes, which is the strongest argument against treating them as authoritative: **Alira is two and a half in 01.1 and three weeks old in 02.1**, and the **nests are thirty meters up in 04.1 and fifteen in 02.2**.

### The superseded scenes

Numbering follows the **rescened** Act 1 in `plan/scene-list-v4.md` — 14 scenes, of which four are new and unwritten. Files renumbered 2026-09-07; the old numbers are in the last column.

| file | scene | POV | day | words | was |
|---|---|---|---|---|---|
| `01.1.md` | 1.1 Cold Open — the Vitarium, Alira dies | Teva | 1 eve | 1163 | — |
| *(unwritten)* | **1.2 The death moves outward** | Teva | 1 night | ~600 | new |
| `02.1.md` | 2.1 Keo trains Noli | Keo | 2 dawn | 967 | — |
| `02.2.md` | 2.2 Benal's math, Marek's dismissal | Benal | 2 am | 974 | — |
| *(unwritten)* | **2.3 Keo with Joram and Riel** | Keo | 2 am | ~2000 | new |
| *(unwritten)* | **2.4 Teva with Omya, lucid** | Teva | 2 pm | ~1800 | new |
| `02.5.md` | 2.5 Teva drills the yazhi | Teva | 2 pm | 964 | 2.3 |
| `03.1.md` | 3.1 The Council debate | Keo | 2 eve | 1206 | — |
| *(unwritten)* | **3.2 Marek after the debate** | Benal | 2 eve | ~700 | new |
| `03.3.md` | 3.3 "I'm going." | Keo | 2 night | 888 | 3.2 |
| `03.4.md` | 3.4 Benal insists | Keo | 2 night | 891 | 3.3 |
| `04.1.md` | 4.1 Stealing from his parents | Keo | 2 late | 996 | — |
| `04.2.md` | 4.2 The Repository | Keo | 2 late | 1052 | — |
| `04.3.md` | 4.3 Through the border-tangle | Keo | 2 pre-dawn | 1478 | — |

**10,579 words written across 10 of 14 Act 1 scenes.** Four unwritten, ~5,100 words, which brings Act 1 to roughly 15,800.

**2.3 and 2.4 are the priority.** Keo's parents have never spoken to him on the page and Omya has never spoken to Teva, so the two relationships the novel's emotional arc rests on have never been dramatized. See `plan/pacing-and-stakes.md` §2.

## `rejected/` — labeled negatives, retained per the design's negative-canon

Not canon. Kept because they are failures against a known target, which makes them useful for the AI-tells blacklist. Do not draw worldbuilding or continuity from them.

| file | was | why rejected |
|---|---|---|
| `05.1-draftA.md` | `content/5.md` | scene 5.1, three competing drafts |
| `05.1-draftB.md` | `content/5b.md` | " |
| `05.1-draftC.md` | `prompts/5.md` | " — was misfiled in `prompts/` |
| `ch6-savanna-constrictor.md` | `content/6.md` | POV shifts three times mid-chapter; out of scene-list order |
| `ch7-river-crossing.md` | `content/7.md` | out of scene-list order |
| `ch8-springs-noli-death.md` | `content/8.md` | Noli's death relocated and unearned |

---

## Two findings from doing the split

**1. The drafted chapters 6–8 are in a different order than the scene list, not merely mis-numbered.**

| scene list says | the drafts did |
|---|---|
| 6.1–6.2 river crossing, Day 3 | savanna trek *(6.5–6.6, Day 7)* |
| 6.3–6.4 jungle, constrictor, Days 4–5 | jungle, constrictor |
| 6.5–6.6 savanna trek, Day 7 | river crossing |
| 7.1–7.2 camp at night, Noli taken at dawn | sulfur springs, Noli taken at midday |

So the escalation was reordered in the drafting and nobody noticed. The scene list is the more considered artifact and wins (decision rule 3). Chapter 6's text also says "Four days" where the scene list puts the savanna at Day 7.

This matters beyond tidiness: the scene list's order puts the **first river crossing early**, so that "water is death" is proven to the reader before the stakes climb, and saves the **savanna** for the hubris climax. The drafted order spends the savanna first and lands the river after the constrictor, which flattens both.

**2. The scenes are running about 40% under length.** `writing-style-v2.md` targets ~1,800 words per scene, for 40 scenes and a 70–100k novel. The canon scenes average **1,058**. At that rate the finished book lands near 42k — a middle-grade length, not a YA novel.

That is not a call to pad. It is evidence for the layers that aren't in the plan yet: interiority, the misjudgment evidence, the intimacy beats, humour, and the sensory allocation all take room, and their absence is *why* the scenes are short. The gap between 1,058 and 1,800 is roughly the size of the material the emotional spine needs.
