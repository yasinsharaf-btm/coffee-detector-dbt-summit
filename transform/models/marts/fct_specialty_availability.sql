-- One row per physical shop with a "Specialty Score": the ratio of experimental
-- single-origin/process beans to the shop-associated roaster's total catalog.

with bean_availability as (
    select * from {{ ref('fct_bean_availability') }}
)

select
    shop_osm_id,
    shop_name,
    roaster_city,
    lat,
    lon,
    count(*) as total_bean_count,
    sum(is_experimental_int) as experimental_bean_count,
    round(sum(is_experimental_int) * 1.0 / nullif(count(*), 0), 4) as specialty_score
from bean_availability
where shop_osm_id is not null
group by 1, 2, 3, 4, 5
