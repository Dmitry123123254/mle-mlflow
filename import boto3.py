import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

# Настройки
bucket_name = 's3-student-mle-20250130-d1608e0ec6' # твой bucket_name
aws_key = '***' 
aws_secret = '***'
endpoint_url = 'https://storage.yandexcloud.net'

# Клиент S3
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_key,
    aws_secret_access_key=aws_secret,
    endpoint_url=endpoint_url,
    config=Config(signature_version='s3v4', s3={'payload_signing_enabled': False})
)

location = s3.get_bucket_location(Bucket=bucket_name)
print(location.get('LocationConstraint', 'us-east-1'))

# Проверка подключения
try:
    s3.head_bucket(Bucket=bucket_name)
    print("S3 доступен")
    location = s3.get_bucket_location(Bucket=bucket_name)
    print(location['LocationConstraint'])

except ClientError:
    print("Ошибка подключения к S3")