{{ config(materialized='table') }}

with scored as (
    select appid, game_name, release_date, categories
    from {{ ref('stg_games__with_scores') }}
)

select
    appid,
    game_name,
    release_date,
    trim(category) as category
from scored, unnest(categories) as t(category)
where categories is not null
  and len(categories) > 0
