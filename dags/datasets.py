import os

from dotenv import load_dotenv
from airflow import Dataset

load_dotenv()

MY_FILE = Dataset(os.getenv('PATH_TEMP_DIR') + 'my_text.txt')
MY_FILE_2 = Dataset(os.getenv('PATH_TEMP_DIR') + 'my_text_2.txt')
MY_CSV = Dataset(os.getenv('PATH_DATASET_DIR') + 'raw_store_transactions.csv')
PATH_CSV = Dataset(os.getenv('PATH_SQL_SCRIPTS'))

