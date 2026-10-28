# Attribution

This plugin package redistributes legal workflow definitions from an upstream open-source project. The workflow bodies are included unmodified; the `description` frontmatter field of 25 workflows has been rewritten, as documented below.

## Upstream project

- **Repository:** https://github.com/Open-Legal-Products/mike-workflows
- **Upstream commit mirrored:** `20bed204ce9ef07e1bc2df0b16b35ee8ad997fb1` (upstream `main`, 2026-10-20)
- **Upstream license:** MIT
- **Upstream copyright:** Copyright (c) 2026 Mike
- **Mirror date:** 2026-08-11 (initial mirror), refreshed 2026-10-28 with the upstream workflows that landed on 2026-10-20

The full upstream MIT license text is reproduced verbatim in [`LICENSE`](./LICENSE) and ships in this package.

## What was redistributed

32 upstream workflow directories:

- 21 assistant workflows (review, drafting, comparison, redline analysis, issues lists, checklists, key-term extraction, proofreading)
- 11 tabular review workflows (structured column extraction)

Each workflow's `SKILL.md` declares `license: MIT` in its frontmatter. Upstream provides no separate `NOTICE` file.

## What was changed, and why

The only modification to upstream content is the `description:` field in the YAML frontmatter of 25 `SKILL.md` files. **No workflow body, instruction, template, YAML schema, or table-column definition was changed.** Every one of those files remains byte-identical to upstream apart from the single `description` line, which this project verified file by file after applying the change.

### Why the descriptions were rewritten

Upstream generates the eleven tabular workflows from a shared template, so ten of them ship with a byte-identical description:

> Use this workflow to review uploaded documents and extract structured information into the tabular review columns defined in table-columns.yaml.

The `description` is the auto-load surface for a skills-only plugin: it is what a model reads when deciding which workflow to run. Ten workflows that describe themselves identically are ten workflows the model cannot tell apart, so a request to extract credit agreement terms could load the supply agreement workflow instead. Upstream's own per-workflow `table-columns.yaml` files differ in exactly the places where these workflows differ, and the rewritten descriptions name those columns.

The 25 rewritten workflows are the ten templated tabular workflows, `change-of-control-tabular-review` (whose upstream description was unique but carried no trigger phrase), and 14 assistant workflows whose descriptions named the task but did not state when the skill should trigger. The rewritten descriptions name the workflow, state what it extracts or reviews, and point at the neighbouring workflow where two skills cover overlapping subject matter.

The remaining seven upstream workflows (`deal-redux`, `msa-draft`, `msa-review`, `dpa-draft`, `dpa-review`, `design-partner-draft`, `design-partner-review`) already carried explicit trigger phrases and are shipped byte-identical to upstream.

### Provenance

`skills/setup/SKILL.md`, `plugin.json`, the files under `assets/`, and `.codex-plugin/plugin.json` are packaging authored by HiveMind Intelligence for this distribution and are not upstream content. The same is true of the `LICENSE` and this `ATTRIBUTION.md` file.

## What is not included

Upstream jurisdiction-specific packs are excluded from this package and are not redistributed here: the Finnish law pack, the German liquidity planning pack, the Polish law pack, the Australian and Singapore digital regulation packs, the PIPL pack, the EU AI governance pack, the EU GDPR pack, the United States litigation workflows, and the legal verification pack.

## Redistribution terms

The upstream MIT license permits redistribution and modification of the material provided the copyright notice and permission notice accompany it. That notice is in `LICENSE` at the root of this package. The modifications described above are limited to workflow description metadata; the substantive legal content is redistributed as-is, with no additional restrictions applied.
