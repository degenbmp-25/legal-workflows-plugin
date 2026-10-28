#!/usr/bin/env bash
# Builds the uploadable plugin ZIP for the Legal Workflows plugin.
#
# SKILLS-ONLY: this package intentionally contains NO MCP server.
# OpenAI's plugin rules: "Adding an MCP server to an existing skills-only plugin
# is not currently supported", and ZIPs containing app references
# (apps / .app.json) cannot currently be submitted. This script enforces that
# by failing loudly if any MCP/app reference appears anywhere in the package.
#
# The ZIP root must contain plugin.json.
set -euo pipefail
cd "$(dirname "$0")/.."

PLUGIN_DIR="plugin"
DIST_DIR="dist"
STAGE="$DIST_DIR/plugin"
OUT="$DIST_DIR/legal-workflows-plugin.zip"

[ -d "$PLUGIN_DIR" ] || { echo "MISSING PLUGIN DIR: $PLUGIN_DIR" >&2; exit 1; }

rm -rf "$STAGE"
mkdir -p "$STAGE"
cp -r "$PLUGIN_DIR/." "$STAGE/"

# ---------------------------------------------------------------- guards ----

# 1. No MCP server and no app references anywhere in the package.
fail_if_present() {
  local label="$1"; shift
  local hits
  hits=$(grep -rIl -E "$1" "$STAGE" 2>/dev/null || true)
  if [ -n "$hits" ]; then
    echo "SKILLS-ONLY VIOLATION ($label): found in $STAGE" >&2
    echo "$hits" >&2
    exit 1
  fi
}

# Filenames that must not exist at all.
for forbidden in mcp.json .mcp.json .app.json apps.json; do
  if [ -n "$(find "$STAGE" -name "$forbidden" -print -quit)" ]; then
    echo "SKILLS-ONLY VIOLATION: package contains $forbidden" >&2
    find "$STAGE" -name "$forbidden" >&2
    exit 1
  fi
done

# Manifest keys that must not appear (would make this an MCP/app plugin).
fail_if_present '"apps"' '"apps"[[:space:]]*:'
fail_if_present '"mcpServers"' '"mcpServers"[[:space:]]*:'
fail_if_present '"mcp_server"' '"mcp"[[:space:]]*:'

# 2. Required files present.
REQUIRED=(
  "plugin.json"
  "LICENSE"
  "ATTRIBUTION.md"
  "skills/setup/SKILL.md"
  "assets/logo.svg"
  "assets/logo-dark.svg"
  "assets/composer-icon.svg"
  "assets/composer-icon-dark.svg"
)
for f in "${REQUIRED[@]}"; do
  [ -f "$STAGE/$f" ] || { echo "MISSING REQUIRED FILE: $f" >&2; exit 1; }
done

# 3. Every path referenced by plugin.json exists in the staged package.
node -e '
const fs = require("fs"), path = require("path");
const root = process.argv[1];
const manifest = JSON.parse(fs.readFileSync(path.join(root, "plugin.json"), "utf8"));
const refs = [];
const iface = manifest.extensions && manifest.extensions["com.openai"]
  ? manifest.extensions["com.openai"].interface
  : {};
const onboarding = manifest.extensions && manifest.extensions["com.openai"]
  ? manifest.extensions["com.openai"].onboardingSkill
  : null;
for (const key of ["skills", "onboardingSkill"]) {
  const v = key === "onboardingSkill" ? onboarding : manifest[key];
  if (typeof v === "string" && v.startsWith("./")) refs.push([key, v]);
}
for (const key of ["composerIcon", "composerIconDark", "logo", "logoDark"]) {
  const v = iface[key];
  if (typeof v === "string" && v.startsWith("./")) refs.push(["interface." + key, v]);
}
let bad = 0;
for (const [label, ref] of refs) {
  const p = path.join(root, ref);
  if (!fs.existsSync(p)) { console.error("MISSING REFERENCED PATH: " + label + " -> " + ref); bad = 1; }
}
if (bad) process.exit(1);
console.log("plugin.json path references: all " + refs.length + " resolved");
' "$STAGE" || exit 1

# 4. No secrets in the package.
if [ -n "$(grep -rIl -E "BEGIN (RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY|sk-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}|xox[baprs]-[A-Za-z0-9-]{10,}" "$STAGE" 2>/dev/null)" ]; then
  echo "SECRET DETECTED IN PACKAGE — refusing to build" >&2
  grep -rIl -E "BEGIN (RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY|sk-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}|xox[baprs]-[A-Za-z0-9-]{10,}" "$STAGE" >&2
  exit 1
fi

# 5. No executable scripts and no network calls inside the package.
EXEC_FILES=$(find "$STAGE" -type f -perm -u+x ! -name "*.md" ! -name "*.json" ! -name "*.yaml" ! -name "*.yml" ! -name "*.svg" | grep -v '\.docx$' || true)
if [ -n "$EXEC_FILES" ]; then
  echo "EXECUTABLE FILE IN PACKAGE — refusing to build" >&2
  echo "$EXEC_FILES" >&2
  exit 1
fi
NET_PAT='curl[[:space:]]|wget[[:space:]]|https?://[a-zA-Z0-9.-]*/(api|fetch|graphql)|fetch\((.|.)https?://|axios\.|requests\.(get|post)|urllib\.request'
if [ -n "$(grep -rIl -E "$NET_PAT" "$STAGE" 2>/dev/null)" ]; then
  echo "NETWORK CALL DETECTED IN PACKAGE — refusing to build" >&2
  grep -rIl -E "curl[[:space:]]|wget[[:space:]]|https?://[a-zA-Z0-9.-]*/(api|fetch|graphql)|fetch\(['\"]https?://|axios\.|requests\.(get|post)|urllib\.request" "$STAGE" >&2
  exit 1
fi

# 6. Per-file size limit (OpenAI caps each image at 5 MiB).
while IFS= read -r big; do
  size=$(stat -c %s "$big")
  if [ "$size" -gt 5242880 ]; then
    echo "FILE OVER 5 MiB: $big ($size bytes) — refusing to build" >&2
    exit 1
  fi
done < <(find "$STAGE" -type f -print)

# 7. Workflow SKILL.md count sanity.
SKILL_COUNT=$(find "$STAGE/skills" -mindepth 2 -maxdepth 2 -name SKILL.md ! -path "*/setup/*" | wc -l)
if [ "$SKILL_COUNT" -ne 32 ]; then
  echo "EXPECTED 32 WORKFLOW SKILLS, FOUND $SKILL_COUNT" >&2
  exit 1
fi

# ----------------------------------------------------------------- build ----

rm -f "$OUT"
( cd "$STAGE" && zip -qr "../$(basename "$OUT")" . )

# 8. ZIP root must contain plugin.json.
#
# Use `unzip -Z1` (name-only listing) piped into a grep that reads ALL input
# rather than exiting early. `grep -q` exits on the first match, which sends
# SIGPIPE to unzip; under `set -o pipefail` that surfaces as exit 141 and the
# check fails at random depending on how the two processes interleave. Reading
# the whole listing with `grep -c` avoids the race entirely.
ZIP_ROOT_COUNT=$(unzip -Z1 "$OUT" | grep -cE "(^|/)plugin\.json$" || true)
if [ "$ZIP_ROOT_COUNT" -ne 1 ]; then
  echo "ZIP ROOT MUST CONTAIN EXACTLY ONE plugin.json (found $ZIP_ROOT_COUNT)" >&2
  exit 1
fi

SIZE=$(stat -c %s "$OUT")
SHA=$(sha256sum "$OUT" | awk '{print $1}')
echo "Built $OUT"
echo "Size: $SIZE bytes ($(( SIZE / 1024 )) KiB)"
echo "SHA256: $SHA"
echo "Workflow skills packaged: $SKILL_COUNT"
