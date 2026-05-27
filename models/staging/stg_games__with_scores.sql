{{ config(materialized='table') }}

with cleaned as (
    select * from {{ ref('stg_games__cleaned') }}
)

select
    appid,
    game_name,
    release_date,
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
    positive_count,
    negative_count,
    positive_count + negative_count as review_count,
    score_rank,
    achievements,
    recommendations,
    avg_playtime_forever,
    avg_playtime_2weeks,
    median_playtime_forever,
    median_playtime_2weeks,
    developers,
    publishers,
    categories,
    genres,
    load_timestamp,

    metacritic_score / 100.0 as metacritic_normalized,
    user_score / 10.0 as user_score_normalized,

    case
        when metacritic_score >= 85 then 'excellent'
        when metacritic_score >= 70 then 'good'
        when metacritic_score >= 50 then 'ok'
        when metacritic_score > 0  then 'poor'
        else 'unrated'
    end as metacritic_tier,

    case
        when user_score >= 8 then 'excellent'
        when user_score >= 6 then 'good'
        when user_score >= 4 then 'ok'
        when user_score > 0  then 'poor'
        else 'unrated'
    end as user_score_tier
from cleaned
