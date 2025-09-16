import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

# Настройки
bucket_name = 's3-student-mle-20250130-d1608e0ec6' # твой bucket_name
aws_key = 'YCAJE3Nlz8iDILW5VTYM1ihQB' 
aws_secret = 'CPjvS7uwhvJpUj3bKm8X-IX4QAwBIVsvX61IL44'
endpoint_url = 'https://storage.yandexcloud.net'

# Клиент S3
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_key,
    aws_secret_access_key=aws_secret,
    endpoint_url=endpoint_url,
    config=Config(signature_version='s3v4', s3={'payload_signing_enabled': False})
)

# Проверка подключения
try:
    s3.head_bucket(Bucket=bucket_name)
    print("S3 доступен")
except ClientError:
    print("Ошибка подключения к S3")