---
name: setup
description: "Onboarding guide for the Legal Workflows plugin. Use when the user opens the plugin for the first time, asks what workflows it contains, asks how to paste a document in, or asks what the plugin can and cannot do. Lists the 32 jurisdiction-neutral legal document workflows it ships, explains how to paste documents in, explains the assistant-versus-tabular output difference, and states plainly what the plugin does not do."
license: "MIT"
metadata:
  version: "1.0.0"
  author: "HiveMind Intelligence"
  language: "English"
  mike-display-name: "Legal Workflows Setup"
  mike-type: "assistant"
  mike-availability: "system"
  practice: "General Transactions"
  jurisdictions: "General"
---

# Legal Workflows — Setup

## What this plugin is

**Legal Workflows** is a bundle of 32 legal document workflows for people who work with contracts every day — in-house counsel, paralegals, legal ops, deal teams, and founders who read their own paper.

It does three things:

1. **Reviews** an agreement against a defined issue list and tells you what is off-market, missing, or risky.
2. **Drafts** an agreement or a closing checklist from a template and the facts you supply.
3. **Extracts** structure out of a document — key terms, clause deltas between two versions, or a fixed-column table of terms across a document set.

Every workflow here is a jurisdiction-neutral, general-practice workflow. None of them is specific to Finnish, Polish, German, Australian, Singapore, or US-litigation law.

## How to use it

**Paste the document text straight into the chat.** That is the whole input mechanism. There is no file upload, no document-parsing service, no connected MCP server, and no account to connect. Copy the text out of your document or PDF and paste it in the message, then say which workflow you want.

Two things that make a paste work well:

- **Say which workflow you want** (for example "run the NDA review on this") or describe the task and let the workflow be selected for you.
- **Paste the whole document.** Workflows that check "is this clause missing" can only find a missing clause if the surrounding text is there.

Long documents are fine. If a document is long enough that the beginning is at risk of being dropped, paste it in labelled parts and say "part 1 of 3".

## The 32 workflows

### Assistant workflows (21) — review, drafting, analysis, prose output

**Transactions and commercial**

- `nda-review` — review a non-disclosure agreement
- `msa-review` — review a master services agreement
- `msa-draft` — draft a master services agreement
- `dpa-review` — review a data processing agreement
- `dpa-draft` — draft a data processing agreement
- `bpo-agreement-review` — review a business process outsourcing agreement
- `design-partner-review` — review a design partner agreement
- `design-partner-draft` — draft a design partner agreement

**Finance and credit**

- `credit-agreement-review` — review a credit or facility agreement
- `guarantee-agreement-review` — review a guarantee agreement

**Corporate**

- `corporate-approvals-review` — review corporate approval steps and resolutions
- `shareholder-agreement-review` — review a shareholders' or shareholders' agreement
- `issues-list-draft` — turn review findings into an issues list to send to the other side

**Real estate**

- `commercial-lease-review` — review a commercial lease

**Employment**

- `employment-agreement-review` — review an employment agreement

**Drafting, extraction and quality**

- `draft-from-template` — edit a copy of your own template using instructions and source material
- `cp-checklist-draft` — draft a closing checklist
- `extract-key-terms` — extract the key legal, commercial, and operational terms
- `proofread` — review a document for drafting quality, internal consistency, and mechanical errors
- `compare-documents` — compare two versions of a document clause by clause
- `deal-redux` — reduce a counterparty's tracked-changes redline to the small number of negotiating positions it actually contains

### Tabular review workflows (11) — structured extraction into a table

Each of these reads a document (or a set of documents) and fills a fixed set of columns defined in that workflow's `table-columns.yaml`.

- `nda-tabular-review`
- `commercial-agreement-tabular-review`
- `commercial-lease-tabular-review`
- `credit-agreement-tabular-review`
- `employment-agreement-tabular-review`
- `shareholder-agreement-tabular-review`
- `limited-partnership-agreement-tabular-review`
- `change-of-control-tabular-review`
- `e-discovery-tabular-review`
- `supply-agreement-tabular-review`
- `spa-tabular-review`

**Output format for tabular workflows: a Markdown table.** The upstream workflow definitions describe the output as an Excel export, but this plugin has no script runtime and no code interpreter, so the result renders as a Markdown table in the conversation. That table is what you want to copy into a spreadsheet, a diligence tracker, or a document. To get a real `.xlsx`, paste the Markdown table into Sheets, Excel, or a converter — the plugin itself will not produce a binary spreadsheet file.

## What the output is

The output is a **structured work product** — a review with issues ranked, a draft agreement with tracked positions, a table of extracted terms. It is the kind of document that makes a lawyer's job faster and gives them a better place to start.

It is **not legal advice**, and the plugin is not a law firm.

## What this plugin will not do

Plainly, so there is no surprise later:

- **It does not give legal advice.** It does not tell you what the law requires, what is enforceable, or what you should do about a risk. It tells you what a checklist says about a document.
- **It does not practise law and does not replace counsel.** A qualified lawyer reviews the output and owns the advice. Nothing here substitutes for that.
- **It does not give jurisdiction-specific guidance.** The workflows are general-practice. They do not know your state, country, governing-law clause, regulator, or local drafting convention, and they will not guess.
- **It does not file anything.** No court filing, no registry submission, no service of process, no regulator notification.
- **It does not sign anything.** It cannot execute, e-sign, or bind anyone to anything.
- **It does not track deadlines.** No docket, no renewal calendar, no closing-date reminders, no notifications.
- **It does not retain your documents.** Nothing you paste is stored as a document record, indexed, or made searchable for later retrieval. What persists in the conversation is the conversation.
- **It does not read your files.** No file upload, no parsing service, no MCP server. Paste the text.
- **It does not produce spreadsheets.** Tabular workflows render as Markdown tables, as described above.
- **It does not take payment.** There is nothing to buy inside the plugin.

## A good first request

Try one of these to see the shape of the output:

- "Here is an NDA. Review it and list every clause that is off-market for a balanced paper."
- "Here is a counterparty redline on our MSA with tracked changes. What positions is the redline actually taking?"
- "Here are two versions of a supply agreement. What changed, clause by clause?"
- "Here is a credit agreement. Extract the key commercial terms into a table."

## Where these workflows come from

The 32 workflows are redistributed unmodified from [Open-Legal-Products/mike-workflows](https://github.com/Open-Legal-Products/mike-workflows), MIT licensed, Copyright (c) 2026 Mike. The plugin adds the packaging, the setup guide, and the icons — nothing else. See `ATTRIBUTION.md` and `LICENSE` at the root of this package.

Jurisdiction-specific upstream packs (Finnish law, German liquidity planning, Polish law, Australian digital regulation, Singapore digital regulation, PIPL, EU AI Act, GDPR, and the United States litigation workflows) are **not** included here. If you need one of those, say so and get the right version — do not use a general workflow where a jurisdiction-specific one exists.
