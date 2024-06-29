from airflow import DAG
from airflow.operators.bash import BashOperator
from groups.group_download import download_task
from groups.group_transform import transform_task

from datetime import datetime

with DAG('group_dag_v3', start_date=datetime(2022, 1, 1),
         schedule_interval='@daily', catchup=False) as dag:
    args = {'start_date': dag.start_date, 'schedule_interval': dag.schedule_interval, 'catchup': dag.catchup}

    downloads = download_task()

    check_files = BashOperator(
        task_id='check_files',
        bash_command='sleep 10'
    )

    transforms = transform_task()

    downloads >> check_files >> transforms
