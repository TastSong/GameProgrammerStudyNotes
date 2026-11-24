#!/usr/bin/env bash
set -euo pipefail

python3 ai/scripts/validate_meta.py
python3 ai/scripts/validate_indexes.py
python3 ai/scripts/build_index.py --check
python3 ai/scripts/check_repo.py
python3 -m unittest discover -s ai/tests -v
python3 ai/scripts/evaluate_retrieval.py --top 5 --min-recall 0.8
