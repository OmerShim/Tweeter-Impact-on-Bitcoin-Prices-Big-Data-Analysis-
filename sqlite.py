import duckdb

duckdb.sql("INSTALL sqlite; LOAD sqlite;")

# Connect to DuckDB
duckdb_conn = duckdb.connect("db_file.duckdb")

# Enable SQLite extension
duckdb_conn.execute("INSTALL sqlite; LOAD sqlite;")

# Connect DuckDB to SQLite
duckdb_conn.execute("ATTACH 'db_file.sqlite' AS sqlite_db (TYPE sqlite);")

# List of tables to export
tables = ["bitcoin_tweets_small","BTC_PRICE_PER_DAY_SMALL","BTC_PRICE_PER_MONTH","locations_most_tweets_small","TWEETS_PER_DAY",
          "TWEETS_PER_MONTH","bull_mention_by_location_small","bear_mention_by_location_small",
          "tweets_per_month_compare_price","tweets_per_day_compare_price","compare_bull_bear_count_locations_small"]

# Loop through and export each table
for table_name in tables:
    print(f"Exporting {table_name} to SQLite...")

    # Export table from DuckDB to SQLite
    duckdb_conn.execute(f"CREATE TABLE sqlite_db.{table_name} AS SELECT * FROM {table_name};")

# Close the connection
duckdb_conn.close()

print("✅ All tables successfully exported to SQLite using DuckDB extension!")


