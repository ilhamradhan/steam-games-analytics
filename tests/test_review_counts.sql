select
    appid,
    game_name,
    positive_count,
    negative_count,
    positive_count + negative_count as total_reviews
from {{ ref('stg_games__with_scores') }}
where positive_count < 0 or negative_count < 0
