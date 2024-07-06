from airflow import DAG
from datetime import datetime, timedelta
# from airflow.operators import DataTransferOperator
from operators.demo_plugin import DataTransferOperator

with DAG(
        'plugins_dag',
        schedule=timedelta(1),
        start_date=datetime(2020, 1, 24),
        catchup=False
):

    t1 = DataTransferOperator(
        task_id='data_transfer',
        source_file_path='/home/daniel/airflow/tmp/source.txt',
        dest_file_path='/home/daniel/airflow/tmp/destination.txt',
        delete_list=['Airflow', 'is'],

    )
