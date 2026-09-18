"""
Fivetran Connector SDK connector for coffee shop locations via the
Overpass API (OpenStreetMap) — no auth required.

Bounding box defaults to Seattle, WA.

Run locally with:
    fivetran debug --configuration configuration.json
"""

import time

import requests
from fivetran_connector_sdk import Connector
from fivetran_connector_sdk import Logging as log
from fivetran_connector_sdk import Operations as op

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 15

# south, west, north, east — central Seattle (downtown through Fremont/Ballard/U District)
DEFAULT_BBOX = "47.55, -122.40, 47.70, -122.28"


def schema(configuration: dict):
    return [{"table": "shops", "primary_key": ["osm_id"]}]


def _build_query(bbox: str) -> str:
    return f"""
    [out:json][timeout:40];
    (
      node["amenity"="cafe"]({bbox});
      node["shop"="coffee"]({bbox});
    );
    out body;
    """


def _query_overpass(bbox: str) -> list:
    """Overpass's public instance is frequently overloaded (per project docs) —
    transient 504s are expected and worth a short retry, not a hard failure."""
    headers = {"User-Agent": "dbt-summit-hackathon-coffee-detector/1.0 (research project)"}
    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(
                OVERPASS_URL, data={"data": _build_query(bbox)}, headers=headers, timeout=60
            )
            resp.raise_for_status()
            return resp.json().get("elements", [])
        except requests.exceptions.HTTPError as exc:
            last_error = exc
            log.warning(
                f"Overpass request failed (attempt {attempt}/{MAX_RETRIES}): {exc}"
            )
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF_SECONDS)
    raise last_error


def update(configuration: dict, state: dict):
    bbox = configuration.get("bbox", DEFAULT_BBOX)
    log.info(f"Querying Overpass for coffee shops in bbox: {bbox}")

    elements = _query_overpass(bbox)

    for el in elements:
        tags = el.get("tags", {})
        row = {
            "osm_id": el.get("id"),
            "lat": el.get("lat"),
            "lon": el.get("lon"),
            "name": tags.get("name"),
            "city": tags.get("addr:city"),
            "street": tags.get("addr:street"),
            "housenumber": tags.get("addr:housenumber"),
            "postcode": tags.get("addr:postcode"),
            "cuisine": tags.get("cuisine"),
            "amenity": tags.get("amenity"),
            "shop": tags.get("shop"),
        }
        yield op.upsert(table="shops", data=row)

    yield op.checkpoint(state={"bbox": bbox})


connector = Connector(update=update, schema=schema)

if __name__ == "__main__":
    connector.debug()
