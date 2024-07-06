from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from datetime import datetime, timedelta

from data_cleaner import __data_cleaner
from datasets import PATH_CSV, MY_CSV

yesterday_date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

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
        dag_id="store_dag",
        schedule="@daily",
        default_args=default_args,
        template_searchpath=[PATH_CSV],
        catchup=False
):
    t1 = BashOperator(
        task_id='check_file_exists',
        bash_command='shasum %s' % MY_CSV,
        retries=2,
        retry_delay=timedelta(seconds=15)
    )

    t2 = PythonOperator(
        task_id='clean_raw_csv',
        python_callable=__data_cleaner
    )

    t3 = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres_default',
        sql="create_table.sql"
    )

    t4 = PostgresOperator(
        task_id='insert_table',
        postgres_conn_id='postgres_default',
        sql="insert_into_table.sql"
    )

    t5 = PostgresOperator(
        task_id='select_table',
        postgres_conn_id='postgres_default',
        sql="select_from_table.sql"
    )

    t6 = BashOperator(
        task_id='move_file_1',
        bash_command='cat /home/daniel/airflow/store_files/location_wise_profit.csv && mv '
                     '/home/daniel/airflow/store_files/location_wise_profit.csv '
                     '/home/daniel/airflow/store_files/location_wise_profit_%s.csv' % yesterday_date
    )

    t7 = BashOperator(
        task_id='move_file_2',
        bash_command='cat /home/daniel/airflow/store_files/store_wise_profit.csv && mv '
                     '/home/daniel/airflow/store_files/store_wise_profit.csv '
                     '/home/daniel/airflow/store_files/store_wise_profit_%s.csv' % yesterday_date
    )

    t8 = EmailOperator(
        task_id='send_email',
        to='',
        subject='Daily report generated',
        html_content="""" <h1>Congratulations! Your store reports are ready.</h1>""",
        files=['/home/daniel/airflow/store_files/location_wise_profit_%s.csv' % yesterday_date,
               '/home/daniel/airflow/store_files/store_wise_profit_%s.csv' % yesterday_date
               ]
    )

    t9 = BashOperator(
        task_id='rename_raw',
        bash_command='mv /home/daniel/airflow/store_files/raw_store_transactions.csv '
                     '/home/daniel/airflow/store_files/raw_store_transactions_%s.csv' % yesterday_date
    )

    t1 >> t2 >> t3 >> t4 >> t5 >> [t6, t7] >> t8 >> t9
