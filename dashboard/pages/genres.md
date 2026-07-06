# Genre Analytics

Genre size matters, but normalized performance matters more. A crowded genre is not automatically an efficient one.

> Revenue is a proxy based on owner ranges and price, and genre totals can overcount because multi-genre games contribute to more than one bucket.

```sql genre_stats
select
    genre,
    game_count,
    avg_price,
    avg_review_count,
    avg_playtime,
    total_revenue_estimate,
    round(total_revenue_estimate / nullif(game_count, 0), 2) as revenue_per_game,
    avg_review_count as reviews_per_game,
    avg_playtime as playtime_per_game,
    popularity_rank
from steam_games.genre_analytics
order by game_count desc
```

<DataTable data={genre_stats} rows=20 title="Genre Statistics">
    <Column id=genre title="Genre" />
    <Column id=game_count title="Games" />
    <Column id=avg_price title="Avg Price" fmt=usd />
    <Column id=avg_review_count title="Avg Reviews" />
    <Column id=avg_playtime title="Avg Playtime (min)" />
    <Column id=total_revenue_estimate title="Est. Revenue" fmt=usd0 />
    <Column id=revenue_per_game title="Revenue per Game" fmt=usd0 />
    <Column id=reviews_per_game title="Reviews per Game" />
    <Column id=playtime_per_game title="Playtime per Game" />
    <Column id=popularity_rank title="Rank" />
</DataTable>

## Scale And Market Density

<BarChart
    data={genre_stats}
    x=genre
    y=game_count
    xAxisTitle="Genre"
    yAxisTitle="Games"
    swapXY=true
    title="Games per Genre"
/>

## Efficiency Versus Volume

```sql genre_efficiency
select
    genre,
    game_count,
    avg_price,
    avg_review_count as reviews_per_game,
    round(total_revenue_estimate / nullif(game_count, 0), 2) as revenue_per_game
from steam_games.genre_analytics
where game_count >= 25
order by revenue_per_game desc
```

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem; margin: 1.5rem 0 2rem;">

<BarChart
    data={genre_efficiency}
    x=genre
    y=revenue_per_game
    xAxisTitle="Genre"
    yAxisTitle="Revenue per Game"
    swapXY=true
    title="Revenue per Game by Genre"
/>

<BarChart
    data={genre_efficiency}
    x=genre
    y=reviews_per_game
    xAxisTitle="Genre"
    yAxisTitle="Reviews per Game"
    swapXY=true
    title="Reviews per Game by Genre"
/>

</div>

<ScatterPlot
    data={genre_efficiency}
    x=avg_price
    y=reviews_per_game
    xAxisTitle="Average Price"
    yAxisTitle="Reviews per Game"
    title="Genre Price vs Attention Density"
/>
