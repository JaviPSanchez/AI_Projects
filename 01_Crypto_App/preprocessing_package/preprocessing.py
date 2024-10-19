import pandas as pd
import re
import json
import streamlit as st

class Preprocessing:
    def __init__(self, df, api=None):
        self.df = df
        # self.api = api
        # self.formatted_df = self.read_df()
        # self.data = self.create_df()
        self.df_final = self.drop_columns()
        # st.write(self.df_final)
        self.df_final = self.df_final.reset_index(drop=True)
        st.write(self.df_final)

        self.df_export = self.tweets_filter(self.df_final)
        st.write(self.df_export)
        # self.final = self.export_df()
        # return self.final

    # def run_preprocessing(self):
    #     self.read_df = self.read_df()
    #     self.create_df = self.create_df()
    #     self.drop_columns = self.drop_columns()
    #     self.filter_tweets = self.tweets_filter(self.df_final)
    #     self.df_final = self.df_final()
    #     return self.df_final

    # def read_df(self):
    #     tweets = []
    #     with open(self.df, 'r') as f:
    #         for row in f.readlines():
    #             tweet = json.loads(row)
    #             tweets.append(tweet)
    #     return tweets
    
    # def create_df(self):
    #     data = pd.DataFrame(self.formatted_df)
    #     return data
    
    def drop_columns(self):
        df_ready = self.df[['lang','text']]
        df_ready_en = df_ready[df_ready['lang'] == 'en']
        return df_ready_en
    
    def tweets_filter(tamiz):
        tamiz = re.sub('#bitcoin', 'bitcoin', tamiz)
        tamiz = re.sub('#Bitcoin', 'Bitcoin', tamiz)
        tamiz = re.sub('#[A-Za-z0-9]+', '', tamiz)
        tamiz = re.sub(r'@[A-Za-z0-9]+', '', tamiz)
        tamiz = re.sub('\\n', '', tamiz)
        tamiz = re.sub('https?:\/\/\S+', '', tamiz)
        tamiz = re.sub(r'RT[\s]+', '', tamiz)
        tamiz = re.sub(r':[\s]+', '', tamiz)
        tamiz = re.sub('[^A-Za-z0-9]+', ' ', tamiz)
        tamiz = tamiz.lower()
        st.write(tamiz)
        # return self.df_final

    def export_df(self):
        # self.df_filtered['Clean_Tweets'] = self.df_filtered['text'].apply(self.df_filtered)
        self.df_filtered['Clean_Tweets'] = self.df_filtered['text'].apply(self.df_filtered)
        return self.df_filtered



    

    

    



    

