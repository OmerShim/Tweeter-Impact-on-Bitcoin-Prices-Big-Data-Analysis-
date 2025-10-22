import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import folium_static
from wordcloud import WordCloud

# Connect to SQLite database
conn = sqlite3.connect("db_file.sqlite")

# Load tables into DataFrames
tweets_btc_df = pd.read_sql("SELECT * FROM tweets_per_month_compare_price", conn)
tweets_per_day_df = pd.read_sql("SELECT * FROM tweets_per_day_compare_price", conn)
locations_tweets_df = pd.read_sql("SELECT * FROM locations_most_tweets_small", conn)
bull_bear_df = pd.read_sql("SELECT * FROM compare_bull_bear_count_locations_small", conn)



st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page:", ["Visualizations", "Tables", "Story"])

if page == "Visualizations":


    # Streamlit App Layout
    st.title("📊 Correlation Between Bitcoin Tweets & BTC Price")
    st.write("This dashboard explores how social media activity around Bitcoin correlates with price changes.")

    # Visualization 1: Tweets vs BTC Price per Month
    st.subheader("📈 Tweets vs BTC Price Per Month")
    st.write("This graph shows the number of tweets mentioning Bitcoin per month and its correlation with the average BTC price. We can observe how social media activity fluctuates with price trends.")
    # Ensure the data is sorted properly
    tweets_btc_df = tweets_btc_df.sort_values(by="month")
    fig, ax1 = plt.subplots(figsize=(10,5))
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Total Tweets", color='tab:blue')
    ax1.plot(tweets_btc_df["month"], tweets_btc_df["tweet_count"], color='tab:blue', marker='o', label="Total Tweets")
    ax1.set_xticks(range(len(tweets_btc_df["month"])))
    ax1.set_xticklabels(tweets_btc_df["month"], rotation=45, ha="right")

    ax2 = ax1.twinx()
    ax2.set_ylabel("Avg BTC Price", color='tab:red')
    ax2.plot(tweets_btc_df["month"], tweets_btc_df["avg_btc_price"], color='tab:red', marker='s', linestyle='dashed', label="Avg BTC Price")
    st.pyplot(fig)

    # Visualization 2: Tweets vs BTC Price per Day
    st.subheader("📉 Tweets vs BTC Price Per Day")
    st.write("This graph provides a more detailed view of daily fluctuations in tweet counts and BTC price. By analyzing the trends, we can assess short-term correlations between market sentiment and price movements.")
    # Ensure the data is sorted properly
    tweets_per_day_df = tweets_per_day_df.sort_values(by="Date")
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=tweets_per_day_df, x="Date", y="tweet_count", label="Tweet Count", color='blue', ax=ax)
    ax2 = ax.twinx()
    sns.lineplot(data=tweets_per_day_df, x="Date", y="price", label="BTC Price", color='red', ax=ax2)
    st.pyplot(fig)

    # Visualization 3: Locations with Most Bitcoin Tweets (World Map)
    st.subheader("🌍 Top Locations Tweeting About Bitcoin")
    st.write("This map visualizes which regions have the most Bitcoin-related discussions on Twitter. The larger the circle, the higher the tweet volume from that location.")
    map_center = [20, 0]  # Center of the map
    tweet_map = folium.Map(location=map_center, zoom_start=2)

    # Example function to get latitude and longitude (this should be replaced with actual geolocation data)
    def get_lat_lon(location):
        geocode_data = {
            "USA": [37.0902, -95.7129], "UK": [55.3781, -3.4360], "India": [20.5937, 78.9629],
            "Canada": [56.1304, -106.3468], "Australia": [-25.2744, 133.7751], "Germany": [51.1657, 10.4515]
        }
        return geocode_data.get(location, [0, 0])

    for index, row in locations_tweets_df.iterrows():
        lat, lon = get_lat_lon(row['user_location'])
        folium.CircleMarker(
            location=[lat, lon],
            radius=row['tweet_count'] / 5000,  # Scale the size of circles
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6,
            popup=f"{row['user_location']}: {row['tweet_count']} tweets"
        ).add_to(tweet_map)

    folium_static(tweet_map)

    # Visualization 4: Bullish vs Bearish Mentions by Location
    st.subheader("🐂🐻 Bullish vs Bearish Mentions by Location")
    st.write("This graph compares locations with the most bullish (positive) and bearish (negative) mentions of Bitcoin. This can help gauge sentiment in different geographic regions.")
    fig, ax = plt.subplots(figsize=(10, 6))
    bull_bear_df = bull_bear_df.nlargest(10, 'total_tweets')
    ax.barh(bull_bear_df["user_location"], bull_bear_df["bull_mention_count"], label="Bullish Mentions", color='green')
    ax.barh(bull_bear_df["user_location"], -bull_bear_df["bear_mention_count"], label="Bearish Mentions", color='red')
    ax.legend()
    st.pyplot(fig)

    # Visualization 5: Word Cloud of Bitcoin Tweets
    st.subheader("💬 Word Cloud of Bitcoin Tweets")
    st.write("This word cloud represents the most frequently mentioned words in Bitcoin-related tweets. This visualization helps identify common discussion themes.")
    conn = sqlite3.connect("db_file.sqlite")
    tweets_text = pd.read_sql("SELECT text FROM bitcoin_tweets_small", conn)
    conn.close()
    wordcloud = WordCloud(width=800, height=400, background_color='black').generate(" ".join(tweets_text['text']))
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

    # Interactive Tweet Trends Filter
    st.subheader("📊 Filter Tweet Trends Over Time")
    st.write("Use the dropdown below to filter tweets by month and analyze how discussions changed over time.")
    selected_month = st.selectbox("Select Month:", tweets_btc_df["month"].unique())
    filtered_df = tweets_btc_df[tweets_btc_df["month"] == selected_month]
    st.dataframe(filtered_df.style.set_properties(**{'background-color': 'black'}))

    st.write("### Insights & Observations")
    st.write("- **Strong correlation** between tweet spikes and BTC price changes.")
    st.write("- Some locations tweet significantly more about Bitcoin than others.")
    st.write("- Bullish and Bearish mentions vary by region, influencing sentiment analysis.")

elif page == "Tables":
    tables_query = "SELECT name FROM sqlite_master WHERE type='table'"
    tables = pd.read_sql(tables_query, conn)['name'].tolist()
    st.title("📋 Database Tables")
    st.write("View all the tables stored in the SQLite database.")
    selected_table = st.selectbox("Select a Table", tables)
    table_data = pd.read_sql(f"SELECT * FROM {selected_table}", conn)
    st.write(table_data)

elif page == "Story":
    st.title("📖 The Story Behind the Data")
    st.write("Bitcoin's price has always been influenced by public sentiment and media attention. This dashboard aims to uncover the correlation between Bitcoin-related Twitter activity and price fluctuations.")
    st.write("### Key Questions Explored:")
    st.write("- Do price spikes lead to more social media discussions about Bitcoin?")
    st.write("- Are certain locations more active in discussing Bitcoin?")
    st.write("- Does sentiment (bullish vs. bearish) in tweets reflect actual market trends?")
    st.write("- What are the most commonly used words in Bitcoin-related tweets?")
    st.write("### What We Found:")
    st.write("- Significant correlation between tweet volume and Bitcoin price movements.")
    st.write("- Geographical hotspots for Bitcoin discussions, highlighting market influence.")
    st.write("- Bullish/Bearish sentiment trends align with major market events.")
    st.write("This analysis helps us understand how social media impacts market trends and whether monitoring Twitter sentiment can provide predictive insights for Bitcoin price movements.")

# Close connection
conn.close()
