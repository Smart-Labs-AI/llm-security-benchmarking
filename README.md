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
  upload.py            # Uploads leaderboard.json to Scaleway S3
params.yaml            # Model list and metadata
dvc.yaml               # Pipeline definition
```

## Adding a new model

1. Add the model ID to `model_ids` in `params.yaml`
2. Add its metadata to `models` in `params.yaml`
3. Run `dvc repro`

## DVC remote (one-time setup)

Results are cached in the `leaderboard-cache` Scaleway bucket so CI only re-evaluates changed models.

```bash
dvc remote modify --local scaleway access_key_id YOUR_SCW_ACCESS_KEY
dvc remote modify --local scaleway secret_access_key YOUR_SCW_SECRET_KEY
```

This writes to `.dvc/config.local` (git-ignored). After running the pipeline locally, push the cache:

```bash
dvc push
```

## Uploading to Scaleway

The leaderboard is served from a Scaleway Object Storage bucket at:
`https://leaderboard.s3.nl-ams.scw.cloud/leaderboard.json`

**One-time setup:**

```bash
cp .env.example .env  # fill in SCW_ACCESS_KEY and SCW_SECRET_KEY
```

The Scaleway API key needs the `ObjectStorageFullAccess` policy (IAM → API Keys in the Scaleway Console).
CORS configuration is managed in the website repo.

**Upload after pipeline run:**

```bash
dvc repro
source .env && uv run python scripts/upload.py
```

With direnv (`.envrc`), just:

```bash
dvc repro && uv run python scripts/upload.py
```

## CI/CD (GitHub Actions)

The pipeline runs automatically on:
- Push to `main` when `evaluate.py`, `cve_db.json`, `params.yaml`, or `dvc.yaml` change
- Monthly schedule (1st of month, 06:00 UTC)
- Manual trigger via `workflow_dispatch`

Required GitHub Secrets (Settings → Secrets and variables → Actions):
- `SCW_ACCESS_KEY`
- `SCW_SECRET_KEY`

## Useful commands

```bash
dvc status                                    # show what's out of date
dvc repro evaluate@<model-id> --force         # force re-evaluate one model
dvc repro --force                             # force re-evaluate everything
dvc push                                      # push results to remote cache
dvc pull                                      # fetch results from remote cache
```