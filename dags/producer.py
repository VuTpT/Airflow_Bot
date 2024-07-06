from airflow import DAG
from airflow.decorators import task
from datasets import MY_FILE, MY_FILE_2

from datetime import datetime, timedelta

default_args = {
    "owner": "daniel",
    "depends_on_past": False,
    "start_date": datetime(2022, 1, 1),
    "email": "admin@gmail.com",
    "email_on_failure": False,
    "email_on_reply": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    # "queue": 'bash_queue',
    # "pool": "backfill",
    # "priority_weight": 10,
    # "end_date": datetime(2021, 1, 1),
}

with DAG(
    dag_id="producer",
    schedule="@daily",
    start_date=datetime(2022, 1, 1),
    catchup=False
):
    @task(outlets=[MY_FILE])
    def update_dataset():
        with open(MY_FILE.uri, "a+") as f:
            f.write("producer update")


    @task(outlets=[MY_FILE_2])
    def update_dataset_2():
        with open(MY_FILE_2.uri, "a+") as f:
            f.write("producer update")


    update_dataset() >> update_dataset_2()
    