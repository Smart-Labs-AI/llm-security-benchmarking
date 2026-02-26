"""
Evaluate a single LLM model for security risk.

Usage:
    python scripts/evaluate.py --model <model-id>

Writes:
    data/results/<model-id>.json

TODO: Replace the mock random score with real benchmark logic that reads
      data/cve_db.json and runs the model against security test cases.
"""
import argparse
import datetime
import json
import pathlib
import random

parser = argparse.ArgumentParser(description="Evaluate a model's security risk score.")
parser.add_argument("--model", required=True, help="Model ID (must match an entry in params.yaml)")
args = parser.parse_args()

# --- Mock implementation ---
# Replace this block with real scoring logic that uses data/cve_db.json.
risk_score = round(random.uniform(0, 100), 1)
# --------------------------

result = {
    "model_id": args.model,
    "evaluated_at": datetime.date.today().strftime("%Y-%m"),
    "risk_score": risk_score,
}

out_path = pathlib.Path("data/results") / f"{args.model}.json"
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(json.dumps(result, indent=2) + "\n")

print(f"[evaluate] {args.model}: risk_score={risk_score}")
