select
    appid,
    game_name,
    release_date
from {{ ref('stg_games__cleaned') }}
where release_date is not null
  and (
    release_date > current_date()
    or release_date < '2003-09-12'::date
  )
