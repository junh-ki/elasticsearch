# Step 1: import modules
try:
    import elasticsearch
    from elasticsearch import Elasticsearch
    print("Loaded ...")
except Exception as e:
    print("Some Modules are Missing {} ".format(e))

# Step 2: create an elasticsearch object
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# Step 3: sample data
sample1 = {
    "myloc": {
        "lat": 48.75,
        "lon": -122.48
    },
    "skills": ["Python", "C++", "Java"],
    "names": [
        {
            "first_name": "ray",
            "last_name": "pelletti",
            "suffix": "None",
            "middle_name": "None",
            "middle_initial": "None",
            "name": "ray pelletti",
            "clean": "ray pelletti",
            "is_primary": True
        },
        {
            "first_name": "raymond",
            "last_name": "pelletti",
            "suffix": "None",
            "middle_name": "None",
            "middle_initial": "None",
            "name": "raymond pelletti",
            "clean": "raymond pelletti",
            "is_primary": False
        }
    ]
}
sample2 = {
    "myloc": {
        "lat": 66.75,
        "lon": -150.48
    },
    "skills": ["C++", "Java"],
    "names": [
        {
            "first_name": "jun",
            "last_name": "ki",
            "suffix": "None",
            "middle_name": "None",
            "middle_initial": "None",
            "name": "ray pelletti",
            "clean": "ray pelletti",
            "is_primary": True
        },
        {
            "first_name": "raymond",
            "last_name": "pelletti",
            "suffix": "None",
            "middle_name": "None",
            "middle_initial": "None",
            "name": "raymond pelletti",
            "clean": "raymond pelletti",
            "is_primary": False
        }
    ]
}

# Step 4: create a custom mapping
settings = {
    'settings': {
        'number_of_shards': 1,
        'number_of_replicas': 0
    },
    'mappings': {
        'properties': {
            'myloc': {
                'type': 'geo_point'
            }
        }
    }
}

# Step 5: create an index
my = es.indices.create(index='jun', ignore=400, body=settings)
print(my)
print("\n ##### \n")
res1 = es.index(index='jun', body=sample1, id=1)
print(res1)
res2 = es.index(index='jun', body=sample2, id=2)
print(res2)
# then go to http://localhost:5601/app/management/data/index_management/indices
