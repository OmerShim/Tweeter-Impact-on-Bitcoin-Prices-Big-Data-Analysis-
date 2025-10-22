import duckdb

# Connect to DuckDB database
conn = duckdb.connect('db_file.duckdb')
##################################################################################################


# Ensure table exists
conn.execute("""
    CREATE TABLE IF NOT EXISTS bitcoin_tweets AS 
    SELECT * FROM read_csv_auto('Bitcoin_tweets.csv', sample_size=-1, ignore_errors=true)
""")

##################################################################################################
conn.execute(f"""
    CREATE TABLE IF NOT EXISTS bitcoin_tweets_small AS 
    SELECT *
    FROM bitcoin_tweets
    LIMIT 500
""")
##################################################################################################

#btc price per day
conn.execute(f"""
    CREATE TABLE IF NOT EXISTS BTC_PRICE_PER_DAY AS 
    SELECT date , close AS price 
    FROM read_csv_auto('BTC_value_per_day.csv', sample_size=-1, ignore_errors=true);
""")
##################################################################################################
conn.execute(f"""
    CREATE TABLE IF NOT EXISTS BTC_PRICE_PER_DAY_SMALL AS 
    SELECT *
    FROM BTC_PRICE_PER_DAY
    LIMIT 500
""")
##################################################################################################
#btc price per month

conn.execute(f"""
    CREATE TABLE IF NOT EXISTS BTC_PRICE_PER_MONTH AS 
SELECT 
    strftime('%Y-%m', Date) AS month, 
    AVG(price) AS avg_btc_price
FROM BTC_PRICE_PER_DAY
GROUP BY month
ORDER BY month;

""")



##################################################################################################

#locations with the most tweets
conn.execute("""
    CREATE TABLE IF NOT EXISTS locations_most_tweets AS 
    SELECT 
        user_location, 
        COUNT(*) AS tweet_count
    FROM bitcoin_tweets
    WHERE user_location IS NOT NULL AND TRIM(user_location) != '' -- Remove empty locations
    GROUP BY user_location
    ORDER BY tweet_count DESC;
""")
##################################################################################################
conn.execute("""
    CREATE TABLE IF NOT EXISTS locations_most_tweets_small AS 
    SELECT *
    FROM locations_most_tweets
    LIMIT 500
""")
##################################################################################################

#tweets per day
conn.execute("""
CREATE TABLE IF NOT EXISTS TWEETS_PER_DAY AS
    SELECT 
        STRFTIME('%Y-%m-%d', TRY_CAST(date AS TIMESTAMP)) AS tweet_date, 
        COUNT(*) AS tweet_count
    FROM bitcoin_tweets
    WHERE TRY_CAST(date AS TIMESTAMP) IS NOT NULL  -- Exclude bad dates
    GROUP BY tweet_date
    ORDER BY tweet_date DESC;
""")


##################################################################################################
#TWEETS_PER_MONTH
conn.execute("""
CREATE TABLE IF NOT EXISTS TWEETS_PER_MONTH AS

    SELECT 
        STRFTIME('%Y-%m', TRY_CAST(date AS TIMESTAMP)) AS month, 
        COUNT(*) AS tweet_count
    FROM bitcoin_tweets
    WHERE TRY_CAST(date AS TIMESTAMP) IS NOT NULL  -- Exclude bad dates
    GROUP BY month
    ORDER BY tweet_count DESC;
""")


##################################################################################################

# bull_mention_by_location

conn.execute("""
CREATE TABLE IF NOT EXISTS bull_mention_by_location AS

    SELECT 
        user_location, 
        COUNT(*) AS bull_mention_count
    FROM bitcoin_tweets
    WHERE user_location IS NOT NULL AND LOWER(text) LIKE '%bull%'
    GROUP BY user_location
    ORDER BY bull_mention_count DESC;
""")
##################################################################################################

conn.execute("""
CREATE TABLE IF NOT EXISTS bull_mention_by_location_small AS

    SELECT *
    FROM bull_mention_by_location
    LIMIT 500
""")
##################################################################################################
# bear_mention_by_location
conn.execute("""
CREATE TABLE IF NOT EXISTS bear_mention_by_location AS

    SELECT 
        user_location, 
        COUNT(*) AS bear_mention_count
    FROM bitcoin_tweets
    WHERE user_location IS NOT NULL AND LOWER(text) LIKE '%bear%'
    GROUP BY user_location
    ORDER BY bear_mention_count DESC;
""")
##################################################################################################

conn.execute("""
CREATE TABLE IF NOT EXISTS bear_mention_by_location_small AS

    SELECT *
    FROM bear_mention_by_location
    LIMIT 500
""")
##################################################################################################

#comparing tweets to price per month

conn.execute("""
CREATE TABLE IF NOT EXISTS tweets_per_month_compare_price AS
SELECT t1.month , t2.tweet_count , t1.avg_btc_price
FROM BTC_PRICE_PER_MONTH AS t1 INNER JOIN 
TWEETS_PER_MONTH AS t2
ON t1.month = t2.month
ORDER BY t2.tweet_count DESC
""")
##################################################################################################
#comparing tweets to price per day


conn.execute("""
CREATE TABLE IF NOT EXISTS tweets_per_day_compare_price AS

SELECT t1.date , t2.tweet_count , t1.price
FROM BTC_PRICE_PER_DAY AS t1 INNER JOIN 
TWEETS_PER_DAY AS t2
ON t1.date = t2.tweet_date
ORDER BY t2.tweet_count DESC
""")

##################################################################################################
#understand the affect on tweets count per location from bull/bear mention

conn.execute("""
CREATE TABLE IF NOT EXISTS compare_bull_bear_count_locations AS

SELECT 
    l.user_location, 
    l.tweet_count AS total_tweets, 
    b.bear_mention_count, 
    bu.bull_mention_count
FROM locations_most_tweets AS l
LEFT JOIN bear_mention_by_location AS b ON l.user_location = b.user_location
LEFT JOIN bull_mention_by_location AS bu ON l.user_location = bu.user_location
ORDER BY total_tweets DESC;

""")
##################################################################################################

conn.execute("""
CREATE TABLE IF NOT EXISTS compare_bull_bear_count_locations_small AS

    SELECT *
    FROM compare_bull_bear_count_locations
    LIMIT 500
""")

conn.close()

#######################################################################################################

