from datetime import datetime
from google.cloud import datastore
from airflow.models import DAG
from airflow.operators.bash import BashOperator
from operator_factory import OperatorFactory
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.operators.dummy import DummyOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator


class DagGenerator:
    def __init__(self, datastore_client, project_id):
        self.client = datastore_client
        self.project_id = project_id

    def _parse_entity(self, entity):
        dag_objects = {
            'is_encrypted': entity['is_encrypted'],
            'is_tokenized': entity['is_tokenized'],
            'ingestion': entity.get('ingestion', {}),
            'curation': entity.get('curation', []),
            'publication': entity.get('publication', [])
        }
        return dag_objects
    
    def _generate_dag_id(self, entity):
        domain = entity['domain']
        sub_domain = entity['sub_domain']
        source = entity['source']
        table = entity['table']
        return f"dag_{domain}_{sub_domain}_{source}_{table}"
    
    def generate_dags(self):
        query = self.client.query(kind='xcelerator')
        entities = list(query.fetch())
        dags = []
        
        print(f"Found {len(entities)} entities to generate DAGs for.")
        
        for entity in entities:
            dag_objects = self._parse_entity(entity)
            dag_id = self._generate_dag_id(entity)
            dag = self._create_dag(dag_id, dag_objects)
            dags.append(dag)

        return dags
    
    def _create_dag(self, dag_id, dag_objects):
        dag = DAG(
            dag_id=dag_id,
            default_args={'owner': 'airflow'},
            schedule_interval=None, 
            start_date=datetime(2025, 1, 1),
        )

        tasks = []
        for task_name, task_config in dag_objects.items():
            task = self.create_task(task_name, task_config, dag)
            if task:
                tasks.extend(task)

        for task in tasks:
            print(f'task is : {task} and type is : {type(task)}')
        
        for i in range(len(tasks) - 1):
            tasks[i] >> tasks[i + 1] 

        return dag

    def create_task(self, task_name, task_config, dag):
        tasks = []


        if isinstance(task_config, list):
            for idx, config in enumerate(task_config):
                task = self.create_task(f"{task_name}_{idx}", config, dag) 
                if task:
                    tasks.extend(task)

        elif isinstance(task_config, dict):
            operator_type = task_config.get('operator_type', 'bash')  
            operator_args = {key: value for key, value in task_config.items() if key != 'operator_type'} 
            task = OperatorFactory.create_task(operator_type, task_name, operator_args, dag)
            if task:
                tasks.append(task)
        
        return tasks



