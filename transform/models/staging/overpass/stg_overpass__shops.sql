with source as (
    select * from {{ source('overpass', 'shops') }}
)

select
    osm_id,
    name,
    lat,
    lon,
    city,
    street,
    housenumber,
    postcode,
    cuisine,
    amenity,
    shop
from source
where name is not null
