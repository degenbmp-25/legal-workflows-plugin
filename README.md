# Legal Workflows — OpenAI / ChatGPT plugin

A skills-only plugin packaging 32 jurisdiction-neutral legal document workflows:
structured review of NDAs, MSAs, DPAs, credit and guarantee agreements, commercial
leases, shareholder and limited-partnership agreements, employment agreements, BPO
and design-partner agreements, SPAs, supply agreements, and e-discovery sets;
redline-to-position analysis; issues-list and CP-checklist drafting; key-term
extraction; proofreading; and 11 tabular workflows that extract agreement terms
into a Markdown table.

## Install

The submission package is `dist/legal-workflows-plugin.zip`. Its root contains
`plugin.json`.

To build it from source:

```bash
bash scripts/package-plugin.sh
```

## What it is

Instructions and templates. When you ask it to review a document, the assistant in
your conversation reads the text you pasted and follows the relevant workflow.

- No MCP server
- No account
- No storage, no telemetry, no analytics
- No file upload — paste the document text into the conversation

## Boundaries

This is a work-product tool, not legal advice. The plugin does not practise law, does
not give jurisdiction-specific legal advice, does not file or serve anything, cannot
sign, does not track deadlines, does not retain documents, and does not replace
qualified counsel.

The workflows are jurisdiction-neutral. You supply the governing law.

Output is a structured draft to take to a lawyer. Read every issue against the source
document before relying on it — a model can be confidently wrong.

## Layout

```
plugin/plugin.json               portable Agent Plugins manifest
plugin/.codex-plugin/plugin.json Codex compatibility manifest
plugin/skills/                  32 upstream workflows + skills/setup/SKILL.md
plugin/assets/                  listing icons
plugin/LICENSE                  upstream MIT licence, reproduced verbatim
plugin/ATTRIBUTION.md           upstream provenance and redistribution terms
legal/privacy-policy.md         privacy policy
legal/terms-of-service.md       terms of service
scripts/package-plugin.sh       builds the submission ZIP
scripts/build_codex_manifest.py generates the Codex manifest from the portable one
scripts/patch_descriptions.py   gives each workflow a distinct trigger description
```

## Upstream

The 32 workflow directories under `skills/` come from
[Open-Legal-Products/mike-workflows](https://github.com/Open-Legal-Products/mike-workflows)
(MIT, Copyright (c) 2026 Mike). Every workflow body, template, and column
definition is byte-identical to upstream. The one exception is the
`description:` frontmatter field of 25 workflows, which was rewritten so each
skill states when it should trigger — upstream generates ten of the tabular
workflows from one template, and ten skills that describe themselves identically
cannot be told apart by auto-selection. See `ATTRIBUTION.md` for the upstream
commit, the exact list of changed files, and the excluded jurisdiction-specific
packs.

Jurisdiction-specific upstream packs are not included: the Finnish, Polish, German,
Australian, Singapore, PIPL, EU AI governance, EU GDPR, United States litigation, and
legal verification packs.

`skills/setup/SKILL.md`, both manifests, the files under `assets/`, the legal
documents, and the packaging scripts are original to this distribution.

## Licence

MIT. See `LICENSE`.
