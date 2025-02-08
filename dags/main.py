from google.cloud import datastore
from airflow import settings
from airflow.models import DagBag, DAG
from datetime import datetime
from dag_generator import DagGenerator
import os

os.environ["DATASTORE_EMULATOR_HOST"] = "datastore-emulator:8081"
os.environ["GOOGLE_CLOUD_PROJECT"] = "cerebro" 
os.environ["GOOGLE_API_USE_MTLS"] = "never" 

print("--------------------------starting--------------------------")

datastore_client = datastore.Client()

dag_generator = DagGenerator(datastore_client, "cerebro")

generated_dags = dag_generator.generate_dags()

print(f"Generated {len(generated_dags)} DAGs.")
print("Generated DAGs:", generated_dags)

for dag in generated_dags:
    globals()[dag.dag_id] = dag

print("DAGs generated and added to Airflow successfully!")

print("--------------------------ending--------------------------")
