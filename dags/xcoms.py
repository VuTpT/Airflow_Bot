import airflow
import airflow.utils.dates

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from datetime import datetime, timedelta

args = {
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(1),
}

with DAG(
        dag_id="xcoms",
        schedule="@daily",
        default_args=args,
        catchup=False
):
    def push_function(**kwargs):
        message = 'This is the push message.'
        ti = kwargs['ti']
        ti.xcom_push(key="message", value=message)

    def pull_function(**kwargs):
        ti = kwargs['ti']
        pull_message = ti.xcom_pull(key='message', task_ids='new_push_task')
        print("Pull Message: '%s'" % pull_message)

    def new_push_function(**kwargs):
        message = 'This is the NEW push message.'
        ti = kwargs['ti']
        ti.xcom_push(key="message", value=message)

    t1 = PythonOperator(
        task_id='push_task',
        python_callable=push_function,
        provide_context=True
    )

    t2 = PythonOperator(
        task_id='pull_task',
        python_callable=pull_function,
        provide_context=True
    )

    t3 = PythonOperator(
        task_id='new_push_task',
        python_callable=new_push_function,
        provide_context=True
    )

    t1 >> t3 >> t2
















