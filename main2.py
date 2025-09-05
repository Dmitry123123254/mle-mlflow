# Загрузка модели используя model_info.model_uri
loaded_model = mlflow.pyfunc.load_model(model_uri=model_info.model_uri)

# Выполнение предсказаний на отложенной выборке
# Предполагается, что у вас есть отложенная выборка X_holdout
model_predictions = loaded_model.predict(X_test)

assert model_predictions.dtype == int

print(model_predictions[:10])