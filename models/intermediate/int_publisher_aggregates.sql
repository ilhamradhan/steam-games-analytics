{{ config(materialized='table') }}

with engagement as (
    select * from {{ ref('int_games__with_engagement') }}
),

publishers_flat as (
    select
        appid,
        game_name,
        price,
        metacritic_score,
        user_score,
        positive_count,
        negative_count,
        review_count,
        avg_playtime,
        revenue_estimate,
        recommendations,
        trim(publisher) as publisher
    from engagement, unnest(publishers) as t(publisher)
    where publishers is not null
      and len(publishers) > 0
)

select
    publisher,
    count(distinct appid) as game_count,
    round(avg(price), 2) as avg_price,
    round(avg(metacritic_score), 1) as avg_metacritic_score,
    round(avg(user_score), 1) as avg_user_score,
    sum(positive_count) as total_positive_reviews,
    sum(negative_count) as total_negative_reviews,
    sum(review_count) as total_reviews,
    round(avg(avg_playtime), 0)::bigint as avg_playtime,
    round(sum(revenue_estimate), 2) as total_revenue_estimate,
    sum(recommendations) as total_recommendations
from publishers_flat
group by publisher
having count(distinct appid) >= 1
