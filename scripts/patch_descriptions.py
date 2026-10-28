#!/usr/bin/env python3
"""Give every packaged workflow a distinct, trigger-explicit description.

Why this exists
---------------
The upstream workflows under `skills/` are redistributed under MIT. Upstream
generates the eleven tabular workflows from one template, so ten of them ship
with a byte-identical description:

    "Use this workflow to review uploaded documents and extract structured
     information into the tabular review columns defined in
     table-columns.yaml."

Description is the auto-load surface for a skills-only plugin: it is what the
model reads when deciding which workflow to run. Ten workflows that describe
themselves identically are ten workflows the model cannot tell apart, so the
"extract the key terms from this credit agreement" prompt can land on the
supply-agreement workflow. The plugin ships a `table-columns.yaml` per tabular
workflow, and those column lists differ precisely where the workflows differ.

The fix is confined to the `description:` field in each SKILL.md frontmatter.
The workflow body is left byte-identical to upstream, so the legal content,
the review instructions, and the column definitions are all untouched.

MIT permits modification of redistributed material provided the copyright and
permission notice accompany it. The upstream `LICENSE` ships in this package
and `ATTRIBUTION.md` records exactly which files were changed and how.

Idempotent: running it twice produces the same result.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# --- Tabular workflows -------------------------------------------------------
# Upstream describes these with one shared sentence. Each replacement names the
# workflow, states what it extracts, and says when to use it *instead of* the
# neighbouring workflow, because several of these overlap in subject matter.
TABULAR = {
    "nda-tabular-review": (
        "Use when the user wants a non-disclosure or confidentiality agreement "
        "pulled into fixed columns rather than reviewed clause by clause: whether "
        "the NDA is mutual or unilateral, how Confidential Information is defined, "
        "the receiving party's obligations, which standard carveouts are present, "
        "permitted disclosures, term and duration, return and destruction, "
        "remedies, and governing law. Extracting these columns from "
        "table-columns.yaml. For a clause-by-clause review from the user's "
        "perspective, use nda-review instead."
    ),
    "credit-agreement-tabular-review": (
        "Use when the user wants a credit agreement or facility agreement "
        "pulled into fixed columns: lenders, borrowers, guarantors and other "
        "parties, facility, committed amount, purpose, interest and commitment "
        "fee, repayment schedule, maturity, security, financial covenants, "
        "events of default, assignment, change of control, prepayment fees, "
        "governing law, and dispute resolution. Extracting these columns from "
        "table-columns.yaml. For a conditions precedent checklist, use "
        "cp-checklist-draft instead."
    ),
    "commercial-lease-tabular-review": (
        "Use when the user wants a commercial lease pulled into fixed columns: "
        "landlord, tenant, guarantor, premises, lease date, term, rent and rent "
        "review, service charge, insurance, permitted use, repair and "
        "maintenance, alterations, assignment and subletting, break rights, "
        "security of tenure, dilapidations, rent deposit, forfeiture and "
        "termination, and governing law. Extracting these columns from "
        "table-columns.yaml."
    ),
    "supply-agreement-tabular-review": (
        "Use when the user wants a supply, purchase, or product supply "
        "agreement pulled into fixed columns: parties, effective date, products, "
        "term and renewal, delivery, quality, warranties, liquidated damages, "
        "limitation of liability, force majeure, termination rights, governing "
        "law, and dispute resolution. Extracting these columns from "
        "table-columns.yaml."
    ),
    "spa-tabular-review": (
        "Use when the user wants a share purchase or acquisition agreement "
        "pulled into fixed columns: parties, date, transaction, consideration, "
        "conditions precedent, completion date, warranties, indemnities, "
        "limitation of liability, covenants, exclusivity, governing law, and "
        "dispute resolution. Extracting these columns from table-columns.yaml."
    ),
    "shareholder-agreement-tabular-review": (
        "Use when the user wants a shareholders' or shareholders' agreement "
        "pulled into fixed columns: parties, share capital and classes, "
        "shareholdings, board composition, reserved matters, pre-emption on new "
        "shares and on transfers, drag-along and tag-along rights, "
        "anti-dilution, dividend policy, exit and liquidity, deadlock, "
        "restrictive covenants, warranties, governing law, and dispute "
        "resolution. Extracting these columns from table-columns.yaml."
    ),
    "employment-agreement-tabular-review": (
        "Use when the user wants an employment contract pulled into fixed "
        "columns: employer, employee, date, title, compensation, full-time or "
        "part-time status, independent-contractor classification, benefits, "
        "notice periods in both directions, overtime, working hours, "
        "variation, intellectual property assignment, grounds for termination, "
        "and annual leave entitlement. Extracting these columns from "
        "table-columns.yaml."
    ),
    "commercial-agreement-tabular-review": (
        "Use when the user wants a general commercial, services, or supply "
        "agreement pulled into fixed columns: parties, scope of work, whether "
        "it amends an earlier agreement, effective date, term, renewal, "
        "pricing, price adjustments, late-payment penalties, estimated contract "
        "value, limitation of liability, IP ownership and licensing, change of "
        "control, force majeure, termination rights, liquidated damages, "
        "governing law, and dispute resolution. Extracting these columns from "
        "table-columns.yaml."
    ),
    "limited-partnership-agreement-tabular-review": (
        "Use when the user wants a limited partnership agreement or fund "
        "governing terms pulled into fixed columns: general partner, fund name "
        "and jurisdiction, total committed capital, capital calls and "
        "drawdowns, funding-failure penalties, investment scope and "
        "restrictions, fund term, management fee, carried interest, preferred "
        "return, GP catch-up, clawback, expenses, distributions, key person, "
        "removal of the GP, LPAC, transfer restrictions, conflicts, and "
        "governing law. Extracting these columns from table-columns.yaml."
    ),
    "change-of-control-tabular-review": (
        "Use when the user wants a change of control due diligence review "
        "pulled into fixed columns: the parties, the date, the term, the "
        "change of control clause itself, whether consent is required, "
        "termination rights, put or call options, and the financial "
        "implications. Extracting these columns from table-columns.yaml."
    ),
    "e-discovery-tabular-review": (
        "Use when the user wants a set of documents catalogued for e-discovery "
        "or a document schedule pulled into fixed columns: date, document type, "
        "sender, recipients, a short summary, the persons mentioned, and "
        "whether the document is marked privileged. Extracting these columns "
        "from table-columns.yaml."
    ),
}

# --- Assistant workflows -----------------------------------------------------
# These upstream descriptions already name the task, so the only gap is the
# explicit trigger phrase. A short "Use when ..." sentence is prepended.
ASSISTANT = {
    "nda-review": (
        "Use when the user wants a non-disclosure agreement reviewed from the "
        "perspective of the party they represent. "
    ),
    "credit-agreement-review": (
        "Use when the user wants a credit agreement reviewed from the "
        "perspective of the party they represent. "
    ),
    "commercial-lease-review": (
        "Use when the user wants a commercial lease reviewed from the "
        "perspective of the party they represent. "
    ),
    "employment-agreement-review": (
        "Use when the user wants an employment agreement reviewed from the "
        "perspective of the party they represent. "
    ),
    "shareholder-agreement-review": (
        "Use when the user wants a shareholder agreement reviewed from the "
        "perspective of the party they represent. "
    ),
    "guarantee-agreement-review": (
        "Use when the user wants a guarantee, guaranty, or "
        "guarantee-and-indemnity agreement reviewed from the perspective of the "
        "party they represent. "
    ),
    "bpo-agreement-review": (
        "Use when the user wants a BPO, IT outsourcing, or IS outsourcing "
        "agreement reviewed from the perspective of the Customer or Supplier "
        "they represent. "
    ),
    "compare-documents": (
        "Use when the user has two or more versions of a document and wants them "
        "compared in a structured table of similarities, differences, risks, "
        "and follow-up points. "
    ),
    "cp-checklist-draft": (
        "Use when the user wants a conditions precedent (CP) checklist drafted "
        "from a credit agreement or financing document. "
    ),
    "corporate-approvals-review": (
        "Use when the user wants to know whether a company's corporate "
        "approvals, resolutions, authority materials, and corporate records are "
        "complete and internally consistent. "
    ),
    "draft-from-template": (
        "Use when the user wants an uploaded template edited or populated using "
        "their instructions and source materials, with the original file "
        "preserved. "
    ),
    "extract-key-terms": (
        "Use when the user wants the key legal, commercial, and operational "
        "terms pulled out of one or more documents. "
    ),
    "issues-list-draft": (
        "Use when the user wants an issues list drafted from an agreement, from "
        "the perspective of the party they represent. "
    ),
    "proofread": (
        "Use when the user wants a document proofread for drafting quality, "
        "internal consistency, and mechanical errors. "
    ),
}

# Workflows whose descriptions already contain a trigger phrase, or that use a
# folded YAML block scalar which this script deliberately does not rewrite.
SKIP = {"msa-draft", "msa-review", "setup"}


def rewrite(path: Path, new_description: str) -> bool:
    text = path.read_text(encoding="utf-8")

    if '"' in new_description or "\\" in new_description:
        raise SystemExit(f"description contains a quote or backslash: {path}")

    match = re.match(r"^(---\n)(.*?)(^---\n)", text, re.S | re.M)
    if not match:
        raise SystemExit(f"no frontmatter found: {path}")

    frontmatter = match.group(2)
    body = text[match.end():]

    desc = re.search(r"^description:[ \t]*(.*)$", frontmatter, re.M)
    if not desc:
        raise SystemExit(f"no description field found: {path}")

    current = desc.group(1).strip()
    if current.startswith(">") or current.startswith("|"):
        # Folded/literal block scalar — handled separately, not by this path.
        raise SystemExit(f"block-scalar description not handled: {path}")

    # Strip surrounding quotes from the existing value for comparison.
    bare = current.strip('"').strip("'")
    if bare == new_description:
        return False

    quoted = '"' + new_description.replace('"', '\\"') + '"'
    new_frontmatter = frontmatter[: desc.start(1)] + quoted + frontmatter[desc.end(1):]

    path.write_text(
        match.group(1) + new_frontmatter + match.group(3) + body,
        encoding="utf-8",
    )
    return True


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: patch_descriptions.py <plugin-dir>", file=sys.stderr)
        return 2

    plugin_dir = Path(sys.argv[1]).resolve()
    skills_dir = plugin_dir / "skills"
    if not skills_dir.is_dir():
        print(f"MISSING SKILLS DIR: {skills_dir}", file=sys.stderr)
        return 1

    planned = {**TABULAR, **ASSISTANT}
    changed = []
    unchanged = []

    for name, description in planned.items():
        path = skills_dir / name / "SKILL.md"
        if not path.is_file():
            print(f"MISSING WORKFLOW: {path}", file=sys.stderr)
            return 1
        if rewrite(path, description):
            changed.append(name)
        else:
            unchanged.append(name)

    # Every workflow that is not explicitly skipped must now carry a distinct
    # description with a trigger phrase.
    descriptions = {}
    missing_trigger = []
    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            continue
        text = skill_file.read_text(encoding="utf-8")
        fm = re.match(r"^---\n(.*?)^---\n", text, re.S | re.M).group(1)
        dm = re.search(r"^description:[ \t]*(.*?)(?=\n[a-zA-Z_]+:|\Z)", fm, re.S | re.M)
        value = dm.group(1).strip() if dm else ""
        if value.startswith(">"):
            value = " ".join(value[1:].split())
        else:
            value = value.strip('"').strip("'")
        descriptions[skill_dir.name] = value

        if not re.search(r"use when|use this when|use whenever", value, re.I):
            missing_trigger.append(skill_dir.name)

    print(f"changed: {len(changed)}")
    for name in changed:
        print(f"  - {name}")
    print(f"already correct: {len(unchanged)}")

    dupes = {}
    for name, value in descriptions.items():
        dupes.setdefault(value, []).append(name)
    duplicate_groups = {k: v for k, v in dupes.items() if len(v) > 1}

    print(f"\nworkflows with a trigger phrase: "
          f"{len(descriptions) - len(missing_trigger)}/{len(descriptions)}")
    if missing_trigger:
        print(f"  MISSING TRIGGER: {missing_trigger}")

    print(f"duplicate description groups: {len(duplicate_groups)}")
    for value, names in duplicate_groups.items():
        print(f"  {names} -> {value[:80]}")

    if missing_trigger or duplicate_groups:
        print("\nFAILED: descriptions are not yet distinct and trigger-explicit")
        return 1

    print("\nOK: every workflow has a distinct, trigger-explicit description")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
