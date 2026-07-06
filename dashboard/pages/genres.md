# Genre Analytics

Genre size matters, but normalized performance matters more. A crowded genre is not automatically an efficient one.

> **How this is calculated**
>
> Estimated revenue is the midpoint of a game's owner range multiplied by its current listed price.
> Genre totals are directional because a multi-genre game contributes to every genre it belongs to.

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

This first cut shows where the catalog is crowded. The next section focuses on whether that scale turns into stronger monetization or attention density.

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

These comparisons are more useful than raw size alone because they normalize large genre buckets and surface where attention is denser.

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
