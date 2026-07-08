<div class="page-header">
  <div class="page-kicker">Audience View</div>
  <h1>Engagement Segments</h1>

  <p class="page-lead">These tiers separate breakout games from the long tail. The useful question is not only where games land, but how much attention and value each segment captures.</p>
</div>

> **How this is calculated**
>
> Engagement tiers are heuristic buckets.
> `viral` requires recommendations > 1000, positive reviews > 500, and average playtime > 1000 minutes.
> `popular` requires positive reviews > 100 and total reviews > 200.
> `moderate` means at least 10 reviews, `low` means 1-9 reviews, and `none` means no review activity.

```sql segment_summary
with totals as (
    select
        count(*) as total_games,
        sum(review_count) as total_reviews
    from steam_games.game_performance
)
select
    gp.engagement_tier,
    count(*) as game_count,
    round(count(*) * 100.0 / max(t.total_games), 2) as share_of_games_pct,
    round(avg(gp.price), 2) as avg_price,
    round(avg(gp.sentiment_ratio), 3) as avg_sentiment_ratio,
    round(avg(gp.avg_playtime), 0)::bigint as avg_playtime,
    round(sum(gp.review_count), 0) as total_reviews,
    round(sum(gp.review_count) * 100.0 / nullif(max(t.total_reviews), 0), 2) as share_of_reviews_pct,
    round(sum(gp.revenue_estimate), 2) as total_revenue_estimate
from steam_games.game_performance gp
cross join totals t
group by gp.engagement_tier
order by
    case gp.engagement_tier
        when 'viral' then 1
        when 'popular' then 2
        when 'moderate' then 3
        when 'low' then 4
        when 'none' then 5
    end
```

<div class="panel panel-cool">
<div class="section-kicker">Segment Table</div>
<DataTable data={segment_summary} title="Engagement Segment Summary">
    <Column id=engagement_tier title="Segment" />
    <Column id=game_count title="Games" />
    <Column id=share_of_games_pct title="Share of Games (%)" />
    <Column id=avg_price title="Avg Price" fmt=usd />
    <Column id=avg_sentiment_ratio title="Avg Sentiment" fmt=pct />
    <Column id=avg_playtime title="Avg Playtime (min)" />
    <Column id=total_reviews title="Total Reviews" />
    <Column id=share_of_reviews_pct title="Share of Reviews (%)" />
    <Column id=total_revenue_estimate title="Est. Revenue" fmt=usd0 />
</DataTable>
</div>

## Where Attention Concentrates

<p class="section-lead">Review share moves much faster than game share. That makes the segment chart more informative than raw counts alone.</p>

<div class="panel panel-cool panel-soft">
<div class="section-kicker">Attention Concentration</div>
<div class="panel-grid">

<BarChart
    data={segment_summary}
    x=engagement_tier
    y=share_of_games_pct
    xAxisTitle="Engagement Tier"
    yAxisTitle="Share of Games (%)"
    title="Catalog Share by Tier"
/>

<BarChart
    data={segment_summary}
    x=engagement_tier
    y=share_of_reviews_pct
    xAxisTitle="Engagement Tier"
    yAxisTitle="Share of Reviews (%)"
    title="Attention Share by Tier"
/>

</div>
</div>

## Segment Economics

<p class="section-lead">Higher tiers are not just louder. They also pull up sentiment, playtime, and monetization proxies.</p>

> Revenue on this page uses the same directional proxy as the publisher and genre views:
> owner-range midpoint times current listed price.

<div class="panel panel-soft">
<div class="section-kicker">Segment Economics</div>
<div class="panel-grid">

<BarChart
    data={segment_summary}
    x=engagement_tier
    y=avg_sentiment_ratio
    xAxisTitle="Engagement Tier"
    yAxisTitle="Average Sentiment"
    title="Average Sentiment by Tier"
/>

<BarChart
    data={segment_summary}
    x=engagement_tier
    y=avg_playtime
    xAxisTitle="Engagement Tier"
    yAxisTitle="Average Playtime (min)"
    title="Average Playtime by Tier"
/>

</div>
</div>

## Standout Games Within Each Tier

```sql top_per_segment
with ranked as (
    select
        game_name,
        engagement_tier,
        review_count,
        price,
        sentiment_ratio,
        recommendations,
        avg_playtime,
        row_number() over (partition by engagement_tier order by review_count desc, recommendations desc) as rn
    from steam_games.game_performance
    where review_count > 0
)
select
    game_name,
    engagement_tier,
    review_count,
    price,
    sentiment_ratio,
    recommendations,
    avg_playtime
from ranked
where rn <= 5
order by
    case engagement_tier
        when 'viral' then 1
        when 'popular' then 2
        when 'moderate' then 3
        when 'low' then 4
        when 'none' then 5
    end,
    review_count desc
```

<div style="margin: 1.25rem 0 2rem; padding: 1.15rem 1.2rem 1.25rem; border: 1px solid rgba(198, 160, 246, 0.14); border-radius: 5px; background: rgba(36, 39, 58, 0.1);">
<DataTable data={top_per_segment} rows=30 title="Top 5 Games Per Segment">
    <Column id=game_name title="Game Name" />
    <Column id=engagement_tier title="Segment" />
    <Column id=review_count title="Reviews" />
    <Column id=price title="Price" fmt=usd />
    <Column id=sentiment_ratio title="Sentiment" fmt=pct />
    <Column id=recommendations title="Recommendations" />
    <Column id=avg_playtime title="Avg Playtime (min)" />
</DataTable>
</div>
