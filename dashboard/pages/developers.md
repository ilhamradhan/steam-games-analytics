# Developer Analytics

Developer performance is often clearer than publisher performance because the creative footprint stays closer to the game itself. This page focuses on scale, player response, and concentration across studios.

> **How this is calculated**
>
> Estimated revenue is the midpoint of owner range multiplied by current listed price.
> Developer totals are directional because co-developed games can contribute to more than one studio.

```sql developer_stats
select
    developer,
    game_count,
    avg_price,
    avg_metacritic_score,
    avg_user_score,
    total_reviews,
    total_recommendations,
    avg_playtime,
    total_revenue_estimate,
    row_number() over (order by total_revenue_estimate desc) as revenue_rank
from steam_games.developer_analytics
where total_reviews > 0
qualify revenue_rank <= 50
order by revenue_rank
```

<div style="margin: 1.25rem 0 2rem; padding: 1.15rem 1.2rem 1.25rem; border: 1px solid rgba(138, 173, 244, 0.15); border-radius: 5px; background: rgba(36, 39, 58, 0.14);">
<DataTable data={developer_stats} rows=25 title="Top 50 Developers">
    <Column id=developer title="Developer" />
    <Column id=game_count title="Games" />
    <Column id=avg_price title="Avg Price" fmt=usd />
    <Column id=avg_metacritic_score title="Avg Metacritic" />
    <Column id=avg_user_score title="Avg User Score" />
    <Column id=total_reviews title="Total Reviews" />
    <Column id=total_recommendations title="Recommendations" />
    <Column id=avg_playtime title="Avg Playtime (min)" />
    <Column id=total_revenue_estimate title="Est. Revenue" fmt=usd0 />
    <Column id=revenue_rank title="Revenue Rank" />
</DataTable>
</div>

## Revenue Leaders

The revenue view shows which studios anchor the catalog's largest breakout games. It works best as a relative ranking, not as audited studio revenue.

```sql top_developers
select developer, total_revenue_estimate
from steam_games.developer_analytics
where total_reviews > 0
order by total_revenue_estimate desc
limit 20
```

```sql review_leaders
select developer, total_reviews
from steam_games.developer_analytics
where total_reviews > 0
order by total_reviews desc
limit 20
```

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem; margin: 1.5rem 0 2rem; padding: 1.1rem 1.2rem 1.25rem; border: 1px solid rgba(145, 215, 227, 0.14); border-radius: 5px; background: rgba(36, 39, 58, 0.1);">

<BarChart
    data={top_developers}
    x=developer
    y=total_revenue_estimate
    xAxisTitle="Developer"
    yAxisTitle="Est. Revenue"
    swapXY=true
    title="Top 20 Developers by Revenue"
/>

<BarChart
    data={review_leaders}
    x=developer
    y=total_reviews
    xAxisTitle="Developer"
    yAxisTitle="Total Reviews"
    swapXY=true
    title="Top 20 Developers by Review Volume"
/>

</div>

## Quality Versus Scale

This comparison highlights whether larger studios also maintain stronger player reception, or whether quality clusters around smaller catalogs.

```sql developer_quality
select
    developer,
    game_count,
    avg_user_score,
    avg_metacritic_score,
    total_revenue_estimate
from steam_games.developer_analytics
where game_count >= 3
  and avg_user_score > 0
order by total_revenue_estimate desc
limit 100
```

<div style="margin: 1rem 0 1.85rem; padding: 1.05rem 1.15rem 1.2rem; border: 1px solid rgba(198, 160, 246, 0.14); border-radius: 5px; background: rgba(36, 39, 58, 0.1);">
<ScatterPlot
    data={developer_quality}
    x=game_count
    y=avg_user_score
    xAxisTitle="Number of Games"
    yAxisTitle="Avg User Score"
    title="Developer Scale vs User Reception"
/>
</div>
