-- Required by MetricFlow even though this project has no time-series
-- dimension yet — see https://docs.getdbt.com/docs/build/metricflow-time-spine

select cast(r.range as date) as date_day
from range(cast('2020-01-01' as date), cast('2030-12-31' as date), interval 1 day) as r
