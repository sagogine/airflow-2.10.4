from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.operators.dummy import DummyOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator


class OperatorFactory:
    @staticmethod
    def create_task(operator_type, task_name, operator_args, dag):
    
        operator_creation_method = getattr(OperatorFactory, f'_create_{operator_type}_task', None)
        if operator_creation_method:
            return operator_creation_method(task_name, operator_args, dag)
        else:
            print(f"Unsupported operator type '{operator_type}' for task '{task_name}'")
            return None

    @staticmethod
    def _create_bash_task(task_name, operator_args, dag):
        
        bash_command = operator_args.get('bash_command', 'echo "No command defined"')
        return BashOperator(
            task_id=task_name,
            bash_command=bash_command,
            dag=dag
        )

    @staticmethod
    def _create_bigquery_task(task_name, operator_args, dag):
        
        query = operator_args.get('query', '')
        destination_table = operator_args.get('destination_table', '')
        return BigQueryInsertJobOperator(
            task_id=task_name,
            sql=query,
            use_legacy_sql=False,
            destination_dataset_table=destination_table,
            write_disposition='WRITE_APPEND',
            dag=dag
        )

    @staticmethod
    def _create_sql_task(task_name, operator_args, dag):
        
        query = operator_args.get('query', '')
        conn_id = operator_args.get('conn_id', 'default_conn')
        return SQLExecuteQueryOperator(
            task_id=task_name,
            sql=query,
            conn_id=conn_id,
            autocommit=True,
            dag=dag
        )

    @staticmethod
    def _create_dummy_task(task_name, operator_args, dag):
        
        return DummyOperator(
            task_id=task_name,
            dag=dag
        )
