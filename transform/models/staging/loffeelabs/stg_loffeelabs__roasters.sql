-- Dictionary table from the LoffeeLabs API; passthrough with a stable column name
-- so downstream models can join on roaster_name without caring about the raw shape.

with source as (
    select * from {{ source('loffeelabs', 'roasters') }}
)

select
    value as roaster_name
from source
