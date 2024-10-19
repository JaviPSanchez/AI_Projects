import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
import streamlit as st
import matplotlib.pyplot as plt

class Rnn:
    def __init__(self, df, api):
        self.df = df.reset_index()
        self.api = api
        self.load_pretrained = self.load_pretrained()
        self.get_sentiment = self.get_sentiment()
        self.final = self.export_dict()
        self.return_getplotbar()
        
        
    def load_pretrained(self):
        tokenizer = AutoTokenizer.from_pretrained("siebert/sentiment-roberta-large-english")
        model = AutoModelForSequenceClassification.from_pretrained("siebert/sentiment-roberta-large-english")
        
    def get_sentiment(self):
        if self.api == 'twitter':
            tweets = []
            for i in range(0, 50):
                st.write(self.df.Clean_Tweets[i])
                sentiment_analysis = pipeline("sentiment-analysis",model="siebert/sentiment-roberta-large-english")
                tweets.append(sentiment_analysis(self.df.Clean_Tweets[i]))
                st.write(sentiment_analysis(self.df.Clean_Tweets[i]))
            return tweets
            
            
        if self.api == 'google':
            articles = []
            for i in range(0, 2):
                st.write(self.df.title[i])
                sentiment_analysis = pipeline("sentiment-analysis",model="siebert/sentiment-roberta-large-english")
                articles.append(sentiment_analysis(self.df.title[i]))
                st.write(sentiment_analysis(self.df.title[i]))
            return articles

    def export_dict(self):
        df_final = pd.DataFrame()
        for i in range(0,len(self.get_sentiment)):
            print(self.get_sentiment[i][0])
            df_final = df_final.append(self.get_sentiment[i][0], ignore_index=True)
        return df_final

    def return_getplotbar(self):
        fig_1 = plt.figure()
        self.final['label'].value_counts().plot(kind='bar')
        plt.title('Sentiment Analysis')
        plt.xlabel('Sentiment')
        plt.ylabel('Counts')
        score = self.final['score'].mean()
        st.write(f'Score : {score}')
        return st.pyplot(fig_1)
            
            
