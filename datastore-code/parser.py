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
    print(f"Entity ID: {entity.key.id}, Data: {entity}")
    print("--------------------------")
    print("Domain: ", entity['domain'])
    print("Sub-domain: ", entity['sub-domain'])
    print("Source: ", entity['source'])
    print("Table: ", entity['table'])
    print("Is Encrypted: ", entity['is-encrypted'])
    print("Is Tokenized: ", entity['is-tokenized'])
    print("--------------------------")
    print("Ingestion: ", entity['ingestion'])
    print("file-type",entity['ingestion']['file-type'])
    print("is-header",entity['ingestion']['is-header'])
    print("--------------------------")
    print("publication: ", entity['publication'])
    print("query",entity['publication'][0]['query'])
    print("schedule",entity['publication'][0]['schedule'])
    print("--------------------------")
    print("curation: ", entity['curation'])