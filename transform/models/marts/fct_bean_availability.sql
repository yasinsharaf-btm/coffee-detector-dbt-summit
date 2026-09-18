-- Bean-level grain, matched to a physical shop by roaster/shop name.
-- TODO: replace the name-based match with a real roaster<->shop key once one exists
-- in the source data (e.g. a shared roaster_id or address join).

with beans as (
    select * from {{ ref('stg_loffeelabs__beans') }}
),

shops as (
    select * from {{ ref('stg_overpass__shops') }}
)

select
    beans.bean_id,
    beans.bean_name,
    beans.roaster_name,
    beans.origin,
    beans.variety,
    beans.process_raw,
    beans.process_category,
    beans.flavor_profile,
    beans.updated_at,
    beans.is_experimental,
    case when beans.is_experimental then 1 else 0 end as is_experimental_int,
    shops.osm_id as shop_osm_id,
    shops.name as shop_name,
    shops.city as roaster_city,
    shops.lat,
    shops.lon
from beans
left join shops
    on lower(trim(beans.roaster_name)) = lower(trim(shops.name))
