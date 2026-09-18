-- Column names verified against a live LoffeeLabs API call. The connector
-- normalizes the raw payload's hyphenated/camelCase keys (roast-name,
-- updatedAt, price-per-cup-(low), ...) to snake_case before landing them, so
-- these match the connector's output columns directly. There is no separate
-- "flavor_profile" field in the API — it's aliased here from "tasting"
-- (free tier strips "tasting-tag"/"general-tag").

with source as (
    select * from {{ source('loffeelabs', 'beans') }}
),

renamed as (
    select
        id as bean_id,
        roast_name as bean_name,
        roaster as roaster_name,
        origin,
        variety,
        process as process_raw,
        tasting as flavor_profile,
        try_cast(updated_at as date) as updated_at,
        lower(trim(process)) as process_normalized
    from source
)

select
    bean_id,
    bean_name,
    roaster_name,
    origin,
    variety,
    process_raw,
    flavor_profile,
    updated_at,
    case
        when process_normalized like '%anaerobic%' then 'anaerobic'
        when process_normalized like '%carbonic%' then 'carbonic_maceration'
        when process_normalized like '%thermal shock%' then 'thermal_shock'
        when process_normalized like '%co-ferment%' or process_normalized like '%coferment%' then 'co_ferment'
        when process_normalized like '%experimental%' then 'experimental_other'
        when process_normalized in ('washed', 'natural', 'honey') then 'traditional'
        else 'other'
    end as process_category,
    case
        when process_normalized like '%anaerobic%'
            or process_normalized like '%carbonic%'
            or process_normalized like '%thermal shock%'
            or process_normalized like '%co-ferment%'
            or process_normalized like '%coferment%'
            or process_normalized like '%experimental%'
        then true
        else false
    end as is_experimental
from renamed
