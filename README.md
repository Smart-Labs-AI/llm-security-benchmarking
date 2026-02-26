# llm-security-benchmarking

Benchmarking the security of various LLMs.

## Setup

```bash
uv sync
```

## Running the pipeline

```bash
dvc repro
```

DVC will only re-run stages whose inputs have changed:

- **New model added** to `params.yaml` → only that model is evaluated
- **`data/cve_db.json` updated** → all models are re-evaluated
- **`scripts/evaluate.py` changed** → all models are re-evaluated
- **Nothing changed** → `Data and pipelines are up to date`

## Project structure

```
data/
  cve_db.json          # CVE database (update this to trigger re-evaluation)
  leaderboard.json     # Final output — sorted by risk score (ascending)
  results/             # Per-model evaluation outputs
scripts/
  evaluate.py          # Evaluates one model: --model <id>
  aggregate.py         # Merges results/ → leaderboard.json
params.yaml            # Model list and metadata
dvc.yaml               # Pipeline definition
```

## Adding a new model

1. Add the model ID to `model_ids` in `params.yaml`
2. Add its metadata to `models` in `params.yaml`
3. Run `dvc repro`

## Useful commands

```bash
dvc status                                    # show what's out of date
dvc repro evaluate@<model-id> --force         # force re-evaluate one model
dvc repro --force                             # force re-evaluate everything
```
