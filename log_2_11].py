import mlflow
import os
import dotenv

# Загрузка переменных окружения
dotenv.load_dotenv()
TRACKING_SERVER_HOST = "0.0.0.0"
TRACKING_SERVER_PORT = 5001

client=mlflow.MlflowClient(f"http://{TRACKING_SERVER_HOST}:{TRACKING_SERVER_PORT}")

REGISTRY_MODEL_NAME = "churn_model_budikdb"
# Ищем версии модели по фильтру
models = client.search_model_versions(filter_string=f"name = '{REGISTRY_MODEL_NAME}'")

print(f"Model info:\n {models}")


model_name_1 = models[-1].name
model_version_1 = models[-1].version
model_stage_1 = models[-1].current_stage

model_name_2 = models[-2].name
model_version_2 = models[-2].version
model_stage_2 =  models[-2].current_stage


print(f"Текущий stage модели 1: {model_stage_1}")
print(f"Текущий stage модели 2: {model_stage_2}")

# поменяйте статус каждой модели
client.transition_model_version_stage(model_name_1, model_version_1, 'production')
client.transition_model_version_stage(model_name_2, model_version_2, 'staging')

# переимнуйте модель в реестре
client.rename_registered_model(name=REGISTRY_MODEL_NAME, new_name=f'{REGISTRY_MODEL_NAME}_b2c')