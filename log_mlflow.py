import os
import pandas as pd
import mlflow
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from mlflow.models.signature import ModelSignature
import mlflow.pyfunc
import dotenv
import joblib  # Добавить импорт

EXPERIMENT_NAME = "churn_prediction_experiment_budikdb"
RUN_NAME = "model_0_registry"
REGISTRY_MODEL_NAME = "churn_model_budikdb"


TRACKING_SERVER_HOST = "0.0.0.0"
TRACKING_SERVER_PORT = 5001
# load .env file
dotenv.load_dotenv()
os.environ["MLFLOW_S3_ENDPOINT_URL"] = os.getenv("MLFLOW_S3_ENDPOINT_URL")
os.environ["AWS_ACCESS_KEY_ID"] = os.getenv("AWS_ACCESS_KEY_ID")
os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv("AWS_SECRET_ACCESS_KEY")

# Загружаем данные из файла initial_data.csv
data_path = "../mle-dvc/data/initial_data.csv"
df = pd.read_csv(data_path)

# Предполагаем, что последний столбец содержит целевую переменную (target)
X = df.iloc[:, :-1]  # Все столбцы, кроме последнего - признаки
y = df.iloc[:, -1]   # Последний столбец - целевая переменная

# Разделяем данные на обучающую и тестовую выборки (80% на 20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Загружаем обученную модель (добавить это)
model_path = "../mle-dvc/models/fitted_model.pkl"
model = joblib.load(model_path)

# Получаем предсказания (добавить это)
prediction = model.predict(X_test)

mlflow.set_tracking_uri(f"http://{TRACKING_SERVER_HOST}:{TRACKING_SERVER_PORT}")
mlflow.set_registry_uri(f"http://{TRACKING_SERVER_HOST}:{TRACKING_SERVER_PORT}")

# Завершение скрипта
pip_requirements="requirements.txt"
signature = mlflow.models.infer_signature(X_test, prediction)
input_example = X_test[:10]
metadata = {'model_type': 'monthly'}


experiment_id = mlflow.get_experiment_by_name(EXPERIMENT_NAME).experiment_id

# Также добавьте вычисление метрик как в main.py
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
accuracy = accuracy_score(y_test, prediction)
precision = precision_score(y_test, prediction, average='weighted')
recall = recall_score(y_test, prediction, average='weighted')
f1 = f1_score(y_test, prediction, average='weighted')

metrics = {
    "accuracy": accuracy,
    "precision": precision,
    "recall": recall,
    "f1_score": f1
}

with mlflow.start_run(run_name=RUN_NAME, experiment_id=experiment_id) as run:
    run_id = run.info.run_id
    
    # Логирование метрик
    mlflow.log_metrics(metrics)

    # Создание заглушки для модели (в реальном сценарии здесь будет загрузка модели)
    model = LogisticRegression()
       
    model_info = mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="models",
        pip_requirements=pip_requirements,
        registered_model_name=REGISTRY_MODEL_NAME,
        signature=signature,
        input_example=input_example,
        await_registration_for=60,
        metadata=metadata
    )