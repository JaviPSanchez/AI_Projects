import matplotlib.pyplot as plt
import wordcloud
import streamlit as st

class WordCloud:
    def __init__(self, df, api):
        self.df = df
        self.api = api

    def run_wc(self):
        self.run_wc = self.cloud()
        

    def cloud(self):
        if self.api=='twitter':
            allWords = " ".join([tweets for tweets in self.df['Clean_Tweets']])
            wordcloud1 = wordcloud.WordCloud().generate(allWords)
            fig_4 = plt.figure(figsize = (15, 15))
            plt.imshow(wordcloud1, interpolation='bilinear')
            plt.axis("off")
            plt.show()
            st.pyplot(fig_4)
            
        if self.api=='google':
            allWords = " ".join([news for news in self.df['title']])
            wordcloud2 = wordcloud.WordCloud().generate(allWords)
            fig_5 = plt.figure(figsize = (15, 15))
            plt.imshow(wordcloud2, interpolation='bilinear')
            plt.axis("off")
            plt.show()
            st.pyplot(fig_5)
            
