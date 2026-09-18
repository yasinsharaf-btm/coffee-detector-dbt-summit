---
name: coffee-pipeline
description: Use for this project's ingestion-to-dbt pipeline work — debugging a Fivetran connector locally, running the transform/ dbt project, checking source freshness, or checking dbt Cloud model/job health for the Experimental Roast & Specialty Coffee Detector.
---

# Coffee Pipeline

This project has two Fivetran Connector SDK connectors landing in Snowflake
(`SUMMIT26_HACKATHON_DB`), and a dbt project in `transform/` that reads from
them. Use this skill whenever asked to run, debug, or check the health of
this pipeline.

## Debugging a connector locally

Each connector has its own venv-friendly folder under `ingestion/<name>/`.
From that folder:

```bash
pip install -r requirements.txt
fivetran debug --configuration configuration.json
```

This writes to a local `files/warehouse.db` DuckDB file for quick iteration —
it does NOT touch the real Snowflake destination. Use it to sanity-check a
connector's schema/output shape before deploying it to Fivetran.

## Running dbt

From `transform/`:

```bash
export DBT_PROFILES_DIR=.
dbt deps
dbt build
```

Requires `transform/profiles.yml` (copy from `profiles.yml.example`, gitignored)
with real Snowflake credentials, or run against dbt Cloud instead (see below).

## Checking dbt Cloud / source freshness

Prefer the `dbt` MCP tools over shelling out to the Admin API:

- `get_all_sources` — check freshness status on `loffeelabs`/`overpass` sources
- `get_all_models`, `get_model_health` — check model state in the `Prod` environment
- `list_jobs`, `list_jobs_runs`, `get_job_run_error` — check/debug scheduled runs
- `get_metrics_compiled_sql`, `query_metrics` — sanity-check `experimental_bean_count` / `specialty_score`

## Known gaps / TODOs to flag if touched

- `transform/models/staging/_sources.yml` schema names (`loffeelabs`, `overpass`)
  are a guess until the Fivetran destination is live — verify against the
  actual Snowflake schema before trusting freshness checks.
- `fct_bean_availability` joins beans to shops by matching roaster name to
  shop name (string match) — there's no real foreign key yet. If a better
  join key shows up in the real data, replace it.
