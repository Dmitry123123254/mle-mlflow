import psycopg
import pandas as pd
import mlflow
import os

# подключение к базе данных
connection = {"sslmode": "require", "target_session_attrs": "read-write"}

postgres_credentials = {
    "host": "",
    "port": "",
    "dbname": "",
    "user": "",
    "password": "",
}

assert all([var_value != "" for var_value in postgres_credentials.values()])

connection.update(postgres_credentials)

# определим название таблицы, в которой хранятся наши данные.
TABLE_NAME = "users_churn"

# загружаем данные из базы
with psycopg.connect(**connection) as conn:
    with conn.cursor() as cur:
        cur.execute(f"SELECT * FROM {TABLE_NAME}")
        data = cur.fetchall()
        columns = [col[0] for col in cur.description]

df = pd.DataFrame(data, columns=columns)

# создаем словарь stats с метриками
feature_columns = [col for col in columns if col not in ["id"]]
counts_columns = [
    "type", "paperless_billing", "internet_service", "online_security", "online_backup", "device_protection",
    "tech_support", "streaming_tv", "streaming_movies", "gender", "senior_citizen", "partner", "dependents",
    "multiple_lines", "target"
]

stats = {}

for col in counts_columns:
    column_stat = df[col].value_counts().to_dict()
    column_stat = {f"{col}_{key}": value for key, value in column_stat.items()}
    stats.update(column_stat)

stats["data_length"] = df.shape[0]
stats["monthly_charges_min"] = df["monthly_charges"].min()
stats["monthly_charges_max"] = df["monthly_charges"].max()
stats["monthly_charges_mean"] = df["monthly_charges"].mean()
stats["monthly_charges_median"] = df["monthly_charges"].median()
stats["total_charges_min"] = df["total_charges"].min()
stats["total_charges_max"] = df["total_charges"].max()
stats["total_charges_mean"] = df["total_charges"].mean()
stats["total_charges_median"] = df["total_charges"].median()
stats["unique_customers_number"] = df["customer_id"].nunique()
stats["end_date_nan"] = df["end_date"].isna().sum()

# записываем 20 колонок в файл columns.txt через запятую
with open("columns.txt", "w", encoding="utf-8") as fio:
    fio.write(",".join(feature_columns))

# сохраняем DataFrame в файл users_churn.csv
df.to_csv("users_churn.csv", index=False)

# задаём название эксперимента и имя запуска для логирования в MLflow
EXPERIMENT_NAME = "churn_bdb"
RUN_NAME = "data_check"

# создаём новый эксперимент в MLflow с указанным названием
# если эксперимент с таким именем уже существует,
# MLflow возвращает идентификатор существующего эксперимента
from mlflow.tracking import MlflowClient

# Создаем клиент MLflow
client = MlflowClient()

# Пытаемся получить существующий эксперимент по имени
experiment = client.get_experiment_by_name(EXPERIMENT_NAME)

if experiment is not None:
    experiment_id = experiment.experiment_id
else:
    # Если эксперимент не существует, создаем новый
    experiment_id = client.create_experiment(EXPERIMENT_NAME)

with mlflow.start_run(run_name=RUN_NAME, experiment_id=experiment_id) as run:
    # получаем уникальный идентификатор запуска эксперимента
    run_id = run.info.run_id
    
    # логируем метрики эксперимента
    # предполагается, что переменная stats содержит словарь с метриками,
    # объявлять переменную stats не надо,
    # где ключи — это названия метрик, а значения — числовые значения метрик
    # если переменная stats не определена, пропускаем логирование метрик
    if 'stats' in locals() or 'stats' in globals():
        mlflow.log_metrics(stats)
    
    # логируем файлы как артефакты эксперимента — 'columns.txt' и 'users_churn.csv'
    mlflow.log_artifact('columns.txt', artifact_path='dataframe')
    mlflow.log_artifact('users_churn.csv', artifact_path='dataframe')

experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
# получаем данные о запуске эксперимента по его уникальному идентификатору
run = mlflow.get_run(run_id)

# проверяем, что статус запуска эксперимента изменён на 'FINISHED'
# это утверждение (assert) можно использовать для автоматической проверки того,
# что эксперимент был завершён успешно
assert run.info.status == 'FINISHED'

# удаляем файлы 'columns.txt' и 'users_churn.csv' из файловой системы,
# чтобы очистить рабочую среду после логирования артефактов
os.remove('columns.txt')
os.remove('users_churn.csv')