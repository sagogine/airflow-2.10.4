from google.cloud import datastore
import os
import json

os.environ["DATASTORE_EMULATOR_HOST"] = "localhost:8081"
os.environ["GOOGLE_CLOUD_PROJECT"] = "cerebro"  

client = datastore.Client()

kind = 'xcelerator'  

query = client.query(kind=kind)
entities = list(query.fetch())

for entity in entities:
    client.delete(entity.key)
    print(f"Deleted entity with key: {entity.key}")

json_objects = [
    {
        "domain": "media",
        "sub_domain": "social_media",
        "source": "twitter",
        "table": "sales",
        "is_encrypted": True,
        "is_tokenized": False,
        "ingestion": {
            "operator_type": "bash",
            "file_type": "csv",
            "is_header": True,
            "delimiter": ",",
            "has_dfm": True,
            "schedule": "daily"
        },
        "curation": [
            {
                "operator_type": "bash",
                "query": "select * from sales",
                "schedule": "daily"
            },
            {
                "operator_type": "bash",
                "query": "select * from sales",
                "schedule": "daily"
            },
            {
                "operator_type": "bash",
                "query": "select * from sales",
                "schedule": "daily"
            }

        ],
        "publication": [
            {
                "operator_type": "dummy",
                "query": "select * from sales",
                "schedule": "daily"
            },
            {
                "operator_type": "dummy",
                "query": "select * from sales",
                "schedule": "daily"
            }
        ]
    },
    {
        "domain": "marketing",
        "sub_domain": "social_media",
        "source": "facebook",
        "table": "sales",
        "is_encrypted": False,
        "is_tokenized": True,
        "ingestion": {
            "operator_type": "bash",
            "file_type": "csv",
            "is_header": True,
            "delimiter": ",",
            "has_dfm": True,
            "schedule": "daily"
        },
        "publication": [
            {
                "operator_type": "dummy",
                "query": "select * from sales",
                "schedule": "daily"
            }
        ]
    },
    # Add other objects here if necessary
]

for obj in json_objects:
    entity_key = client.key(kind)   
    entity = datastore.Entity(key=entity_key)
    
    entity.update(obj)  # Update the entity with data from json object

    print(f"Inserting entity with key: {entity_key} and data: {obj}")
    
    client.put(entity)

query = client.query(kind=kind)
entities = list(query.fetch())

print(f"Found {len(entities)} entities.")

for entity in entities:
    print(f"Entity retrieved: {entity}")
