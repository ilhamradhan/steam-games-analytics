<div class="homepage-hero">
  <div class="homepage-hero-grid">
    <div class="homepage-hero-copy">
      <div class="page-kicker">Steam Marketplace Lens</div>
      <h1>Steam Games Analytics</h1>

      <p class="page-lead">A compact view of the Steam catalog: size, pricing, platform reach, and how quality signals distribute across 124k+ titles.</p>

      <p class="section-lead">This homepage is built to answer the first-order questions first: how large the market is, how concentrated ownership looks, how free and paid titles split, and how much of the catalog sits in the breakout layer rather than the long tail.</p>
    </div>

    <div class="homepage-side-stack">
      <div class="homepage-side-card">
        <strong>Coverage</strong>
        <p>Tracks the catalog before drilling into genres, publishers, developers, categories, and audience behavior.</p>
      </div>
      <div class="homepage-side-card">
        <strong>Read Order</strong>
        <p>Start here for market shape, then move into company, studio, category, and audience views for more specific cuts.</p>
      </div>
    </div>
  </div>
</div>

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

<div class="panel panel-soft">
<div class="section-kicker">Topline Snapshot</div>
<div class="stats-grid">

<div class="stat-card">
<BigValue
    data={game_count}
    value=total
    title="Games Tracked"
/>
</div>

<div class="stat-card">
<BigValue
    data={avg_price}
    value=avg_price
    title="Average Paid Price"
    subtitle="USD"
/>
</div>

<div class="stat-card">
<BigValue
    data={genre_count}
    value=genres
    title="Genres"
    subtitle="Represented"
/>
</div>

<div class="stat-card">
<BigValue
    data={featured_title}
    value=game_name
    title="Featured Title"
    subtitle="Top critic score with review depth"
/>
</div>

</div>
</div>

## Market Snapshot

<p class="section-lead">The catalog is heavily skewed toward long-tail titles, so the most useful top-level cuts are ownership scale, pricing model, and platform breadth.</p>

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

<div class="panel panel-soft">
<div class="section-kicker">Ownership Distribution</div>
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

<div class="panel panel-cool panel-soft">
<div class="section-kicker">Catalog Structure</div>
<div class="panel-grid">

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
</div>

## Quality And Engagement Signals

<p class="section-lead">Success and engagement are both heuristic summaries here, but they still show how much of the catalog sits in the tail versus the breakout layer.</p>

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

<div class="panel panel-accent panel-soft">
<div class="section-kicker">Breakout Layer</div>
<div class="panel-grid">

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
</div>
