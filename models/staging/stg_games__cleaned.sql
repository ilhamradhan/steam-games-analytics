{{ config(materialized='table') }}

with base as (
    select * from {{ ref('stg_games__base') }}
),

deduped as (
    select distinct on (appid) *
    from base
    order by appid, load_timestamp desc
)

select
    appid,
    trim(lower(name)) as game_name,
    release_date,
    estimated_owners,
    coalesce(peak_ccu, 0) as peak_ccu,
    required_age,
    coalesce(price, 0) as price,
    coalesce(dlc_count, 0) as dlc_count,
    coalesce(supported_languages, []::varchar[]) as supported_languages,
    coalesce(full_audio_languages, []::varchar[]) as full_audio_languages,
    windows,
    mac,
    linux,
    coalesce(metacritic_score, 0) as metacritic_score,
    coalesce(user_score, 0) as user_score,
    coalesce(positive, 0) as positive_count,
    coalesce(negative, 0) as negative_count,
    score_rank,
    coalesce(achievements, 0) as achievements,
    coalesce(recommendations, 0) as recommendations,
    coalesce(average_playtime_forever, 0) as avg_playtime_forever,
    coalesce(average_playtime_2weeks, 0) as avg_playtime_2weeks,
    coalesce(median_playtime_forever, 0) as median_playtime_forever,
    coalesce(median_playtime_2weeks, 0) as median_playtime_2weeks,
    coalesce(developers, []::varchar[]) as developers,
    coalesce(publishers, []::varchar[]) as publishers,
    coalesce(categories, []::varchar[]) as categories,
    genres,
    load_timestamp
from deduped
