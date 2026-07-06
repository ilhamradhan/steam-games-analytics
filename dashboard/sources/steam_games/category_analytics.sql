with categories as (
    select * from dev_intermediate.int_games__flattened_tags
),

games as (
    select
        appid,
        price,
        review_count,
        avg_playtime,
        revenue_estimate
    from dev_marts.mart_games_performance
)

select
    c.category,
    count(distinct c.appid) as game_count,
    round(avg(g.price), 2) as avg_price,
    round(avg(g.review_count), 0)::bigint as avg_review_count,
    round(avg(g.avg_playtime), 0)::bigint as avg_playtime,
    round(sum(g.revenue_estimate), 2) as total_revenue_estimate
from categories c
left join games g on c.appid = g.appid
group by c.category
order by game_count desc
