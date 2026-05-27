{{ config(materialized='table') }}

with engagement as (
    select * from {{ ref('int_games__with_engagement') }}
)

select
    appid,
    game_name,
    release_date,
    estimated_owners,
    price,
    metacritic_score,
    user_score,
    metacritic_tier,
    user_score_tier,
    metacritic_normalized,
    user_score_normalized,
    sentiment_ratio,
    positive_count,
    negative_count,
    review_count,
    recommendations,
    achievements,
    avg_playtime,
    avg_playtime_2weeks,
    median_playtime,
    owners_min,
    owners_max,
    revenue_estimate,

    engagement_score_raw,
    engagement_tier,

    windows,
    mac,
    linux,
    (case when windows then 1 else 0 end
     + case when mac then 1 else 0 end
     + case when linux then 1 else 0 end) as platform_count,

    case
        when metacritic_score >= 85 and sentiment_ratio >= 0.85 then 'blockbuster'
        when metacritic_score >= 70 and sentiment_ratio >= 0.75 then 'strong'
        when metacritic_score >= 50 then 'mixed'
        when metacritic_score > 0 then 'weak'
        else 'unrated'
    end as success_indicator
from engagement
