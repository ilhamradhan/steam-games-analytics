# Engagement Segments

```sql segment_summary
select
    engagement_tier,
    count(*) as game_count,
    round(avg(price), 2) as avg_price,
    round(sum(review_count), 0) as total_reviews
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

<DataTable data={segment_summary}>
    <Column id=engagement_tier title="Segment" />
    <Column id=game_count />
    <Column id=avg_price fmt=usd />
    <Column id=total_reviews />
</DataTable>

## Reviews by Segment

<BarChart
    data={segment_summary}
    x=engagement_tier
    y=total_reviews
    xAxisTitle="Engagement Segment"
    yAxisTitle="Total Reviews"
/>

## Top Games by Reviews Per Segment

```sql top_per_segment
with ranked as (
    select
        game_name,
        engagement_tier,
        review_count,
        row_number() over (partition by engagement_tier order by review_count desc) as rn
    from steam_games.game_performance
    where review_count > 0
)
select game_name, engagement_tier, review_count
from ranked
where rn <= 5
order by
    case engagement_tier
        when 'viral' then 1
        when 'popular' then 2
        when 'moderate' then 3
        when 'low' then 4
        when 'none' then 5
    end, review_count desc
```

<DataTable data={top_per_segment} rows=30>
    <Column id=game_name />
    <Column id=engagement_tier />
    <Column id=review_count />
</DataTable>
