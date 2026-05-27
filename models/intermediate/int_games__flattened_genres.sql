{{ config(materialized='table') }}

with scored as (
    select appid, game_name, release_date, genres
    from {{ ref('stg_games__with_scores') }}
)

select
    appid,
    game_name,
    release_date,
    trim(genre) as genre
from scored, unnest(genres) as t(genre)
where genres is not null
  and len(genres) > 0
