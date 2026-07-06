# Categories And Tags

This view uses Steam category-style metadata such as single-player, multi-player, co-op, controller support, and achievements. It is narrower than genre analysis and better for understanding product shape.

> **How this is calculated**
>
> Estimated revenue is the midpoint of a game's owner range multiplied by its current listed price.
> Category totals are directional because a game can belong to many categories at once.

```sql category_stats
select
    category,
    game_count,
    avg_price,
    avg_review_count,
    avg_playtime,
    total_revenue_estimate,
    round(total_revenue_estimate / nullif(game_count, 0), 2) as revenue_per_game,
    avg_review_count as reviews_per_game,
    avg_playtime as playtime_per_game
from steam_games.category_analytics
order by game_count desc
```

<div style="margin: 1.25rem 0 2rem; padding: 1.15rem 1.2rem 1.25rem; border: 1px solid rgba(138, 173, 244, 0.15); border-radius: 16px; background: rgba(54, 58, 79, 0.28);">
<DataTable data={category_stats} rows=20 title="Category Statistics">
    <Column id=category title="Category" />
    <Column id=game_count title="Games" />
    <Column id=avg_price title="Avg Price" fmt=usd />
    <Column id=avg_review_count title="Avg Reviews" />
    <Column id=avg_playtime title="Avg Playtime (min)" />
    <Column id=total_revenue_estimate title="Est. Revenue" fmt=usd0 />
    <Column id=revenue_per_game title="Revenue per Game" fmt=usd0 />
    <Column id=reviews_per_game title="Reviews per Game" />
    <Column id=playtime_per_game title="Playtime per Game" />
</DataTable>
</div>

## Product Shape Distribution

These counts show which product features dominate the Steam catalog. They are useful for understanding how common multiplayer, controller support, or achievement-heavy packaging really is.

```sql category_scale
select category, game_count
from steam_games.category_analytics
order by game_count desc
limit 20
```

<div style="margin: 1rem 0 1.85rem; padding: 1.05rem 1.15rem 1.2rem; border: 1px solid rgba(145, 215, 227, 0.14); border-radius: 16px; background: rgba(54, 58, 79, 0.22);">
<BarChart
    data={category_scale}
    x=category
    y=game_count
    xAxisTitle="Category"
    yAxisTitle="Games"
    swapXY=true
    title="Top Categories by Game Count"
/>
</div>

## Commercial And Attention Density

The more interesting question is whether those categories also pull higher revenue and stronger review density per game.

```sql category_efficiency
select
    category,
    game_count,
    avg_price,
    avg_review_count as reviews_per_game,
    round(total_revenue_estimate / nullif(game_count, 0), 2) as revenue_per_game
from steam_games.category_analytics
where game_count >= 25
order by revenue_per_game desc
```

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem; margin: 1.5rem 0 2rem; padding: 1.1rem 1.2rem 1.25rem; border: 1px solid rgba(198, 160, 246, 0.14); border-radius: 16px; background: rgba(54, 58, 79, 0.24);">

<BarChart
    data={category_efficiency}
    x=category
    y=revenue_per_game
    xAxisTitle="Category"
    yAxisTitle="Revenue per Game"
    swapXY=true
    title="Revenue per Game by Category"
/>

<BarChart
    data={category_efficiency}
    x=category
    y=reviews_per_game
    xAxisTitle="Category"
    yAxisTitle="Reviews per Game"
    swapXY=true
    title="Reviews per Game by Category"
/>

</div>

<div style="margin: 0.5rem 0 1.85rem; padding: 1.05rem 1.15rem 1.2rem; border: 1px solid rgba(245, 169, 127, 0.14); border-radius: 16px; background: rgba(54, 58, 79, 0.2);">
<ScatterPlot
    data={category_efficiency}
    x=avg_price
    y=reviews_per_game
    xAxisTitle="Average Price"
    yAxisTitle="Reviews per Game"
    title="Category Price vs Attention Density"
/>
</div>
