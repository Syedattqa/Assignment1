import csv
import praw
import kagglehub
import pandas as pd
import yfinance as yf
from kagglehub import KaggleDatasetAdapter

def get_reddit_data(client, secret, agent):
    reddit = praw.Reddit(client_id =client,
                         client_secret =secret,
                         user_agent = agent)
    subreddits = reddit.subreddits.search_by_name('crypto')
    titles=[]
    texts=[]
    authors=[]
    dates=[]
    upvotes=[]
    subreddit_names=[]
    for subreddit in subreddits:
        for submission in reddit.subreddit(subreddit.display_name).hot(limit=50):
            titles.append(submission.title)
            texts.append(submission.selftext)
            authors.append(submission.author)
            dates.append(submission.created_utc)
            upvotes.append(submission.score)
            subreddit_names.append(subreddit.display_name)
    
    
    reddit_df = pd.DataFrame({
        'Subreddit': subreddit_names,
        'Title': titles,
        'Author': authors,
        'Upvotes': upvotes,
        'Datetime': dates,
        'Text': texts
    })
    return reddit_df

def preprocess_reddit(reddit_df):
    reddit_df.dropna(inplace=True)
    reddit_df = reddit_df[reddit_df['Text'].str.strip() != '']
    reddit_df.reset_index(drop=True)
    return reddit_df

def summarize(df):
    print(df.head())

def save_to_csv(df, filename):
    header = df.columns.tolist() 
    rows = df.values.tolist()
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header) 
        writer.writerows(rows)  

df = get_reddit_data(client ='ic70bWPRnEJzRQnZBAGdCQ',
                    secret ='IgdtzNFf1It0ddCaPVRlqzWqBNv2lQ',
                    agent ='DataEng')
df = preprocess_reddit(df)
summarize(df)
save_to_csv(df, 'reddit.csv')