import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import streamlit as st

class NlpApi:
    def __init__(self, df, api):
        self.df = df
        self.api = api
        self.do_nlp()


    def getAnalysis(self, score):
        if score < 0:
            return 'Negative'
        elif score == 0:
            return 'Neutral'
        else:
            return 'Positive' 

    def getSubjectivity(self, col_df):
        return TextBlob(col_df).sentiment.subjectivity

    def getPolarity(self, col_df):
        return TextBlob(col_df).sentiment.polarity

    def do_nlp(self):
        if self.api=='twitter':
            self.df['Subjectivity'] = self.df['Clean_Tweets'].apply(self.getSubjectivity)
            self.df['Polarity'] = self.df['Clean_Tweets'].apply(self.getPolarity)
            self.compute_sentiment()
            fig_plotbar = self.return_getplotbar()
            fig_plotscatter = self.return_getplotscatter()
            fig_plotcammenbert = self.return_getplotcamembert()
            return fig_plotbar, fig_plotscatter, fig_plotcammenbert
        if self.api=='google':
            self.df['Subjectivity'] = self.df['title'].apply(self.getSubjectivity)
            self.df['Polarity'] = self.df['title'].apply(self.getPolarity)
            self.compute_sentiment()
            fig_plotbar = self.return_getplotbar()
            fig_plotscatter = self.return_getplotscatter()
            fig_plotcammenbert = self.return_getplotcamembert()
            return fig_plotbar, fig_plotscatter, fig_plotcammenbert
        
    def compute_sentiment(self):
        # self.df['Analysis'] = self.getAnalysis(self.df['Polarity'])
        self.df['Analysis'] = self.df['Polarity'].apply(self.getAnalysis)
        self.df = self.df.reset_index()
        ptweets = self.df[self.df.Analysis == 'Positive']
        ntweets = self.df[self.df.Analysis == 'Negative']
        netweets = self.df[self.df.Analysis == 'Neutral']
        self.total_positive = round((ptweets.shape[0] / self.df.shape[0])*100, 1)
        self.total_negative = round((ntweets.shape[0] / self.df.shape[0])*100, 1)
        self.total_neutral = round((netweets.shape[0] / self.df.shape[0])*100, 1)
        
    def return_getplotbar(self):
        fig_1 = plt.figure()
        self.df['Analysis'].value_counts().plot(kind='bar')
        plt.title('Sentiment Analysis')
        plt.xlabel('Sentiment')
        plt.ylabel('Counts')
        return st.pyplot(fig_1)


    def return_getplotscatter(self):
        fig_2 = plt.figure(figsize=(8,6))
        for i in range(0,self.df.shape[0]):
            plt.scatter(self.df['Polarity'][i], self.df['Subjectivity'][i], color='Blue')
        plt.title('Sentiment Analysis')
        plt.xlabel('Polarity')
        plt.ylabel('Subjectivity')
        plt.show()
        return st.pyplot(fig_2)

    def return_getplotcamembert(self):
        fig_3 = plt.figure()
        explode=(0,0.2,0)
        labels='Positive', 'Negative', 'Neutral'
        colors=['#7ECA9C','#EC255A','#51C4D3']
        size=[self.total_positive,self.total_negative,self.total_neutral]
        plt.pie(size, explode=explode,colors=colors,startangle=180,autopct='%1.1f%%')
        plt.legend(labels,loc=(-0.05,0.05),shadow=True)
        return st.pyplot(fig_3)








