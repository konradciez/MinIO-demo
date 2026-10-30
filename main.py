import boto3
from botocore.client import Config

# Inicjalizacja klienta (tutaj skonfigurowana pod lokalne MinIO)
# Dla AWS S3 wystarczy usunąć endpoint_url
s3_client = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin",
    config=Config(signature_version="s3v4"),
    region_name="us-east-1",
)

bucket_name = "analytics-lake"

# 1. Tworzenie bucketu
s3_client.create_bucket(Bucket=bucket_name)

# 2. Zapis obiektu z niestandardowymi metadanymi (PUT Object)
s3_client.put_object(
    Bucket=bucket_name,
    Key="sensors/2026-10-29/temp_01.json",
    Body=b'{"sensor_id": 1, "temp": 22.5, "unit": "C"}',
    ContentType="application/json",
    Metadata={"department": "iot-research", "verified": "true"},
)

# 3. Odczyt obiektu i jego metadanych (GET Object)
response = s3_client.get_object(
    Bucket=bucket_name, Key="sensors/2026-10-29/temp_01.json"
)
data = response["Body"].read().decode("utf-8")
print(f"Dane (Payload): {data}")
print(f"Metadane użytkownika: {response['Metadata']}")

# 4. Generowanie Presigned URL (tymczasowy link ważny przez 15 minut)
url = s3_client.generate_presigned_url(
    "get_object",
    Params={"Bucket": bucket_name, "Key": "sensors/2026-10-29/temp_01.json"},
    ExpiresIn=900,
)
print(f"Tymczasowy link do pobrania: {url}")

