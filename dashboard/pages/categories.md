<div class="page-header">
  <div class="page-kicker">Product Shape</div>
  <h1>Categories And Tags</h1>
  <p class="page-lead">This view uses Steam category-style metadata such as single-player, multi-player, co-op, controller support, and achievements. It is narrower than genre analysis and better for understanding product shape.</p>
</div>

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

<div class="panel panel-soft">
<div class="section-kicker">Category Table</div>
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

<p class="section-lead">These counts show which product features dominate the Steam catalog. They are useful for understanding how common multiplayer, controller support, or achievement-heavy packaging really is.</p>

```sql category_scale
select category, game_count
from steam_games.category_analytics
order by game_count desc
limit 20
```

<div class="panel panel-cool panel-soft">
<div class="section-kicker">Feature Distribution</div>
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

<p class="section-lead">The more interesting question is whether those categories also pull higher revenue and stronger review density per game.</p>

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

<div class="panel panel-accent panel-soft">
<div class="section-kicker">Commercial Density</div>
<div class="panel-grid">

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
</div>

<div class="panel panel-warm panel-soft">
<div class="section-kicker">Price Versus Attention</div>
<ScatterPlot
    data={category_efficiency}
    x=avg_price
    y=reviews_per_game
    xAxisTitle="Average Price"
    yAxisTitle="Reviews per Game"
    title="Category Price vs Attention Density"
/>
</div>
