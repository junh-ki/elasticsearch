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
es.ping()
