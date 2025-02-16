import csv
import praw
import kagglehub
import pandas as pd
import yfinance as yf
from kagglehub import KaggleDatasetAdapter


def get_yahoo_data(ticker_symbol = "BITW", period="2y")
    # Define the ticker symbol
    # Create a Ticker object
    ticker = yf.Ticker(ticker_symbol)
    
    # Fetch historical market data
    historical_data = ticker.history(period=period)  # data for the last 5 days
    yahoo_df = pd.DataFrame(historical_data["Close"])
    print("Historical Data:")
    historical_data.head()
    return yahoo_df

def preprocess_yahoo(yahoo_df):
    yahoo_df['Date'] = pd.to_datetime(yahoo_df.index, format='mixed')
    columns_order = ['Date'] + [col for col in yahoo_df.columns if col != 'Date']
    yahoo_df = yahoo_df[columns_order]
    yahoo_df.reset_index(drop=True, inplace=True)
    return yahoo_df

def summarize_yahoo(df):
    print(df.head())
    
def save_to_csv(df, filename):
    header = df.columns.tolist() 
    rows = df.values.tolist()
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header) 
        writer.writerows(rows)  

df = get_yahoo_data()
df = preprocess_yahoo(df)
summarize_yahoo(df)
save_to_csv(df, 'yahoo.csv')