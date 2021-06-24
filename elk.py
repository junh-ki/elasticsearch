# pip3 install elasticsearch pandas

try:
    import os
    import sys
    import elasticsearch
    from elasticsearch import Elasticsearch
    import pandas as pd

    print("All Modules Loaded ! ")

except Exception as e:
    print("Some Modules are missing {}".format(e))

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
isConnected = es.ping()
print(str(isConnected))

# Create an index ## Kibana: GET _cat/indices
es.indices.create(index='my-foo', ignore=400)
res = es.indices.get_alias("*")
for Name in res:
    print(Name)
print("\n ##### \n")

# Delete an index ## Kibana: GET _cat/indices
es.indices.delete(index="my-foo", ignore=[400, 404])
res = es.indices.get_alias("*")
for Name in res:
    print(Name)
print("\n ##### \n")

# Upload two sample Json Doc  ## Kibana: GET testperson/_search
e1 = {
    "first_name": "Junhyung",
    "last_name": "Ki",
    "age": 29,
    "about": "Backend Software Developer",
    "interests": ['Youtube', 'Gym'],
}
e2 = {
    "first_name": "Taehyun",
    "last_name": "Ki",
    "age": 32,
    "about": "SPA Retail Operator",
    "interests": ['Soccer', 'Fashion'],
}
es.indices.create(index='testperson', ignore=400)
res1 = es.index(index='testperson', doc_type='testpeople', body=e1, id=1)
res2 = es.index(index='testperson', doc_type='testpeople', body=e2, id=2)
