# Steam Games Analytics

A compact view of the Steam catalog: size, pricing, platform reach, and how quality signals distribute across 124k+ titles.

> This overview is designed as a market scan. It emphasizes ownership scale, pricing structure,
> and top-level quality signals before drilling into genre, publisher, developer, and engagement detail.

```sql game_count
select count(*) as total from steam_games.game_performance
```

```sql avg_price
select round(avg(price), 2) as avg_price
from steam_games.game_performance
where price > 0
```

```sql genre_count
select count(distinct genre) as genres from steam_games.genre_analytics
```

```sql featured_title
select game_name
from steam_games.game_performance
where metacritic_score > 0
  and review_count >= 500
order by metacritic_score desc, review_count desc, recommendations desc
limit 1
```

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.5rem; margin: 2rem 0; padding: 1.2rem 1.25rem; border: 1px solid rgba(138, 173, 244, 0.16); border-radius: 16px; background: rgba(54, 58, 79, 0.32);">

<BigValue
    data={game_count}
    value=total
    title="Games Tracked"
/>

<BigValue
    data={avg_price}
    value=avg_price
    title="Average Paid Price"
    subtitle="USD"
/>

<BigValue
    data={genre_count}
    value=genres
    title="Genres"
    subtitle="Represented"
/>

<BigValue
    data={featured_title}
    value=game_name
    title="Featured Title"
    subtitle="Top critic score with review depth"
/>

</div>

## Market Snapshot

The catalog is heavily skewed toward long-tail titles, so the most useful top-level cuts are ownership scale, pricing model, and platform breadth.

```sql owner_band_mix
select
    estimated_owners,
    count(*) as game_count
from steam_games.game_performance
group by estimated_owners
order by
    case estimated_owners
        when '0 - 20000' then 1
        when '20000 - 50000' then 2
        when '50000 - 100000' then 3
        when '100000 - 200000' then 4
        when '200000 - 500000' then 5
        when '500000 - 1000000' then 6
        when '1000000 - 2000000' then 7
        when '2000000 - 5000000' then 8
        when '5000000 - 10000000' then 9
        when '10000000 - 20000000' then 10
        when '20000000 - 50000000' then 11
        when '50000000 - 100000000' then 12
        when '100000000 - 200000000' then 13
        else 14
    end
```

<div style="margin: 1.1rem 0 1.75rem; padding: 1.1rem 1.2rem 1.25rem; border: 1px solid rgba(138, 173, 244, 0.16); border-radius: 16px; background: rgba(54, 58, 79, 0.26);">
<BarChart
    data={owner_band_mix}
    x=estimated_owners
    y=game_count
    xAxisTitle="Estimated Owners"
    yAxisTitle="Games"
    title="Catalog Distribution by Ownership Band"
/>
</div>

```sql pricing_mix
select
    case when price = 0 then 'free' else 'paid' end as pricing_model,
    count(*) as game_count
from steam_games.game_performance
group by 1
order by case pricing_model when 'free' then 1 else 2 end
```

```sql platform_mix
select
    case platform_count
        when 1 then 'single platform'
        when 2 then 'two platforms'
        when 3 then 'three platforms'
    end as platform_reach,
    count(*) as game_count
from steam_games.game_performance
group by 1, platform_count
order by platform_count
```

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem; margin: 1.5rem 0 2rem; padding: 1.1rem 1.2rem 1.25rem; border: 1px solid rgba(145, 215, 227, 0.14); border-radius: 16px; background: rgba(54, 58, 79, 0.22);">

<BarChart
    data={pricing_mix}
    x=pricing_model
    y=game_count
    xAxisTitle="Pricing Model"
    yAxisTitle="Games"
    title="Free vs Paid Catalog Split"
/>

<BarChart
    data={platform_mix}
    x=platform_reach
    y=game_count
    xAxisTitle="Platform Reach"
    yAxisTitle="Games"
    title="Platform Support Breadth"
/>

</div>

## Quality And Engagement Signals

Success and engagement are both heuristic summaries here, but they still show how much of the catalog sits in the tail versus the breakout layer.

> **How to read this**
>
> `success_indicator` is driven by critic score and sentiment, while `engagement_tier`
> is a heuristic based on reviews, recommendations, and playtime. These are summary signals,
> not official Steam labels.

```sql engagement_breakdown
select engagement_tier, count(*) as game_count
from steam_games.game_performance
group by engagement_tier
order by
    case engagement_tier
        when 'viral' then 1
        when 'popular' then 2
        when 'moderate' then 3
        when 'low' then 4
        when 'none' then 5
    end
```
 
```sql success_breakdown
select success_indicator, count(*) as game_count
from steam_games.game_performance
group by success_indicator
order by
    case success_indicator
        when 'blockbuster' then 1
        when 'strong' then 2
        when 'mixed' then 3
        when 'weak' then 4
        when 'unrated' then 5
    end
```

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem; margin: 1.5rem 0 2rem; padding: 1.1rem 1.2rem 1.25rem; border: 1px solid rgba(198, 160, 246, 0.14); border-radius: 16px; background: rgba(54, 58, 79, 0.24);">

<BarChart
    data={engagement_breakdown}
    x=engagement_tier
    y=game_count
    xAxisTitle="Engagement Tier"
    yAxisTitle="Games"
    title="Games by Engagement Tier"
/>

<BarChart
    data={success_breakdown}
    x=success_indicator
    y=game_count
    xAxisTitle="Success Indicator"
    yAxisTitle="Games"
    title="Games by Success Indicator"
/>

</div>
