---
name: coffee-pipeline
description: Use for this project's ingestion-to-dbt pipeline work — running a Fivetran connector locally, running the transform/ dbt project against DuckDB, or debugging a model, for the Experimental Roast & Specialty Coffee Detector.
---

# Coffee Pipeline

Fivetran Connector SDK + DuckDB, entirely local — no cloud warehouse. Each
connector's `fivetran debug` run writes to its own local DuckDB file
(`ingestion/<name>/files/warehouse.db`, schema `tester`). The dbt project in
`transform/` attaches both files read-only and builds a working DuckDB on top
of them (`transform/coffee_detector.duckdb`).

## Running a connector

From `ingestion/<name>/`:

```bash
pip install -r requirements.txt
fivetran debug --configuration configuration.json
```

Re-run this whenever the connector code changes or you need fresher data —
it overwrites that connector's `files/warehouse.db`.

## Running dbt

From `transform/`:

```bash
pip install dbt-duckdb
cp profiles.yml.example profiles.yml   # first time only
export DBT_PROFILES_DIR=.
dbt build
```

`dbt build` runs and tests every model. Use `dbt run -s <model>` /
`dbt test -s <model>` to iterate on one model at a time.

## Known gaps / TODOs to flag if touched

- `fct_bean_availability` joins beans to shops by matching roaster name to
  shop name (string match) — there's no real foreign key in the source data.
  If a better join key shows up, replace it.
- `transform/models/staging/_sources.yml` points at the `tester` schema,
  which is what `fivetran debug` uses locally. If a connector is later
  deployed to real Fivetran with a different destination schema, update the
  sources and profile accordingly.
