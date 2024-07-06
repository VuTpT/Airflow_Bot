COPY users1 (firstname, lastname, country, username, password, email) FROM '/home/daniel/airflow/store_files/clean_store_transactions.csv'
DELIMITER ',' CSV HEADER;