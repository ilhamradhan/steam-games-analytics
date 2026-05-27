{{ config(materialized='table') }}

with engagement as (
    select * from {{ ref('int_games__with_engagement') }}
)

select
    appid,
    game_name,
    release_date,
    price,
    positive_count,
    negative_count,
    review_count,
    recommendations,
    avg_playtime,
    sentiment_ratio,
    engagement_tier,

    case
        when engagement_tier = 'viral' then 'High social proof with strong review volume and playtime'
        when engagement_tier = 'popular' then 'Solid review base with decent engagement'
        when engagement_tier = 'moderate' then 'Some reviews but limited engagement'
        when engagement_tier = 'low' then 'Very few reviews, low visibility'
        when engagement_tier = 'none' then 'No reviews or engagement data'
    end as segment_description,

    case
        when engagement_tier in ('viral', 'popular') then 'high_value'
        when engagement_tier = 'moderate' then 'mid_value'
        when engagement_tier in ('low', 'none') then 'low_value'
    end as segment_value_category
from engagement
order by
    case engagement_tier
        when 'viral' then 1
        when 'popular' then 2
        when 'moderate' then 3
        when 'low' then 4
        when 'none' then 5
    end
