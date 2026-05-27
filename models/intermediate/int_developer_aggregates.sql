{{ config(materialized='table') }}

with engagement as (
    select * from {{ ref('int_games__with_engagement') }}
),

developers_flat as (
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
        trim(developer) as developer
    from engagement, unnest(developers) as t(developer)
    where developers is not null
      and len(developers) > 0
)

select
    developer,
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
from developers_flat
group by developer
having count(distinct appid) >= 1
