# Experimental Roast & Specialty Coffee Detector

dbt Summit 2026 hackathon project. Bridges generic coffee shop listings with
specialty roasters offering experimental processes (anaerobic, thermal shock,
carbonic maceration).

## Structure

- `ingestion/` — Fivetran Connector SDK connectors
  - `loffeelabs/` — bean catalog (origin, roaster, process) from the LoffeeLabs API
  - `overpass/` — coffee shop locations from OpenStreetMap via the Overpass API
- `transform/` — dbt project
  - `models/staging/` — cleaned, normalized sources
  - `models/marts/` — `fct_bean_availability`, `fct_specialty_availability`
  - `models/semantic/` — semantic model + metrics (`experimental_bean_count`, `specialty_score`)

## Stack

Fivetran Connector SDK + DuckDB, run entirely locally — no data warehouse.
Each connector's `fivetran debug` run writes to its own local DuckDB file
(`ingestion/<name>/files/warehouse.db`, schema `tester`). The dbt project
attaches both files read-only and builds its own working DuckDB
(`transform/coffee_detector.duckdb`) on top of them.

## Local dbt development

```bash
cd ingestion/loffeelabs && pip install -r requirements.txt && fivetran debug --configuration configuration.json && cd ../..
cd ingestion/overpass && pip install -r requirements.txt && fivetran debug --configuration configuration.json && cd ../..

cd transform
pip install dbt-duckdb
cp profiles.yml.example profiles.yml
export DBT_PROFILES_DIR=.
dbt build
```
