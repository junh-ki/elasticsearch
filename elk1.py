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
    print("Loaded ...")
except Exception as e:
    print("Some Modules are Missing {} ".format(e))

def generator(df2):
    for c, line in enumerate(df2):
        yield {
            '_index': 'myelkfirst',
            '_type': '_doc',
            '_id': line.get("show_id", None),
            '_source': { # source is where you define the JSON document
                'title': line.get('title', ''),
                'director': line.get('director', ''),
                'description': line.get('description', ''),
                'duration': line.get('duration', None),
                'cast': line.get('cast', None)
            }
        }
    raise StopIteration

# Read all the files in the current directory
for x in os.listdir():
    print(x)
df = pd.read_csv("netflix_titles.csv")
print(df.head(3)) # show the top 3 contents
print(df.columns) # show all columns used in the index
print(df.shape) # how many rows and columns
print(df["show_id"].nunique())
print("\n ##### \n")

# Read the Dataset
df = pd.read_csv("netflix_titles.csv")

# Create an Elasticsearch instance
ENDPOINT = "http://localhost:9200/" # if you are using an AWS instance you can replace this with it
es = Elasticsearch(timeout=600, hosts=ENDPOINT)
print(es.ping())
print("\n ##### \n")

# Before uploading, do some data cleaning
print(df.isna().sum()) # how many null values are there
df = df.dropna() # drop all the documents with null value(s), this is how you clean data
print(df.isna().sum())
print(df.shape) # how many rows and columns

# You need to convert the data into appropriate format that Elasticsearch can understand
df2 = df.to_dict('records') # dataframe into a dictionary of series ('dict', 'list', 'series', 'split', 'records', 'index')
print(df2[0])
print(len(df2))

# You need to convert the data into ELK format
mycustom = generator(df2)
print(json.dumps(next(mycustom), indent=3)) # pretty
