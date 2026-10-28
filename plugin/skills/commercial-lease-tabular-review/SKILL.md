---
name: "commercial-lease-tabular-review"
description: "Use when the user wants a commercial lease pulled into fixed columns: landlord, tenant, guarantor, premises, lease date, term, rent and rent review, service charge, insurance, permitted use, repair and maintenance, alterations, assignment and subletting, break rights, security of tenure, dilapidations, rent deposit, forfeiture and termination, and governing law. Extracting these columns from table-columns.yaml."
license: "MIT"
metadata:
  version: "1.0.0"
  author: "Open Legal Products"
  language: "English"
  mike-display-name: "Commercial Lease Tabular Review"
  mike-type: "tabular"
  mike-availability: "system"
  practice: "Real Estate"
  jurisdictions: "General"
---
# Commercial Lease Tabular Review

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