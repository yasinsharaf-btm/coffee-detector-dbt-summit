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

## dbt Cloud

This repo is connected to the dbt Cloud project **dbt Summit 26 - Hackathon**
(account 188483, project 573518), warehouse: Snowflake (`SUMMIT26_HACKATHON_DB`).
The dbt project subdirectory is `transform/`.

Sources in `transform/models/staging/_sources.yml` assume the Fivetran
destination schemas are named `loffeelabs` and `overpass` — confirm and adjust
once the connectors are deployed and syncing.

## Local dbt development

```bash
cd transform
cp profiles.yml.example profiles.yml   # fill in your Snowflake user/password
export DBT_PROFILES_DIR=.
dbt deps
dbt build
```
