# Publisher Rankings

```sql publisher_stats
select
    publisher,
    game_count,
    avg_price,
    avg_metacritic_score,
    total_revenue_estimate,
    market_share_pct,
    revenue_rank
from steam_games.publisher_rankings
where revenue_rank <= 50
order by revenue_rank
```

<DataTable data={publisher_stats} rows=25>
    <Column id=publisher />
    <Column id=game_count />
    <Column id=avg_price fmt=usd />
    <Column id=avg_metacritic_score title="Avg Metacritic" />
    <Column id=total_revenue_estimate title="Est. Revenue" fmt=usd0 />
    <Column id=market_share_pct title="Share %" fmt=pct />
    <Column id=revenue_rank title="Rank" />
</DataTable>

## Revenue Distribution (Top 20)

```sql top_publishers
select publisher, total_revenue_estimate
from steam_games.publisher_rankings
where revenue_rank <= 20
order by total_revenue_estimate desc
```

<BarChart
    data={top_publishers}
    x=publisher
    y=total_revenue_estimate
    xAxisTitle="Publisher"
    yAxisTitle="Est. Revenue"
    swapXY=true
/>

## Quality vs Volume

```sql quality_volume
select
    publisher,
    game_count,
    avg_metacritic_score
from steam_games.publisher_rankings
where game_count >= 5
order by avg_metacritic_score desc
limit 20
```

<ScatterPlot
    data={quality_volume}
    x=game_count
    y=avg_metacritic_score
    xAxisTitle="Number of Games"
    yAxisTitle="Avg Metacritic Score"
/>
