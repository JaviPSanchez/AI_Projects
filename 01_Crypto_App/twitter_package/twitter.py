import requests
import os
import json
import pandas as pd
import time
import streamlit as st
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv("../secrets/.env.local")


class ApiTwitter:
    def __init__(self, query, num_tweets):
        self.query = query
        self.num_tweets = num_tweets
        self.tweety_bearer_token = os.getenv("X_BEARER_TOKEN")
        self.out_file = './assets/database/raw_twitter_results.csv'
        self.search_url = "https://api.twitter.com/2/tweets/search/recent"
        self.query_params = {'query': self.query,
                #'start_time': '2021-11-01T12:00:00Z',
                'tweet.fields': 'author_id,public_metrics,lang',
                'user.fields': 'username',
                'expansions': 'author_id',
                'max_results': self.num_tweets,
               }
    
    def run_api_twitter(self):
        self.headers = self.create_headers()
        self.respond_endpoint = self.connect_to_endpoint()
        self.get_tweeters = self.get_tweets()
        self.tweets = self.tweets()
        self.tweets_pandas = pd.json_normalize(self.tweets)
        return self.tweets_pandas

    def create_headers(self):
        headers = {"Authorization": "Bearer {}".format(self.tweety_bearer_token)}
        return headers
       
    def connect_to_endpoint(self, next_token=None):
        if next_token:
            self.params['next_token'] = next_token
        response = requests.request("GET", self.search_url, headers=self.headers, params=self.query_params)
        time.sleep(3.1)
        # st.write(response.status_code)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()

    def get_tweets(self):
        with open(self.out_file, 'w') as output_fh:
            self.next_token = None
            tweets_stored = 0
            while tweets_stored < self.num_tweets:
                self.headers = self.create_headers()
                json_response = self.connect_to_endpoint()
                if json_response['meta']['result_count'] == 0:
                    break
                author_dict = {x['id']: x['username'] for x in json_response['includes']['users']}
                for tweet in json_response['data']:
                    try:
                        tweet['username'] = author_dict[tweet['author_id']]
                    except KeyError:
                        print(f"No data for {tweet['author_id']}")
                    output_fh.write(json.dumps(tweet) + '\n')
                    tweets_stored += 1
                try:
                    self.next_token = json_response['meta']['next_token']
                except KeyError:
                    break
            return None
        output_fh.close()
  
    def tweets(self):
        tweets = []
        with open(self.out_file, 'r') as f:
            for row in f.readlines():
                self.tweet = json.loads(row)
                tweets.append(self.tweet)
        f.close()   
        return tweets

