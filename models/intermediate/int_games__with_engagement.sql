{{ config(materialized='table') }}

with scored as (
    select * from {{ ref('stg_games__with_scores') }}
)

select
    appid,
    game_name,
    release_date,
    estimated_owners,
    price,
    metacritic_score,
    user_score,
    metacritic_normalized,
    user_score_normalized,
    metacritic_tier,
    user_score_tier,
    positive_count,
    negative_count,
    review_count,
    recommendations,
    avg_playtime_forever as avg_playtime,
    avg_playtime_2weeks,
    median_playtime_forever as median_playtime,
    achievements,
    windows,
    mac,
    linux,
    developers,
    publishers,
    categories,
    genres,
    load_timestamp,

    cast(split_part(estimated_owners, ' - ', 1) as bigint) as owners_min,
    cast(split_part(estimated_owners, ' - ', 2) as bigint) as owners_max,

    case
        when positive_count + negative_count > 0
        then positive_count::float / (positive_count + negative_count)
        else null
    end as sentiment_ratio,

    ln(greatest(review_count, 1)) * 0.4
      + ln(greatest(avg_playtime_forever, 1)) * 0.3
      + ln(greatest(recommendations, 1)) * 0.3
    as engagement_score_raw,

    case
        when recommendations > 1000
             and positive_count > 500
             and avg_playtime_forever > 1000
        then 'viral'
        when positive_count > 100
             and review_count > 200
        then 'popular'
        when review_count >= 10
        then 'moderate'
        when review_count > 0
        then 'low'
        else 'none'
    end as engagement_tier,

    (cast(split_part(estimated_owners, ' - ', 1) as bigint)
     + cast(split_part(estimated_owners, ' - ', 2) as bigint)) / 2.0
     * coalesce(price, 0) as revenue_estimate
from scored
