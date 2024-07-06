from airflow import DAG
from airflow.decorators import task
from datasets import MY_FILE, MY_FILE_2

from datetime import datetime

with DAG(
    dag_id="consumer",
    schedule=[MY_FILE, MY_FILE_2],
    start_date=datetime(2022, 1, 1),
    catchup=False
):

    @task
    def read_dataset():
        with open(MY_FILE.uri, "r") as f:
            print(f.read())


    @task
    def read_dataset_2():
        with open(MY_FILE_2.uri, "r") as f:
            print(f.read())

    read_dataset() >> read_dataset_2()
