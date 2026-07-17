#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

rm -rf src mutants
mkdir -p src

rsync -a subject_system/banking_system/accounts/ src/accounts/
rsync -a subject_system/banking_system/transactions/ src/transactions/
rsync -a subject_system/banking_system/banking_system/ src/banking_system/
rsync -a subject_system/banking_system/core/ src/core/
rsync -a subject_system/banking_system/templates/ src/templates/

find src -type d -name "__pycache__" -prune -exec rm -rf {} +
find src -type f -name "*.pyc" -delete

echo "Mutation workspace prepared under src/"
