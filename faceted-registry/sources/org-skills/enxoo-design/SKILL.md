---
name: enxoo-design
description: Use this skill to generate well-branded interfaces and assets for Enxoo, either for production or throwaway prototypes/mocks/etc. Contains essential design guidelines, colors, type, fonts, assets, and token references for prototyping.
user-invocable: true
---

Read the README.md file within this skill, and explore the other available files.

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, you can copy assets and read the rules here to become an expert in designing with this brand.

If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts or production code, depending on the need.

## Quick reference

- **Tokens live in** `colors_and_type.css`. Import it and use the CSS variables. Do not redefine values.
- **Only ever use semantic tokens** in real designs. The primitives exist so semantic tokens can be defined.
- **Three typefaces, one voice:** Gabarito (headings), Instrument Serif Italic (one accent word per heading), Inter Tight (body).
- **Two backgrounds:** light `#F2F2FF` and dark `#101070`. Alternate them deliberately to create rhythm. Never mix freely.
- **Pick one radius per document** and apply it uniformly to every card and image crop. Do not mix.
- **All spacing divisible by 8.** No 10, 15, 22, etc.
- **No em dashes** anywhere in the output.
- **No ALL CAPS** anywhere in the system.
- **No drop shadows** as default styling. Use background contrast and color for depth.
- **Emphasis always pairs** Semibold weight with the accent color. Never weight alone.

See `README.md` for full rules, content tone, and visual foundations.
See `preview/` for token specimen cards.
See `slides/` for sample slide layouts using the system.
