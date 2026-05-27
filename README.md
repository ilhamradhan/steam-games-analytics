# Steam Games Analytics — dbt Project

End-to-end analytics pipeline for Steam games data using **dbt** and **DuckDB**.

[![CI](https://github.com/ilhamradhan/steam-games-analytics/actions/workflows/dbt_run.yml/badge.svg)](https://github.com/ilhamradhan/steam-games-analytics/actions/workflows/dbt_run.yml)

## Overview

This project transforms raw Steam games data (from HuggingFace) through 3 layers into analytics-ready tables:

```
Raw Parquet → Staging → Intermediate → Marts
```

- **Staging**: Type casting, deduplication, cleaning, score normalization
- **Intermediate**: Array flattening, engagement metrics, publisher/developer aggregates
- **Marts**: Performance dashboards, genre analytics, publisher rankings, engagement segments

## Quick Start

```bash
pip install -r requirements.txt
python load_steam_data.py
cp profiles.yml.example profiles.yml
dbt run
dbt test
```

## Data Source

[FronkonGames/steam-games-dataset](https://huggingface.co/datasets/FronkonGames/steam-games-dataset) — 124,146 Steam games with metadata, reviews, pricing, and more.

## Project Structure

```
steam-games-analytics/
├── models/
│   ├── staging/           # 3 models — base, cleaned, scored
│   ├── intermediate/      # 5 models — flattened, engagement, aggregates
│   ├── marts/             # 4 models — performance, genres, publishers, segments
│   ├── _models.yml        # Documentation for all models
│   └── _sources.yml       # Raw source definition
├── tests/
│   ├── test_review_counts.sql
│   ├── test_price_range.sql
│   ├── test_dates_logical.sql
│   └── generic/           # Custom generic tests
├── macros/
│   └── generate_schema_name.sql
├── .github/workflows/
│   └── dbt_run.yml
├── load_steam_data.py
├── dbt_project.yml
├── profiles.yml.example
└── requirements.txt
```

## Model Lineage

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

## Key Metrics

| Metric | Description |
|--------|------------|
| `sentiment_ratio` | Positive reviews / total reviews |
| `engagement_tier` | viral \| popular \| moderate \| low \| none |
| `metacritic_tier` | excellent (85+) \| good (70+) \| ok (50+) \| poor \| unrated |
| `success_indicator` | blockbuster \| strong \| mixed \| weak \| unrated |
| `revenue_estimate` | Midpoint of owner range × price |
| `market_share_pct` | Publisher's share of total estimated market revenue |

## Testing

**21 data tests** across all layers:
- `not_null` on key fields (appid, game_name, genre, publisher)
- `unique` on appid in staging and marts
- `accepted_values` on score tiers, engagement tiers, success indicators
- **Singular tests**: review counts non-negative, valid price range, logical dates

```bash
dbt test   # 21/21 pass
```

## Tech Stack

- **dbt** 1.11 — Data transformations
- **DuckDB** 1.5 — Embedded analytical database
- **Python** 3.12 — Data loading
- **GitHub Actions** — CI/CD pipeline

## License

MIT
