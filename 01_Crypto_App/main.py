# ---------LIBRARIES------------ #

import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from dotenv import load_dotenv
import twitter_package.twitter
import google_package.google
import wc_package.wc
import nlp_package.nlp
import kmeans_package.kmeans
import preprocessing_package.preprocessing
import rnn_package.rnn
from loguru import logger
from config.logging_config import configure_logger

# Configure logging
configure_logger()

# Load environment variables from .env file
load_dotenv("./secrets/.env.local")

# ---------PAGE LAYOUT------------ #
st.set_page_config(page_title='Crypto Dash', layout="centered", initial_sidebar_state="collapsed", page_icon='random')

# ---------PAGE TITLE------------ #
with open("html/header.html", "r", encoding="utf-8") as file:
    header_html = file.read()
st.markdown(header_html, unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,1,1])
with col1:
    st.write("")
with col2:
    st.image('./assets/images/bitcoin.png', caption="Let's do some predictions!", width=400, use_column_width=True)
with col3:
    st.write("")

# ---------SECTION OPTIONS------------ #
col4, col5, col6 = st.columns([1,4,1])
with col5:
    # Load the HTML content for SELECT CRYPTO
    with open("html/crypto_select.html", "r", encoding="utf-8") as file:
        crypto_select_html = file.read()

    # Display the HTML content
    col5.markdown(crypto_select_html, unsafe_allow_html=True)

    tickers = ('BTC-USD', 'ETH-USD', 'BNB-USD', 'USDT-USD', 'SOL-USD', 'ADA-USD', 'USDC-USD', 'XRP-USD', 'DOT-USD', 'LUNA-USD', 'DOGE-USD')
    crypto = col5.multiselect('Select Crypto', tickers)
    start = col5.date_input('Start date', value=pd.to_datetime('2021-01-01'))
    end = col5.date_input('End date', value=pd.to_datetime('today'))
    interval = col5.selectbox('Select Interval', ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'))

def relativeReturn(df):
    relative = df.pct_change()
    cumulativeReturn = (1 + relative).cumprod() - 1
    cumulativeReturn = cumulativeReturn.fillna(0)
    return cumulativeReturn

if len(crypto) > 0:
    data1 = yf.download(crypto, start, end)['Adj Close']
    data2 = relativeReturn(yf.download(crypto, start, end, interval='1d')['Adj Close'])
    st.line_chart(data1)
    st.line_chart(data2)

# ---------SECTION APIs------------ #
col10, col11, col12 = st.columns([1, 3, 1])
with col11:
    twitter_form = st.form("API_TWITTER")
    
    # Load the HTML content for TWITTER API
    with open("html/twitter_api.html", "r", encoding="utf-8") as file:
        twitter_api_html = file.read()

    twitter_form.markdown(twitter_api_html, unsafe_allow_html=True)
    twitter_form.image('./assets/images/twitter.png', caption="Let's do some predictions!", width=None, use_column_width=True)
    
    search_term = twitter_form.text_input("Search tweets!")
    limit_tweets = twitter_form.slider('Select a range of tweeters', 0, 100)
    submit_button_twitter = twitter_form.form_submit_button("Search")

    def load_data():
        if submit_button_twitter:
            tweets_api = twitter_package.twitter.ApiTwitter(search_term, limit_tweets).run_api_twitter()
            return tweets_api

    tweets_api_load = load_data()
    st.write(tweets_api_load)

col13, col14, col15 = st.columns([1, 3, 1])
with col14:
    google_form = st.form("API_GOOGLE")

    # Load the HTML content for GOOGLE API
    with open("html/google_api.html", "r", encoding="utf-8") as file:
        google_api_html = file.read()

    google_form.markdown(google_api_html, unsafe_allow_html=True)
    google_form.image('./assets/images/google.png', caption="Let's do some predictions!", width=None, use_column_width=True)
    google_search = google_form.text_input("Search news!")
    date_article = google_form.date_input('Select date', value=pd.to_datetime('today'))
    
    # Button
    submit_button_google = google_form.form_submit_button("Search")

    if submit_button_google:
        try:
            news_api = google_package.google.ApiGoogleNews(google_search, date_article).run_api_google()
            st.write(news_api)
        except Exception as error:
            logger.error(f"Error: {error}")

    st.write("Preprocessing:")
    google_preprocessing_form = st.form("GOOGLE_PRE")
    submit_button_google_preprocessing = google_preprocessing_form.form_submit_button("Let's clean those articles!")

    uploaded_file_2 = st.file_uploader("Choose a file 2")

    if uploaded_file_2 is not None:
        df_2 = pd.read_csv(uploaded_file_2, index_col=[0])
        st.write(df_2)
        st.write(df_2.shape)
        fig_20 = plt.figure()
        df_2['description'].str.len().plot(kind='hist')
        plt.title('Text length')
        st.pyplot(fig_20)

    api_name = st.selectbox("Select API*", (" ", "twitter", "google"))
    classifier_name = st.selectbox("Select Classifier", (" ", "WORD CLOUD", "NLP*", "KMEANS", "RNN"))

    if classifier_name == 'WORD CLOUD':  
        wc_package.wc.WordCloud(df_2, api_name).run_wc()
    elif classifier_name == "NLP*":
        nlp_package.nlp.NlpApi(df_2, api_name)
    elif classifier_name == "KMEANS":
        kmeans_package.kmeans.Kmeans(df_2, api_name)
    elif classifier_name == "RNN":
        # rnn_package.rnn.Rnn(df_2, api_name)
        st.write('Not supported in this version')
    else:
        st.write('Choose a Method')
