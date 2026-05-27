{{ config(materialized='table') }}

with source as (
    select * from {{ source('raw', 'raw_steam_games') }}
)

select
    cast(appid as integer) as appid,
    name,
    try_cast(release_date as date) as release_date,
    estimated_owners,
    peak_ccu,
    required_age,
    price,
    dlc_count,
    supported_languages,
    full_audio_languages,
    windows,
    mac,
    linux,
    metacritic_score,
    user_score,
    positive,
    negative,
    score_rank,
    achievements,
    recommendations,
    average_playtime_forever,
    average_playtime_2weeks,
    median_playtime_forever,
    median_playtime_2weeks,
    developers,
    publishers,
    categories,
    genres,
    current_timestamp as load_timestamp
from source
