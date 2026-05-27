import os
import sys

import duckdb

PARQUET_URL = "https://huggingface.co/datasets/FronkonGames/steam-games-dataset/resolve/refs%2Fconvert%2Fparquet/default/train/0000.parquet"
PARQUET_PATH = "data/raw_steam_games.parquet"
DUCKDB_PATH = "steam_games.duckdb"


def download_parquet():
    if os.path.exists(PARQUET_PATH):
        print(f"Parquet file already exists at {PARQUET_PATH}")
        return

    print(f"Downloading from {PARQUET_URL} ...")
    import requests

    response = requests.get(PARQUET_URL, stream=True)
    response.raise_for_status()

    os.makedirs("data", exist_ok=True)
    with open(PARQUET_PATH, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    file_size = os.path.getsize(PARQUET_PATH) / (1024 * 1024)
    print(f"Downloaded {file_size:.1f} MB to {PARQUET_PATH}")


def load_to_duckdb():
    print(f"Loading into DuckDB ({DUCKDB_PATH}) ...")
    conn = duckdb.connect(DUCKDB_PATH)

    row_count = conn.execute(
        f"SELECT count(*) FROM read_parquet('{PARQUET_PATH}')"
    ).fetchone()[0]
    print(f"Parquet contains {row_count:,} rows")

    conn.execute(f"""
        CREATE OR REPLACE TABLE raw_steam_games AS
        SELECT * FROM read_parquet('{PARQUET_PATH}')
    """)

    verify_count = conn.execute("SELECT count(*) FROM raw_steam_games").fetchone()[0]
    print(f"Loaded {verify_count:,} rows into raw_steam_games")

    conn.close()
    print("Done.")


if __name__ == "__main__":
    download_parquet()
    load_to_duckdb()
