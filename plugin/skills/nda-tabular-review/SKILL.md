---
name: "nda-tabular-review"
description: "Use when the user wants a non-disclosure or confidentiality agreement pulled into fixed columns rather than reviewed clause by clause: whether the NDA is mutual or unilateral, how Confidential Information is defined, the receiving party's obligations, which standard carveouts are present, permitted disclosures, term and duration, return and destruction, remedies, and governing law. Extracting these columns from table-columns.yaml. For a clause-by-clause review from the user's perspective, use nda-review instead."
license: "MIT"
metadata:
  version: "1.0.0"
  author: "Open Legal Products"
  language: "English"
  mike-display-name: "NDA Tabular Review"
  mike-type: "tabular"
  mike-availability: "system"
  practice: "General Transactions"
  jurisdictions: "General"
---
# NDA Tabular Review

## Purpose

Use this workflow to review uploaded documents and extract structured information into the tabular review columns defined in `table-columns.yaml`.

## Instructions

- Apply each column prompt in `table-columns.yaml` to each document independently.
- Extract only information supported by the document text.
- Include clause references, section names, dates, amounts, party names, and defined terms where available.
- If responsive information is not found, return an empty value or a concise "Not found" response.
- Keep cell outputs concise while including enough context to make each extracted value useful.
- Do not invent citations, facts, parties, dates, rights, obligations, or financial consequences.
- Render the completed results as an exportable Excel (`.xlsx`) file. If Excel output is not possible, render the results as a Markdown table.