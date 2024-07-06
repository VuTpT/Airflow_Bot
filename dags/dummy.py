from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import BranchPythonOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2019,1,1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG (
    "dummy_operator",
    default_args=default_args,
    schedule=timedelta(1)
):
    t1 = BashOperator(task_id="print_date1", bash_command="date")
    t2 = BashOperator(task_id="print_date2", bash_command="date")
    t3 = BashOperator(task_id="print_date3", bash_command="date")
    t4 = BashOperator(task_id="print_date4", bash_command="date")
    t5 = BashOperator(task_id="print_date5", bash_command="date")
    t6 = BashOperator(task_id="print_date6", bash_command="echo Hi")
    t7 = BashOperator(task_id="print_date7", bash_command="echo Hi")
    t8 = BashOperator(task_id="print_date8", bash_command="echo Hi")
    t9 = BashOperator(task_id="print_date9", bash_command="echo Hi")
    t10 = BashOperator(task_id="print_date10", bash_command="echo Hi")

    td = BranchPythonOperator(task_id='dummy')



    [t1, t2, t3, t4, t5] >> td >> [t6, t7, t8, t9, t10]


