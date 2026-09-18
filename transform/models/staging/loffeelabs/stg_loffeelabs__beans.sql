-- TODO: column names below assume the LoffeeLabs bean payload shape described in the
-- project brief (id, name, roaster, origin, variety, process, flavor notes). Adjust once
-- the connector is deployed and the real Snowflake column names are known.

with source as (
    select * from {{ source('loffeelabs', 'beans') }}
),

renamed as (
    select
        id as bean_id,
        name as bean_name,
        roaster as roaster_name,
        origin,
        variety,
        process as process_raw,
        flavor_profile,
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
