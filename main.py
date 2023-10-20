# importing requests package
import requests     
from google.cloud import firestore
from hashlib import blake2b

db = firestore.Client(project="sims-398915")
collection_ref = db.collection("articles")

def NewsFromBBC():
     
    # BBC news api
    # following query parameters are used
    # source, sortBy and apiKey
    query_params = {
      "source": "bbc-news",
      "sortBy": "top",
      "apiKey": "ec9d43ad13644f6bb1357e9f5c4443d9"
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
               
 
# Driver Code
if __name__ == '__main__':
     
    # function call
    NewsFromBBC() 