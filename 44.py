##### 4. Проверяем себя, что в MLflow:
# - создался `experiment` с нашим именем
# - внутри эксперимента появился запуск `run`
# - внутри `run` записалась наша тестовая `metric`
from import_data import mlflow, EXPERIMENT_NAME, run_id, METRIC_NAME, METRIC_VALUE

experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
run = mlflow.get_run(run_id)

assert "active" == experiment.lifecycle_stage
assert mlflow.get_run(run_id)
assert METRIC_VALUE == run.data.metrics[METRIC_NAME]