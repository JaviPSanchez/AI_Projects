from newsapi import NewsApiClient
import os
import pandas as pd
import sys
from dotenv import load_dotenv
from loguru import logger
from config.logging_config import configure_logger

# Configure logging
configure_logger()


# Load environment variables from .env file
logger.debug("Attempting to load environment variables!")
load_dotenv("../secrets/.env.local")
logger.debug("Done loading environment variables!")


class ApiGoogleNews:
    def __init__(self, query, date):
        self.query = query
        self.date_article = date
        self.api_key = os.getenv('API-NEWS-KEY')
        self.respond_endpoint = self.results()

    def run_api_google(self):
        self.return_articles = self.results()
        return self.return_articles

    def results(self):
        results_conca = pd.DataFrame(columns=['author', 'title', 'description', 'url', 'urlToImage','publishedAt','content', 'source.id', 'source.name'])
        newsapi = NewsApiClient(api_key=self.api_key)
        results = newsapi.get_everything(q=self.query,sort_by='relevancy', language='en', page=1, from_param=self.date_article)
        logger.info(f"Results found: {results['totalResults']}")
        logger.info(f"First Article found: {results['articles'][0]}")
        
        try:
            for i in range(results['totalResults']):
                print(f"Article {i + 1}: {results['articles'][0]['title']}")

                # Normalize:
                json_normalized = pd.json_normalize(results['articles'])
                logger.info(f"Normalization: {json_normalized}")
                results_conca = pd.concat([results_conca, json_normalized], ignore_index=True)
                
                
                
                results_conca.to_csv('./assets/database/raw_google_results.csv')
                return results_conca
        except Exception as event:
            logger.error(f"Error: {event}")
            

    


    


