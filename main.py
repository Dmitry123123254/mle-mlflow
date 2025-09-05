import os
import mlflow
import numpy as np
from mlflow.models import infer_signature
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()
# Загружаем необходимые библиотеки для работы с данными и моделированием
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib

# Загружаем данные из файла initial_data.csv
data_path = "../mle-dvc/data/initial_data.csv"
df = pd.read_csv(data_path)

# Предполагаем, что последний столбец содержит целевую переменную (target)
X = df.iloc[:, :-1]  # Все столбцы, кроме последнего - признаки
y = df.iloc[:, -1]   # Последний столбец - целевая переменная

# Разделяем данные на обучающую и тестовую выборки (80% на 20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Загружаем обученную модель из файла
model_path = "../mle-dvc/models/fitted_model.pkl"
model = joblib.load(model_path)

# Выполняем предсказания на тестовых данных
prediction = model.predict(X_test)

# Вычисляем метрики качества модели
accuracy = accuracy_score(y_test, prediction)
precision = precision_score(y_test, prediction, average='weighted')
recall = recall_score(y_test, prediction, average='weighted')
f1 = f1_score(y_test, prediction, average='weighted')

# Создаем словарь с метриками для логирования
metrics = {
    "accuracy": accuracy,
    "precision": precision,
    "recall": recall,
    "f1_score": f1
}

# Создаем сигнатуру модели и пример входных данных
signature = mlflow.models.infer_signature(X_test, prediction)
input_example = X_test[:10]  # Первые 10 строк тестовых данных как пример
metadata = {'model_type': 'monthly'}


EXPERIMENT_NAME = "churn_prediction_experiment_budikdb"
RUN_NAME = "model_0_registry"
REGISTRY_MODEL_NAME = "churn_model_budikdb"

# поднимаем MLflow локально
TRACKING_SERVER_HOST = "127.0.0.1"
TRACKING_SERVER_PORT = 5001
# устанавливаем host, который будет отслеживать наши эксперименты
mlflow.set_tracking_uri(f"http://{TRACKING_SERVER_HOST}:{TRACKING_SERVER_PORT}")

# Устанавливаем переменные окружения из .env файла
os.environ["MLFLOW_S3_ENDPOINT_URL"] = os.environ.get("MLFLOW_S3_ENDPOINT_URL")
os.environ["AWS_ACCESS_KEY_ID"] = os.environ.get("AWS_ACCESS_KEY_ID")
os.environ["AWS_SECRET_ACCESS_KEY"] = os.environ.get("AWS_SECRET_ACCESS_KEY")

# Создаем эксперимент, если он не существует
try:
    experiment_id = mlflow.create_experiment(EXPERIMENT_NAME)
except:
    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
    if experiment is None:
        experiment_id = mlflow.create_experiment(EXPERIMENT_NAME)
    else:
        experiment_id = experiment.experiment_id

pip_requirements = '../mle-dvc/requirements.txt'

with mlflow.start_run(run_name=RUN_NAME, experiment_id=experiment_id) as run:
    run_id = run.info.run_id
    
    # Логируем метрики
    mlflow.log_metrics(metrics)
    
    # Логируем параметры модели
    if hasattr(model, 'get_params'):
        mlflow.log_params(model.get_params())
    
    # Логируем модель в реестр
    model_info = mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="models",
        await_registration_for=60,
        conda_env=None,
        pip_requirements=pip_requirements,
        signature=signature,
        input_example=input_example,
        metadata=metadata,
        registered_model_name=REGISTRY_MODEL_NAME
    )
# Загрузка модели используя model_info.model_uri
loaded_model = mlflow.pyfunc.load_model(model_uri=model_info.model_uri)

# Выполнение предсказаний на отложенной выборке
# Предполагается, что у вас есть отложенная выборка X_holdout
model_predictions = loaded_model.predict(X_test)

assert model_predictions.dtype == int

print(model_predictions[:10])