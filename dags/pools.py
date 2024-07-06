from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "start_date": datetime(2019, 1, 1)
}

with DAG(
        dag_id="pools",
        default_args=default_args,
        schedule=timedelta(minutes=1)
):
    t1 = BashOperator(
        task_id="task-1",
        bash_command="sleep 5",
        pool_slots="pool_1"
    )

    t2 = BashOperator(
        task_id="task-2",
        bash_command="sleep 5",
        pool_slots="pool_1"
    )

    t3 = BashOperator(
        task_id="task-3",
        bash_command="sleep 5",
        pool_slots="pool_2",
        priority_weight="2"
    )

    t4 = BashOperator(
        task_id="task-1",
        bash_command="sleep 5",
        pool_slots="pool_2"
    )
