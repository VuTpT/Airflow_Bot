import os

from dotenv import load_dotenv
from airflow import DAG, Dataset
from airflow.decorators import task

from datetime import datetime, date

load_dotenv()

my_file = Dataset(os.getenv('PATH_TEMP_DIR') + 'my_text.txt')
my_file_2 = Dataset(os.getenv('PATH_TEMP_DIR') + 'my_text_2.txt')

with DAG(
    dag_id="consumer",
    schedule=[my_file, my_file_2],
    start_date=datetime(2022, 1, 1),
    catchup=False
):

    @task
    def read_dataset():
        with open(my_file.uri, "r") as f:
            print(f.read())


    @task
    def read_dataset_2():
        with open(my_file_2.uri, "r") as f:
            print(f.read())

    read_dataset() >> read_dataset_2()