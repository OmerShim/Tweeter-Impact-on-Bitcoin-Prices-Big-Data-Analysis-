authors: Asaf Hakmon 205364409 and Omer Shimoni 318201597

# Bitcoin Tweets & Price Correlation - Final Project

## Overview

This project analyzes the relationship between Bitcoin-related discussions on Twitter and the price fluctuations of Bitcoin.
 It processes large datasets, performs SQL-based analysis, and visualizes the results in an interactive dashboard using Streamlit.

## Project Structure


📂 Project Directory
├── project.py   # Loads and processes data into DuckDB
├── sqlite.py    # Transfers processed data from DuckDB to SQLite
├── dashboard.py # Streamlit dashboard for data visualization
├── db_file.duckdb # DuckDB database file (processed data)
├── db_file.sqlite # SQLite database file (for dashboard queries)
├── Bitcoin_tweets.csv  # Large dataset of tweets about Bitcoin
├── BTC_value_per_day.csv  # Bitcoin price history per day
├── requirements.txt # Required Python libraries
├── Project-details.docx # Explanations of the project as a whole, in writing and with pictures



## Installation

### Prerequisites

- Python 3.8+
- Virtual environment (optional but recommended)
- Streamlit installed for running the dashboard

### Setup

1. Clone this repository:
   ```sh
   git clone <repo-url>
   cd project-directory
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Data Processing

### 1️⃣ Load and Process Data (**project.py**)

- Reads Bitcoin tweets (`Bitcoin_tweets.csv`) and price data (`BTC_value_per_day.csv`).
- Stores data in **DuckDB**.
- Performs SQL queries to clean and structure the data.
- Creates summary tables such as:
  - `tweets_per_day`, `tweets_per_month`
  - `btc_price_per_day`, `btc_price_per_month`
  - `bullish_bearish_tweets`

### 2️⃣ Transfer Data to SQLite (**sqlite.py**)

- Moves relevant processed tables from **DuckDB** to **SQLite**.
- Enables efficient queries for Streamlit visualization.

### 3️⃣ Visualization and Dashboard (**dashboard.py**)

- Loads data from SQLite and creates interactive visualizations using **Streamlit**.
- Key graphs:
  - **Tweets vs. Bitcoin Price (Monthly & Daily Trends)**
  - **Geographical Distribution of Bitcoin Tweets**
  - **Sentiment Analysis (Bullish vs. Bearish)**
  - **Word Cloud of Frequent Terms**
- Users can interactively explore trends and filter data.

## Running the Project

1. **Run Data Processing**
   ```sh
   python project.py
   ```
2. **Transfer to SQLite**
   ```sh
   python sqlite.py
   ```
3. **Run the Streamlit Dashboard**
   ```sh
   streamlit run dashboard.py
   ```
4. Open the displayed local link in a web browser to view the interactive dashboard.

## Insights & Observations

- There is a noticeable correlation between Bitcoin-related Twitter activity and price fluctuations.
- Geographic analysis highlights the most active regions in Bitcoin discussions.
- Sentiment analysis shows trends in positive vs. negative discussions related to Bitcoin price changes.



