{{ config(materialized='table') }}

with publishers as (
    select * from {{ ref('int_publisher_aggregates') }}
),

total_market as (
    select sum(total_revenue_estimate) as total_global_revenue,
           sum(game_count) as total_global_games
    from publishers
)

select
    p.publisher,
    p.game_count,
    p.avg_price,
    p.avg_metacritic_score,
    p.avg_user_score,
    p.total_positive_reviews,
    p.total_negative_reviews,
    p.total_reviews,
    p.avg_playtime,
    p.total_revenue_estimate,
    p.total_recommendations,

    round(
        p.total_revenue_estimate::float
        / nullif(tm.total_global_revenue, 0) * 100, 2
    ) as market_share_pct,

    row_number() over (order by p.total_revenue_estimate desc) as revenue_rank,
    row_number() over (order by p.avg_metacritic_score desc) as quality_rank

from publishers p
cross join total_market tm
order by p.total_revenue_estimate desc
