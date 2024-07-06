from airflow import DAG
from airflow.operators.bash import BashOperator

from datetime import datetime, timedelta
#from airflow.models import Variable

default_args = {
    "owner": "airflow",
    "start_date": datetime(2019,1,1)
}

with DAG(
    "variable",
    default_args=default_args,
    schedule=timedelta(1)
):
    t1 = BashOperator(
        task_id="print_path",
        bash_command="echo {{var.value.source_path}}"
    )
