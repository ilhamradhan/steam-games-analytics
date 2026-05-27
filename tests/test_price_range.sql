select
    appid,
    game_name,
    price
from {{ ref('stg_games__cleaned') }}
where price < 0 or price > 2000
