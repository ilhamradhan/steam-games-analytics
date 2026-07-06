# Publisher Rankings

Publisher tables can look clean while hiding concentration and attribution issues. The views below keep the ranking but add quality, attention, and market-share context.

> Revenue and market share are directional metrics here. Co-published games can be counted under more than one publisher.

```sql publisher_stats
select
    publisher,
    game_count,
    avg_price,
    avg_metacritic_score,
    avg_user_score,
    total_reviews,
    total_recommendations,
    avg_playtime,
    total_revenue_estimate,
    market_share_pct,
    market_share_pct / 100.0 as market_share_share,
    revenue_rank,
    quality_rank
from steam_games.publisher_rankings
where revenue_rank <= 50
order by revenue_rank
```

<DataTable data={publisher_stats} rows=25 title="Top 50 Publishers">
    <Column id=publisher title="Publisher" />
    <Column id=game_count title="Games" />
    <Column id=avg_price title="Avg Price" fmt=usd />
    <Column id=avg_metacritic_score title="Avg Metacritic" />
    <Column id=avg_user_score title="Avg User Score" />
    <Column id=total_reviews title="Total Reviews" />
    <Column id=total_recommendations title="Recommendations" />
    <Column id=avg_playtime title="Avg Playtime (min)" />
    <Column id=total_revenue_estimate title="Est. Revenue" fmt=usd0 />
    <Column id=market_share_share title="Market Share" fmt=pct />
    <Column id=revenue_rank title="Revenue Rank" />
    <Column id=quality_rank title="Quality Rank" />
</DataTable>

## Revenue Concentration

```sql top_publishers
select publisher, total_revenue_estimate
from steam_games.publisher_rankings
where revenue_rank <= 20
order by total_revenue_estimate desc
```

```sql market_share_leaders
select publisher, market_share_pct
from steam_games.publisher_rankings
where revenue_rank <= 15
order by market_share_pct desc
```

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem; margin: 1.5rem 0 2rem;">

<BarChart
    data={top_publishers}
    x=publisher
    y=total_revenue_estimate
    xAxisTitle="Publisher"
    yAxisTitle="Est. Revenue"
    swapXY=true
    title="Top 20 Publishers by Revenue"
/>

<BarChart
    data={market_share_leaders}
    x=publisher
    y=market_share_pct
    xAxisTitle="Publisher"
    yAxisTitle="Market Share (%)"
    swapXY=true
    title="Top 15 Publishers by Market Share"
/>

</div>

## Quality Versus Scale

The useful comparison is broad, not just a handpicked top slice. This view keeps only publishers with enough catalog depth to be comparable.

```sql quality_volume
select
    publisher,
    game_count,
    avg_user_score,
    avg_metacritic_score,
    total_revenue_estimate
from steam_games.publisher_rankings
where game_count >= 5
  and avg_user_score > 0
order by total_revenue_estimate desc
limit 100
```

<ScatterPlot
    data={quality_volume}
    x=game_count
    y=avg_user_score
    xAxisTitle="Number of Games"
    yAxisTitle="Avg User Score"
    title="Publisher Scale vs User Reception"
/>
