# importing requests package
import requests     
from google.cloud import firestore
from hashlib import blake2b
import os

db = firestore.Client(project="sims-398915")
collection_ref = db.collection("articles")


def main():
    NewsFromBBC()


def NewsFromBBC():
    """Call News API for BBC source"""
     
    query_params = {
      "source": "bbc-news",
      "sortBy": "top",
      "apiKey": os.environ['NEWS_API_KEY']
    }
    main_url = " https://newsapi.org/v1/articles"
 
    # fetching data in json format
    res = requests.get(main_url, params=query_params)
    open_bbc_page = res.json()
 
    # getting all articles in a string article
    article = open_bbc_page["articles"]
 
    # empty list which will 
    # contain all trending news
    results = []
     
    for ar in article:
        firestore_doc_name = blake2b(bytes(ar['title'].encode('utf-8'))).hexdigest()
        doc_ref = collection_ref.document(firestore_doc_name) 
        doc_ref.set(ar)
        results.append(ar)

    for i in range(len(results)):
        # printing all trending news
        print(i + 1, results[i])
               
 
if __name__ == '__main__':     
    main()
