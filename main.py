import requests     
from google.cloud import firestore
from hashlib import blake2b
import logging
import os

def main(data, context):
    """Entrypoint"""

    logging.info(f'Context: {context}')

    articles = NewsFromBBC()

    if not articles:
        logging.info('No articles')
    else:
        collection_ref = firestore.Client(project="sims-398915").collection("articles")
        
        results = []
        for ar in articles:
            firestore_doc_name = blake2b(bytes(ar['title'].encode('utf-8'))).hexdigest()
            doc_ref = collection_ref.document(firestore_doc_name) 
            doc_ref.set(ar)
            results.append(ar)

        for i in range(len(results)):
            print(i + 1, results[i])


def NewsFromBBC():
    """Call News API for BBC source"""
    query_params = {
      "source": "bbc-news",
      "sortBy": "top",
      "apiKey": os.environ['NEWS_API_KEY']
    }
    main_url = " https://newsapi.org/v1/articles"

    res = requests.get(main_url, params=query_params)
    open_bbc_page = res.json()

    return open_bbc_page["articles"]
