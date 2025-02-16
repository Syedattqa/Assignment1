import csv
import praw
import kagglehub
import pandas as pd
import yfinance as yf
from kagglehub import KaggleDatasetAdapter

def get_kaggle_data():
    # Set the path to the file you'd like to load
    file_path = "look_into_bitcoin_daily_data.csv"
    
    # Load the latest version
    kgl_df = kagglehub.load_dataset(
      KaggleDatasetAdapter.PANDAS,
      "aleexharris/bitcoin-network-on-chain-blockchain-data",
      file_path,
      # Provide any additional arguments like 
      # sql_query or pandas_kwargs. See the 
      # documenation for more information:
      # https://github.com/Kaggle/kagglehub/blob/main/README.md#kaggledatasetadapterpandas
    )
    return kgl_df


def preprocess_kaggle(kgl_df):
    kgl_df['datetime'] = pd.to_datetime(kgl_df['datetime'], format='mixed')
    kgl_df = kgl_df[kgl_df['fear_greed_category']!='0']
    kgl_df = pd.get_dummies(kgl_df, columns = ['fear_greed_category'], dtype=int)
    return kgl_df.reset_index(drop='True')

def summarize(kgl_df):
    print(kgl_df['fear_greed_category'].value_counts())

def save_to_csv(df, filename):
    header = df.columns.tolist() 
    rows = df.values.tolist()
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header) 
        writer.writerows(rows)  

df = get_kaggle_data()
df = preprocess_kaggle(df)
summarize(df)
save_to_csv(df, 'kaggle.csv')

