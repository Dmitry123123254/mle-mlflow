export $(grep -v '^#' .env | xargs)

export MLFLOW_S3_ENDPOINT_URL=https://storage.yandexcloud.net

mlflow server \
  --registry-store-uri postgresql://$DB_DESTINATION_USER:$DB_DESTINATION_PASSWORD@$DB_DESTINATION_HOST:$DB_DESTINATION_PORT/$DB_DESTINATION_NAME \
  --backend-store-uri postgresql://$DB_DESTINATION_USER:$DB_DESTINATION_PASSWORD@$DB_DESTINATION_HOST:$DB_DESTINATION_PORT/$DB_DESTINATION_NAME \
  --default-artifact-root s3://$AWS_BUCKET_NAME \
  --no-serve-artifacts \
  --host 127.0.0.1 \
  --port 5001