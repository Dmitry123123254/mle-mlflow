import os

from dotenv import load_dotenv

load_dotenv()
import psycopg
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mlflow

TABLE_NAME = "users_churn" # таблица с данными в postgres 

TRACKING_SERVER_HOST = "0.0.0.0"
TRACKING_SERVER_PORT = 5001

EXPERIMENT_NAME = "churn_prediction_experiment_budikdb" # напишите название вашего эксперимента
RUN_NAME = "eda"


pd.options.display.max_columns = 100
pd.options.display.max_rows = 64


# Создаем директорию assets в папке mle-mlflow
ASSETS_DIR = "mle-mlflow/assets"
os.makedirs(ASSETS_DIR, exist_ok=True) # создает директорию, если она еще не существует

sns.set_style("white")
sns.set_theme(style="whitegrid")

connection = {
    "sslmode": "require",
    "target_session_attrs": "read-write",
    "host": os.getenv("DB_DESTINATION_HOST"),
    "port": os.getenv("DB_DESTINATION_PORT"),
    "dbname": os.getenv("DB_DESTINATION_NAME"),
    "user": os.getenv("DB_DESTINATION_USER"),
    "password": os.getenv("DB_DESTINATION_PASSWORD"),
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