# pip3 install elasticsearch pandas tqdm
try:
    import elasticsearch
    from elasticsearch import Elasticsearch
    from elasticsearch import helpers
    import pandas as pd
    import json
    from ast import literal_eval
    from tqdm import tqdm
    import datetime
    import os
    import sys
    import numpy as np
    print('Loaded ...')
except Exception as e:
    print('Some Modules are Missing {} '.format(e))

def generator(contents):
    for content in contents:
        # specifying type and id in bulk requests is deprecated (7.13.2)
        # all documents will just be sent to elasticsearch to be indexed as-is
        yield {
            '_index': 'myelkfirst',
            '_type': '_doc',
            '_id': content.get('show_id', ''),
            '_source': {
                # source is where you define the JSON document
                'title': content.get('title', ''),
                'director': content.get('director', ''),
                'description': content.get('description', ''),
                'duration': content.get('duration', ''),
                'cast': content.get('cast', '')
            }
        }
        # refer to https://elasticsearch-py.readthedocs.io/en/v7.13.2/helpers.html#example
    raise StopIteration

# Read all the files in the current directory
for x in os.listdir():
    print(x)
df = pd.read_csv('netflix_titles.csv')
print(df.head(3)) # show the top 3 contents
print(df.columns) # show all columns used in the index
print(df.shape) # how many rows and columns
print(df['show_id'].nunique())
print('\n ##### \n')

# Read the Dataset
df = pd.read_csv('netflix_titles.csv')

# Create an Elasticsearch instance
ENDPOINT = 'http://localhost:9200/' # if you are using an AWS instance you can replace this with it
es = Elasticsearch(timeout=600, hosts=ENDPOINT)
print(es.ping())
print('\n ##### \n')

# Before uploading, do some data cleaning
print(df.isna().sum()) # how many null values are there
df = df.dropna() # drop all the documents with null value(s), this is how you clean data
print(df.isna().sum())
print(df.shape) # how many rows and columns
print('\n ##### \n')

# You need to convert the data into appropriate format that Elasticsearch can understand
contents = df.to_dict('records') # dataframe into a dictionary of series ('dict', 'list', 'series', 'split', 'records', 'index')
print(contents[0])
print(len(contents))
print('\n ##### \n')

# # You need to convert the data into ELK format
# mycustom = generator(contents)
# for i in range(len(contents)):
#     print(json.dumps(contents[i], indent=3) + '\n')
# print('done')
# #print(json.dumps(next(mycustom), indent=3)) # pretty

# Settings and Mappings
settings = {
    'settings': {
        'number_of_shards': 1,
        'number_of_replicas': 0
    },
    'mappings': {
        'properties': {
            'director': {
                'type': 'text',
            },
            'duration': {
                'type': 'text',
            }
        }
    }
}

# Upload the data into Elasticsearch
try:
    res = helpers.bulk(es, generator(contents))
    print('Working')
except Exception as e:
    print('Not working {} '.format(e))
    pass

# Delete the index
es.indices.delete(index='myelkfirst', ignore=[400, 404])

# Create the index
my = es.indices.create(index='myelkfirst', ignore=[400, 404], body=settings)
print(my)

try:
    res = helpers.bulk(es, generator(contents))
    print('Working')
except Exception as e:
    print('Not working {} '.format(e))
    pass
