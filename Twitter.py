# importing libraries and packa
import snscrape.modules.twitter as sntwitter
import pandas as pd
from pymongo import MongoClient
import datetime
import time
import streamlit as st

st.set_page_config(page_title = "Twitter",layout="wide")
st.title("TWITTER SCRAPPER")
search = st.text_input("Scrape Tweets with Keyword/Hashtag", placeholder="Enter the Keyword or Hashtag")

yesterday = datetime.date.today() - datetime.timedelta(days = 1)
today = datetime.date.today()

start_date = st.date_input("From", max_value=yesterday, value=yesterday, help="Tweets posted since this date will be scraped")
end_date = st.date_input("To", max_value=today, min_value=start_date, help="Tweets posted until this date will be scraped")
count = st.number_input("Enter the limit", min_value=1, value=100, help="Maximum Number of Tweets to Return")

if search is not "":
    # Creating list to append tweet data 
    tweets_list1 = []

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f"{search} since:{str(start_date)} until:{str(end_date)}").get_items()): #declare a username 
        if i>count-1: #number of tweets you want to scrape
            break
        tweets_list1.append([tweet.date, tweet.id,tweet.url, tweet.content, tweet.user.username,tweet.replyCount,tweet.lang,tweet.source,tweet.likeCount]) #declare the attributes to be returned
        
    # Creating a dataframe from the tweets list above 
    tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'Tweet Id', 'Url','Text', 'Username','Replycount','Language','Source','Likecount'])
    # Making a Connection with MongoClient

    st.dataframe(tweets_df1)

    if st.button('Upload Data to DB'):
        client = MongoClient("mongodb://localhost:27017/")
        # database
        db = client["Twitter"]
        # collection
        tweets = db["Twitts"]
        data_dict = tweets_df1.to_dict("records")
        tweets.insert_one({search+"_"+str(time.time()):data_dict})
        st.write("Data Uploaded to MongoDB successfully.")

    csv = tweets_df1.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=f'{search}.csv',
        mime='text/csv',
    )

    json = tweets_df1.to_json()
    st.download_button(
        label="Download data as JSON",
        data=json,
        file_name=f'{search}.json',
        mime='text/json',
    )
