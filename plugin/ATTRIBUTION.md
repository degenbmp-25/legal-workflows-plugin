# Attribution

This plugin package redistributes legal workflow definitions from an upstream open-source project. The upstream workflows are included **unmodified**.

## Upstream project

- **Repository:** https://github.com/Open-Legal-Products/mike-workflows
- **Upstream commit mirrored:** `20bed204ce9ef07e1bc2df0b16b35ee8ad997fb1` (upstream `main`, 2026-10-20)
- **Upstream license:** MIT
- **Upstream copyright:** Copyright (c) 2026 Mike
- **Mirror date:** 2026-08-11 (initial mirror), refreshed 2026-10-28 with the upstream workflows that landed on 2026-10-20

The full upstream MIT license text is reproduced verbatim in [`LICENSE`](./LICENSE) and ships in this package.

## What was redistributed

32 upstream workflow directories, each copied byte-for-byte from the upstream repository with no edits, rewrites, renames, or reformatting:

- 21 assistant workflows (review, drafting, comparison, redline analysis, issues lists, checklists, key-term extraction, proofreading)
- 11 tabular review workflows (structured column extraction)

Each workflow's `SKILL.md` declares `license: MIT` in its frontmatter. Upstream provides no separate `NOTICE` file.

Every file in `skills/` other than `skills/setup/SKILL.md` is upstream content, byte-identical to upstream. `skills/setup/SKILL.md`, `plugin.json`, and the files under `assets/` are packaging authored by HiveMind Intelligence for this distribution and are not upstream content.

## What is not included

Upstream jurisdiction-specific packs are excluded from this package and are not redistributed here: the Finnish law pack, the German liquidity planning pack, the Polish law pack, the Australian and Singapore digital regulation packs, the PIPL pack, the EU AI governance pack, the EU GDPR pack, the United States litigation workflows, and the legal verification pack.

## Redistribution terms

The upstream MIT license permits redistribution provided the copyright notice and permission notice accompany the material. That notice is in `LICENSE` at the root of this package. No upstream workflow file was modified; the workflows are redistributed as-is, with no additional restrictions applied.

## Publisher

Packaged and published by HiveMind Intelligence — https://hivemindintelligence.com
