# Pagination

# Step 1: import the library
try:
    import os
    import sys
    import json
    import elasticsearch
    from elasticsearch import Elasticsearch
    import pandas as pd
    print("All modules are loaded!")
except Exception as e:
    print("Some modules are missing {}".format(e))

def connect_elasticsearch():
    es = None
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if es.ping():
        print('Connected.')
    else:
        print('Not connect!')
    return es


es = connect_elasticsearch()

myquery = {
    "_source": [],
    "size": 10,
    "query": {
        "bool": {
            "must": [],
            "filter": [
                {
                    "exists": {
                        "field": "director"
                    }
                }
            ],
            "should": [
                {
                    "match_phrase": {
                        "director": "Richard"
                    }
                }
            ],
            "must_not": []
        }
    }
}

res = es.search(
    index='myelkfirst',
    scroll='2m',
    size=3,
    body=myquery
)
sid = res["_scroll_id"]
# size is how many records do you want in a page

print(json.dumps(res, indent=3))

# by assigning scroll id, you can keep querying the next three documents
page = es.scroll(scroll_id=sid, scroll='10m') # The scroll parameter tells Elasticsearch to keep the search context open for another 10m.
print(page)

scroll_size = res['hits']['total']['value']
print("scroll_size: " + str(scroll_size))

print(len(res["hits"]["hits"]))

# you can also loop over data
counter = 0
# Start scrolling
while (scroll_size > 0):
    print("Scrolling...")
    page = es.scroll(scroll_id=sid, scroll='10m')
    # Get the number of results that we returned in the last scroll
    scroll_size = len(page['hits']['hits'])
    print(scroll_size)
    # Update the scroll ID
    sid = page['_scroll_id']
    print("Scroll Size {}".format(scroll_size))
    # Do something with the obtained page
    counter = counter + 1
print("COUNTER : {}".format(counter))
