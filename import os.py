import os

from dotenv import load_dotenv

load_dotenv()
import psycopg
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mlflow
TABLE_NAME = "runs" # таблица с данными
connection = {
    "sslmode": "require",
    "target_session_attrs": "read-write",
    "connect_timeout": 10
}
postgres_credentials = {
    "host": os.getenv("DB_DESTINATION_HOST"),
    "port": os.getenv("DB_DESTINATION_PORT"),
    "dbname": os.getenv("DB_DESTINATION_NAME"),
    "user": os.getenv("DB_DESTINATION_USER"),
    "password": os.getenv("DB_DESTINATION_PASSWORD"),
}

connection.update(postgres_credentials)

with psycopg.connect(**connection) as conn:

    with conn.cursor() as cur:
        cur.execute(f"SELECT * FROM {TABLE_NAME}")
        data = cur.fetchall()
        columns = [col[0] for col in cur.description]

df = pd.DataFrame(data, columns=columns)

df.head(2)