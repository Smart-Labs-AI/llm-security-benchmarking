"""
Aggregate per-model evaluation results into data/leaderboard.json.

Reads:
    params.yaml           — model metadata (name, provider, category)
    data/results/*.json   — per-model risk scores from evaluate.py

Writes:
    data/leaderboard.json — sorted leaderboard (ascending risk score)
"""
import datetime
import json
import pathlib
import yaml

params = yaml.safe_load(pathlib.Path("params.yaml").read_text())
metadata = params["models"]

results_dir = pathlib.Path("data/results")
entries = []

for result_file in sorted(results_dir.glob("*.json")):
    result = json.loads(result_file.read_text())
    model_id = result["model_id"]

    if model_id not in metadata:
        print(f"[aggregate] WARNING: no metadata for '{model_id}', skipping")
        continue

    meta = metadata[model_id]
    entries.append({
        "model": meta["name"],
        "provider": meta["provider"],
        "risk_score": result["risk_score"],
        "category": meta["category"],
        "last_evaluated": result["evaluated_at"],
    })

entries.sort(key=lambda e: e["risk_score"])

leaderboard = {
    "updated_at": datetime.date.today().isoformat(),
    "entries": entries,
}

out_path = pathlib.Path("data/leaderboard.json")
out_path.write_text(json.dumps(leaderboard, indent=2) + "\n")
print(f"[aggregate] wrote {len(entries)} entries to {out_path}")
