import os
from dotenv import load_dotenv

import mlflow


# Загружаем переменные окружения из .env файла
load_dotenv()

# Определяем основные credentials, которые нужны для подключения к MLflow
# Важно, что credentials мы передаём для себя как пользователей Tracking Service
# У вас должен быть доступ к бакету, в который вы будете складывать артефакты
os.environ["MLFLOW_S3_ENDPOINT_URL"] = "https://storage.yandexcloud.net"  # endpoint бакета от YandexCloud

# Получаем ключи из .env, если они не установлены — будет ошибка
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

if not aws_access_key_id or not aws_secret_access_key:
    raise EnvironmentError("Отсутствуют AWS_ACCESS_KEY_ID или AWS_SECRET_ACCESS_KEY в .env файле")

os.environ["AWS_ACCESS_KEY_ID"] = aws_access_key_id
os.environ["AWS_SECRET_ACCESS_KEY"] = aws_secret_access_key

# Определяем глобальные переменные
# Поднимаем MLflow локально
TRACKING_SERVER_HOST = "127.0.0.1"
TRACKING_SERVER_PORT = 5001

YOUR_NAME = "Дмитрий"  # введите своё имя для создания уникального эксперимента
assert YOUR_NAME, "введите своё имя в переменной YOUR_NAME для создания уникального эксперимента"

# Название тестового эксперимента и запуска (run) внутри него
EXPERIMENT_NAME = f"test_connection_experiment_{YOUR_NAME}"
RUN_NAME = "test_connection_run"

# Тестовые данные
METRIC_NAME = "test_metric"
METRIC_VALUE = 0

# Устанавливаем host, который будет отслеживать наши эксперименты
mlflow.set_tracking_uri(f"http://{TRACKING_SERVER_HOST}:{TRACKING_SERVER_PORT}")

# Создаём тестовый эксперимент и записываем в него тестовую информацию
# Проверяем, существует ли уже эксперимент с таким именем
try:
    experiment_id = mlflow.create_experiment(EXPERIMENT_NAME)
except mlflow.exceptions.RestException as e:
    if "RESOURCE_ALREADY_EXISTS" in str(e):
        # Если эксперимент уже существует, получаем его ID
        experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
        experiment_id = experiment.experiment_id
    else:
        # Если другая ошибка, пробрасываем дальше
        raise e
with mlflow.start_run(run_name=RUN_NAME, experiment_id=experiment_id) as run:
    run_id = run.info.run_id
    
    mlflow.log_metric(METRIC_NAME, METRIC_VALUE)