{{ config(materialized='table') }}

with genres as (
    select * from {{ ref('int_games__flattened_genres') }}
),

engagement as (
    select appid, price, review_count, avg_playtime, revenue_estimate
    from {{ ref('int_games__with_engagement') }}
),

genre_stats as (
    select
        g.genre,
        count(distinct g.appid) as game_count,
        round(avg(e.price), 2) as avg_price,
        round(avg(e.review_count), 0)::bigint as avg_review_count,
        round(avg(e.avg_playtime), 0)::bigint as avg_playtime,
        round(sum(e.revenue_estimate), 2) as total_revenue_estimate
    from genres g
    left join engagement e on g.appid = e.appid
    group by g.genre
)

select
    genre,
    game_count,
    avg_price,
    avg_review_count,
    avg_playtime,
    total_revenue_estimate,
    row_number() over (order by game_count desc) as popularity_rank
from genre_stats
order by game_count desc
