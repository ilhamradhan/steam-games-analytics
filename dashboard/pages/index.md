# Steam Games Analytics

```sql game_count
select count(*) as total from steam_games.game_performance
```

```sql avg_price
select round(avg(price), 2) as avg_price from steam_games.game_performance where price > 0
```

```sql top_rated
select game_name
from steam_games.game_performance
where metacritic_score > 0
order by metacritic_score desc
limit 1
```

```sql genre_count
select count(distinct genre) as genres from steam_games.genre_analytics
```

<BigValue
    data={game_count}
    value=total
    title="Games Tracked"
/>

<BigValue
    data={avg_price}
    value=avg_price
    title="Avg Price (USD)"
/>

<BigValue
    data={genre_count}
    value=genres
    title="Genres Represented"
/>

## Highest Rated Game

<BigValue
    data={top_rated}
    value=game_name
    title="Top by Metacritic"
/>

## Games by Engagement Tier

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

<BarChart
    data={engagement_breakdown}
    x=engagement_tier
    y=game_count
    xAxisTitle="Engagement Tier"
    yAxisTitle="Number of Games"
/>

## Games by Success Indicator

```sql success_breakdown
select success_indicator, count(*) as game_count
from steam_games.game_performance
group by success_indicator
```

<BarChart
    data={success_breakdown}
    x=success_indicator
    y=game_count
    xAxisTitle="Success Indicator"
    yAxisTitle="Number of Games"
/>
