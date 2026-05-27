# Steam Games Analytics

An analytics pipeline for Steam games data, built with dbt and DuckDB.

[![CI](https://github.com/ilhamradhan/steam-games-analytics/actions/workflows/dbt_run.yml/badge.svg)](https://github.com/ilhamradhan/steam-games-analytics/actions/workflows/dbt_run.yml)

## What this does

Takes the raw Steam games dataset from HuggingFace (124k+ games) and transforms it through three layers: staging, intermediate, and marts. The output is a set of clean, denormalized tables you can query directly or plug into a BI tool.

Each layer handles a specific job:

Staging models cast types, deduplicate rows, standardize column names, handle nulls, and compute normalized scores and review counts.

Intermediate models flatten array columns (genres, categories, developers, publishers) into one-row-per-value tables and calculate engagement metrics. A sentiment ratio, composite engagement score, and rough revenue estimates are all derived here.

Marts are the consumption layer. Four tables: game performance (one row per game, all metrics), genre analytics (aggregates per genre), publisher rankings (ranked by estimated revenue), and engagement segments (each game bucketed into viral, popular, moderate, low, or none).

An [Evidence dashboard](dashboard/) sits on top of the marts with charts for genre distribution, publisher rankings, and engagement breakdowns.

## Quick start

```bash
pip install -r requirements.txt
python load_steam_data.py
cp profiles.yml.example profiles.yml
dbt run
dbt test
```

## Data source

[FronkonGames/steam-games-dataset](https://huggingface.co/datasets/FronkonGames/steam-games-dataset) on HuggingFace. 124,146 Steam games with metadata, reviews, pricing, playtime stats, and platform support.

## Project structure

```
steam-games-analytics/
├── models/
│   ├── staging/           # 3 models: base, cleaned, scored
│   ├── intermediate/      # 5 models: flattened, engagement, aggregates
│   └── marts/             # 4 models: performance, genres, publishers, segments
├── dashboard/             # Evidence dashboard (npm run dev)
│   ├── pages/             # index, genres, publishers, engagement
│   └── sources/           # SQL queries against DuckDB marts
├── tests/
│   ├── test_review_counts.sql
│   ├── test_price_range.sql
│   ├── test_dates_logical.sql
│   └── generic/
├── .github/workflows/
│   └── dbt_run.yml
├── load_steam_data.py
├── dbt_project.yml
├── profiles.yml.example
└── requirements.txt
```

## Model lineage

```
raw_steam_games (source)
  └── stg_games__base
        └── stg_games__cleaned
              └── stg_games__with_scores
                    ├── int_games__flattened_genres
                    ├── int_games__flattened_tags
                    ├── int_games__with_engagement
                    │     ├── int_publisher_aggregates
                    │     └── int_developer_aggregates
                    └── (used by all marts)
                          ├── mart_games_performance
                          ├── mart_genres_analytics
                          ├── mart_publishers_rankings
                          └── mart_engagement_segments
```

## Key metrics

| Metric | Description |
|--------|------------|
| `sentiment_ratio` | Positive reviews / total reviews |
| `engagement_tier` | viral, popular, moderate, low, or none |
| `metacritic_tier` | excellent (85+), good (70+), ok (50+), poor, or unrated |
| `success_indicator` | blockbuster, strong, mixed, weak, or unrated |
| `revenue_estimate` | Midpoint of owner range multiplied by price |
| `market_share_pct` | Publisher's share of total estimated market revenue |

## Testing

24 data tests run across every layer. Generic tests cover not-null constraints on key fields (appid, game_name, genre, publisher), uniqueness on appid in staging and marts, and accepted values on score tiers, engagement tiers, and success indicators. Singular tests validate that review counts are non-negative, prices fall within a sensible range, and release dates are logical (not in the future, not before 2003).

```bash
dbt test   # 24/24 pass
```

## Dashboard

```bash
cd dashboard
npm install
npm run sources
npm run dev
```

Opens at `localhost:3000` with four pages:

- Overview. KPIs (games tracked, avg price, genres), engagement tier breakdown, success indicator distribution.
- Genres. Data table and bar charts for game counts and revenue by genre.
- Publishers. Ranked by estimated revenue, top 20 revenue chart, quality vs volume scatter plot.
- Engagement. Segment summaries, review totals per segment, top games per tier.

Deploy to GitHub Pages or any static host with `npm run build`.

## Tech stack

dbt 1.11 for transformations, DuckDB 1.5 as the embedded database, Python 3.12 for data loading, Evidence for the dashboard, and GitHub Actions for CI.

## License

MIT
