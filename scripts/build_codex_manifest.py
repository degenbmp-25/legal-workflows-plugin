#!/usr/bin/env python3
"""Generate the Codex compatibility manifest from the portable Agent Plugins manifest.

OpenAI supports two package layouts:

  * Agent Plugins (portable) — `plugin.json` at the plugin root, with OpenAI
    settings under `extensions.com.openai`.
  * Codex — `.codex-plugin/plugin.json`, with the presentation fields at the
    root `interface` object and onboarding/review/publication still under
    `extensions.com.openai`.

The submission docs are explicit that the two files are NOT merged. When
`extensions.com.openai` is present in the root `plugin.json`, OpenAI ignores
`.codex-plugin/plugin.json` entirely; when it is absent, OpenAI reads those
settings from the Codex manifest instead.

That makes it safe to ship both in one package: the portable root manifest
wins for App Store submission, and the Codex manifest makes the same package
installable locally through Codex marketplace discovery.

This script derives the Codex manifest from the portable one so the two can
never drift. It never invents fields: every value is copied from the source.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Fields the Codex format wants at the root of its manifest.
ROOT_IDENTITY = ("name", "version", "description", "author", "homepage",
                 "repository", "license", "keywords")

# `skills` is required in the Codex format but is NOT part of the Agent Plugins
# schema (which sets additionalProperties:false and discovers skills/ by
# convention). It is therefore declared here rather than read from the portable
# manifest, so the two formats each stay valid on their own terms.
CODEX_SKILLS_PATH = "./skills/"

# `$schema` is required for Agent Plugins and must be omitted from the Codex
# manifest, which is not validated against the portable schema.
PORTABLE_ONLY = ("$schema",)


def build_codex_manifest(portable: dict) -> dict:
    codex: dict = {}

    for key in ROOT_IDENTITY:
        if key in portable:
            codex[key] = portable[key]

    # Required for Codex packages that ship skills.
    codex["skills"] = CODEX_SKILLS_PATH

    extensions = portable.get("extensions", {})
    openai = extensions.get("com.openai", {})

    # Presentation moves to the root `interface` object in the Codex format.
    interface = openai.get("interface")
    if interface is not None:
        codex["interface"] = interface

    # Onboarding, review, and publication stay under extensions.com.openai.
    passthrough = {
        key: openai[key]
        for key in ("onboardingSkill", "review", "publication")
        if key in openai
    }
    if passthrough:
        codex["extensions"] = {"com.openai": passthrough}

    return codex


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: build_codex_manifest.py <plugin-dir>", file=sys.stderr)
        return 2

    plugin_dir = Path(sys.argv[1]).resolve()
    src = plugin_dir / "plugin.json"
    if not src.is_file():
        print(f"MISSING PORTABLE MANIFEST: {src}", file=sys.stderr)
        return 1

    portable = json.loads(src.read_text(encoding="utf-8"))

    for key in PORTABLE_ONLY:
        portable.pop(key, None)

    codex = build_codex_manifest(portable)

    # The Codex manifest must not carry the portable schema reference.
    assert "$schema" not in codex, "Codex manifest must omit $schema"
    # It must not invent an MCP server for a skills-only package.
    assert "mcpServers" not in codex, "skills-only package must not declare mcpServers"

    out_dir = plugin_dir / ".codex-plugin"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "plugin.json"
    out.write_text(json.dumps(codex, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8")

    print(f"wrote {out}")
    print(f"  root fields: {sorted(codex.keys())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
