# Genre Analytics

```sql genre_stats
select
    genre,
    game_count,
    avg_price,
    avg_review_count,
    avg_playtime,
    total_revenue_estimate,
    popularity_rank
from steam_games.genre_analytics
order by game_count desc
```

<DataTable data={genre_stats} rows=20>
    <Column id=genre />
    <Column id=game_count />
    <Column id=avg_price fmt=usd />
    <Column id=avg_review_count />
    <Column id=avg_playtime title="Avg Playtime (min)" />
    <Column id=total_revenue_estimate title="Est. Revenue" fmt=usd2 />
    <Column id=popularity_rank />
</DataTable>

## Top Genres by Game Count

<BarChart
    data={genre_stats}
    x=genre
    y=game_count
    xAxisTitle="Genre"
    yAxisTitle="Number of Games"
    swapXY=true
/>

## Revenue by Genre

```sql genre_revenue
select genre, total_revenue_estimate
from steam_games.genre_analytics
where total_revenue_estimate > 0
order by total_revenue_estimate desc
limit 15
```

<BarChart
    data={genre_revenue}
    x=genre
    y=total_revenue_estimate
    xAxisTitle="Genre"
    yAxisTitle="Est. Revenue"
    swapXY=true
/>
