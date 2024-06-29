import os

from dotenv import load_dotenv
from airflow import DAG, Dataset
from airflow.decorators import task

from datetime import datetime, date

load_dotenv()

my_file = Dataset(os.getenv('PATH_TEMP_DIR') + 'my_text.txt')
my_file_2 = Dataset(os.getenv('PATH_TEMP_DIR') + 'my_text_2.txt')

with DAG(
    dag_id="producer",
    schedule="@daily",
    start_date=datetime(2022, 1, 1),
    catchup=False
):
    @task(outlets=[my_file])
    def update_dataset():
        with open(my_file.uri, "a+") as f:
            f.write("producer update")


    @task(outlets=[my_file_2])
    def update_dataset_2():
        with open(my_file.uri, "a+") as f:
            f.write("producer update")


    update_dataset() >> update_dataset_2()