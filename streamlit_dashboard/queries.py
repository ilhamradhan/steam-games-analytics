"""Reusable SQL queries for the Streamlit dashboard."""

# ── Overview ───────────────────────────────────────────────

OVERVIEW_KPIS = """
    select
        count(*)                                          as total_games,
        round(avg(case when price > 0 then price end), 2) as avg_paid_price,
        (select count(distinct genre) from dev_marts.mart_genres_analytics) as genre_count
    from dev_marts.mart_games_performance
"""

OWNER_BANDS = """
    select
        estimated_owners,
        count(*) as game_count
    from dev_marts.mart_games_performance
    group by estimated_owners
    order by
        case estimated_owners
            when '0 - 20000' then 1  when '20000 - 50000' then 2
            when '50000 - 100000' then 3  when '100000 - 200000' then 4
            when '200000 - 500000' then 5  when '500000 - 1000000' then 6
            when '1000000 - 2000000' then 7  when '2000000 - 5000000' then 8
            when '5000000 - 10000000' then 9  when '10000000 - 20000000' then 10
            when '20000000 - 50000000' then 11  when '50000000 - 100000000' then 12
            when '100000000 - 200000000' then 13
            else 14
        end
"""

PRICING_MIX = """
    select
        case when price = 0 then 'free' else 'paid' end as pricing_model,
        count(*) as game_count
    from dev_marts.mart_games_performance
    group by 1
    order by case pricing_model when 'free' then 1 else 2 end
"""

PLATFORM_MIX = """
    select
        case platform_count
            when 1 then 'single platform'
            when 2 then 'two platforms'
            when 3 then 'three platforms'
        end as platform_reach,
        count(*) as game_count
    from dev_marts.mart_games_performance
    group by 1, platform_count
    order by platform_count
"""

ENGAGEMENT_BREAKDOWN = """
    select engagement_tier, count(*) as game_count
    from dev_marts.mart_games_performance
    group by engagement_tier
    order by
        case engagement_tier
            when 'viral' then 1 when 'popular' then 2
            when 'moderate' then 3 when 'low' then 4 when 'none' then 5
        end
"""

SUCCESS_BREAKDOWN = """
    select success_indicator, count(*) as game_count
    from dev_marts.mart_games_performance
    group by success_indicator
    order by
        case success_indicator
            when 'blockbuster' then 1 when 'strong' then 2
            when 'mixed' then 3 when 'weak' then 4 when 'unrated' then 5
        end
"""

FEATURED_TITLE = """
    select game_name
    from dev_marts.mart_games_performance
    where metacritic_score > 0 and review_count >= 500
    order by metacritic_score desc, review_count desc, recommendations desc
    limit 1
"""

# ── Genres ────────────────────────────────────────────────

GENRE_STATS = """
    select
        genre,
        game_count,
        avg_price,
        avg_review_count,
        avg_playtime,
        total_revenue_estimate,
        round(total_revenue_estimate / nullif(game_count, 0), 2) as revenue_per_game,
        avg_review_count                                        as reviews_per_game,
        avg_playtime                                            as playtime_per_game,
        popularity_rank
    from dev_marts.mart_genres_analytics
    order by game_count desc
"""

GENRE_EFFICIENCY = """
    select
        genre,
        game_count,
        avg_price,
        avg_review_count as reviews_per_game,
        round(total_revenue_estimate / nullif(game_count, 0), 2) as revenue_per_game
    from dev_marts.mart_genres_analytics
    where game_count >= 25
    order by revenue_per_game desc
"""

# ── Publishers ────────────────────────────────────────────

PUBLISHER_RANKINGS = """
    select
        publisher, game_count, avg_price,
        avg_metacritic_score, avg_user_score,
        total_reviews, total_recommendations, avg_playtime,
        total_revenue_estimate, market_share_pct,
        market_share_pct / 100.0 as market_share_share,
        revenue_rank, quality_rank
    from dev_marts.mart_publishers_rankings
    where revenue_rank <= 50
    order by revenue_rank
"""

PUBLISHER_TOP_REVENUE = """
    select publisher, total_revenue_estimate
    from dev_marts.mart_publishers_rankings
    where revenue_rank <= 20
    order by total_revenue_estimate desc
"""

PUBLISHER_MARKET_SHARE = """
    select publisher, market_share_pct
    from dev_marts.mart_publishers_rankings
    where revenue_rank <= 15
    order by market_share_pct desc
"""

PUBLISHER_QUALITY_VOLUME = """
    select
        publisher, game_count, avg_user_score,
        avg_metacritic_score, total_revenue_estimate
    from dev_marts.mart_publishers_rankings
    where game_count >= 5 and avg_user_score > 0
    order by total_revenue_estimate desc
    limit 100
"""

# ── Engagement ────────────────────────────────────────────

ENGAGEMENT_SEGMENTS = """
    with totals as (
        select
            count(*) as total_games,
            sum(review_count) as total_reviews
        from dev_marts.mart_games_performance
    )
    select
        gp.engagement_tier,
        count(*)                                                      as game_count,
        round(count(*) * 100.0 / max(t.total_games), 2)              as share_of_games_pct,
        round(avg(gp.price), 2)                                       as avg_price,
        round(avg(gp.sentiment_ratio), 3)                             as avg_sentiment_ratio,
        round(avg(gp.avg_playtime), 0)                                as avg_playtime,
        round(sum(gp.review_count), 0)                                as total_reviews,
        round(sum(gp.review_count) * 100.0 / nullif(max(t.total_reviews), 0), 2) as share_of_reviews_pct,
        round(sum(gp.revenue_estimate), 2)                            as total_revenue_estimate
    from dev_marts.mart_games_performance gp
    cross join totals t
    group by gp.engagement_tier
    order by
        case gp.engagement_tier
            when 'viral' then 1 when 'popular' then 2
            when 'moderate' then 3 when 'low' then 4 when 'none' then 5
        end
"""

TOP_GAMES_PER_SEGMENT = """
    with ranked as (
        select
            game_name, engagement_tier, review_count,
            price, sentiment_ratio, recommendations, avg_playtime,
            row_number() over (
                partition by engagement_tier
                order by review_count desc, recommendations desc
            ) as rn
        from dev_marts.mart_games_performance
        where review_count > 0
    )
    select game_name, engagement_tier, review_count,
           price, sentiment_ratio, recommendations, avg_playtime
    from ranked
    where rn <= 5
    order by
        case engagement_tier
            when 'viral' then 1 when 'popular' then 2
            when 'moderate' then 3 when 'low' then 4 when 'none' then 5
        end,
        review_count desc
"""

# ── Developers ────────────────────────────────────────────

DEVELOPER_STATS = """
    select
        developer, game_count, avg_price,
        avg_metacritic_score, avg_user_score,
        total_reviews, total_recommendations, avg_playtime,
        total_revenue_estimate,
        row_number() over (order by total_revenue_estimate desc) as revenue_rank
    from dev_intermediate.int_developer_aggregates
    where total_reviews > 0
    qualify revenue_rank <= 50
    order by revenue_rank
"""

DEV_REVENUE_LEADERS = """
    select developer, total_revenue_estimate
    from dev_intermediate.int_developer_aggregates
    where total_reviews > 0
    order by total_revenue_estimate desc limit 20
"""

DEV_REVIEW_LEADERS = """
    select developer, total_reviews
    from dev_intermediate.int_developer_aggregates
    where total_reviews > 0
    order by total_reviews desc limit 20
"""

DEV_QUALITY_SCALE = """
    select developer, game_count, avg_user_score,
           avg_metacritic_score, total_revenue_estimate
    from dev_intermediate.int_developer_aggregates
    where game_count >= 3 and avg_user_score > 0
    order by total_revenue_estimate desc limit 100
"""

# ── Categories ────────────────────────────────────────────

CATEGORY_STATS = """
    with cat_games as (
        select * from dev_intermediate.int_games__flattened_tags
    ),
    game_metrics as (
        select appid, price, review_count, avg_playtime, revenue_estimate
        from dev_marts.mart_games_performance
    )
    select
        c.category,
        count(distinct c.appid)                           as game_count,
        round(avg(g.price), 2)                            as avg_price,
        round(avg(g.review_count), 0)                     as avg_review_count,
        round(avg(g.avg_playtime), 0)                     as avg_playtime,
        round(sum(g.revenue_estimate), 2)                 as total_revenue_estimate
    from cat_games c
    left join game_metrics g on c.appid = g.appid
    group by c.category
    order by game_count desc
"""

CATEGORY_SCALE = """
    with cat_games as (
        select * from dev_intermediate.int_games__flattened_tags
    )
    select category, count(distinct appid) as game_count
    from cat_games
    group by category
    order by game_count desc
    limit 20
"""

CATEGORY_EFFICIENCY = """
    with cat_games as (
        select * from dev_intermediate.int_games__flattened_tags
    ),
    game_metrics as (
        select appid, price, review_count, revenue_estimate
        from dev_marts.mart_games_performance
    )
    select
        c.category,
        count(distinct c.appid)                           as game_count,
        round(avg(g.price), 2)                            as avg_price,
        round(avg(g.review_count), 0)                     as reviews_per_game,
        round(sum(g.revenue_estimate)
              / nullif(count(distinct c.appid), 0), 2)     as revenue_per_game
    from cat_games c
    left join game_metrics g on c.appid = g.appid
    group by c.category
    having game_count >= 25
    order by revenue_per_game desc
"""
