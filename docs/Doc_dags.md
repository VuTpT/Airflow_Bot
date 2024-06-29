# Defination a dags

with DAG(

        dag_id="user_processing",

        start_date=datetime(2023, 1, 1), # The timestamp from which the scheduler will attempt to backfill  
        
        schedule_interval="@daily", # How often a DAG runs
        
        end_date=datetime(2023, 1, 1), # The timestamp from which a DAG ends
        
        catchup=False # Return past non triggered DAG runs

) as dag:

A DAG is triggered AFTER the 
start_date/last_run + the schedule_interval

# Test dags
airflow tasks test <dag_id> <task_id> <start_date>
Ex: airflow tasks test user_processing create_table 2024-06-24