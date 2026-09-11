#!/bin/bash
# Regenerate the typed transport client from the v3 OpenAPI spec.
#
# The generated code lands in src/aplos_nca_saas_sdk/_generated/ and is fully
# overwritten each run — never hand-edit it. The ergonomic facade (AplosClient)
# and the existing nca_resources ergonomics live OUTSIDE _generated/ and are
# unaffected by regeneration.
#
# To refresh the spec from the IaC repo first, copy its generated spec into
# openapi/openapi-spec.json (see the sibling refresh step / README).
#
# Usage:  ./openapi/generate-client.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

SPEC="$REPO_ROOT/openapi/openapi-spec.json"
CONFIG="$REPO_ROOT/openapi/codegen-config.yaml"
OUT="$REPO_ROOT/src/aplos_nca_saas_sdk/_generated"

echo "Generating typed client from $SPEC"
echo "  output: $OUT"

# --meta none: emit only the package (no pyproject/setup), so it embeds in the
# existing SDK package. --overwrite: regeneration replaces the prior output.
openapi-python-client generate \
  --path "$SPEC" \
  --config "$CONFIG" \
  --meta none \
  --output-path "$OUT" \
  --overwrite

echo "Client generation complete."
