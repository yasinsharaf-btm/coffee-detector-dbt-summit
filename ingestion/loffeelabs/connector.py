"""
Fivetran Connector SDK connector for the LoffeeLabs Bean Base API.

Free tier constraints (see https://loffeelabs.com/developers/documentation):
  - 1 request / 3 seconds
  - max 50 beans per call
  - latest 1,000 beans available, 2,000/day quota

Run locally with:
    fivetran debug --configuration configuration.json
"""

import time

import requests
from fivetran_connector_sdk import Connector
from fivetran_connector_sdk import Logging as log
from fivetran_connector_sdk import Operations as op

BASE_URL = "https://api.loffeelabs.com/api/v2"
PAGE_LIMIT = 50
RATE_LIMIT_SECONDS = 3

DICTIONARY_ENDPOINTS = ["roasters", "processes", "origins", "varieties"]


def schema(configuration: dict):
    tables = [{"table": "beans", "primary_key": ["id"]}]
    for name in DICTIONARY_ENDPOINTS:
        tables.append({"table": name, "primary_key": ["value"]})
    return tables


def _get(endpoint: str, headers: dict, params: dict | None = None) -> requests.Response:
    resp = requests.get(f"{BASE_URL}/{endpoint}", headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    return resp


def _extract_list(payload):
    """LoffeeLabs wraps list responses inconsistently across endpoints; handle both shapes."""
    if isinstance(payload, list):
        return payload
    for key in ("data", "beans", "results", "items"):
        if isinstance(payload, dict) and key in payload:
            return payload[key]
    return []


def _sync_beans(headers: dict, state: dict):
    page = state.get("last_page", 0) + 1
    while True:
        log.info(f"Fetching beans page {page}")
        resp = _get("beans", headers, params={"page": page, "limit": PAGE_LIMIT})
        beans = _extract_list(resp.json())
        if not beans:
            break

        for bean in beans:
            yield op.upsert(table="beans", data=bean)

        state["last_page"] = page
        yield op.checkpoint(state=state)

        if len(beans) < PAGE_LIMIT:
            break
        page += 1
        time.sleep(RATE_LIMIT_SECONDS)


def _sync_dictionary(endpoint: str, headers: dict):
    log.info(f"Fetching dictionary endpoint: {endpoint}")
    resp = _get(endpoint, headers, params={"flat": "true"})
    values = _extract_list(resp.json())
    for value in values:
        if isinstance(value, dict):
            row = value
            row.setdefault("value", row.get("name") or row.get("id"))
        else:
            row = {"value": value}
        yield op.upsert(table=endpoint, data=row)
    time.sleep(RATE_LIMIT_SECONDS)


def update(configuration: dict, state: dict):
    api_key = configuration["api_key"]
    headers = {"Authorization": f"Bearer {api_key}"}

    yield from _sync_beans(headers, state)

    for endpoint in DICTIONARY_ENDPOINTS:
        yield from _sync_dictionary(endpoint, headers)

    yield op.checkpoint(state=state)


connector = Connector(update=update, schema=schema)

if __name__ == "__main__":
    connector.debug()
