from pyspark.sql import SparkSession

spark = (
    SparkSession.builder.appName("S3-MinIO-BigData")
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4")
    .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:9000")
    .config("spark.hadoop.fs.s3a.access.key", "minioadmin")
    .config("spark.hadoop.fs.s3a.secret.key", "minioadmin")
    .config(
        "spark.hadoop.fs.s3a.path.style.access", "true"
    )  # Wymagane dla MinIO
    .config(
        "spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem"
    )
    .getOrCreate()
)

# Tworzenie przykładowego zbioru danych
data = [
    ("PL", "2026-10-29", 150.0),
    ("DE", "2026-10-29", 320.5),
    ("PL", "2026-10-30", 90.0),
]
df = spark.createDataFrame(data, ["country", "date", "amount"])

# Zapis do S3/MinIO w formacie Parquet z partycjonowaniem po kraju (tworzy prefiksy country=PL/, country=DE/)
df.write.mode("overwrite").partitionBy("country").parquet(
    "s3a://analytics-lake/transactions/"
)

# Odczyt z wykorzystaniem Partition Pruning i Predicate Pushdown
df_filtered = spark.read.parquet("s3a://analytics-lake/transactions/").filter(
    "country = 'PL' AND amount > 100"
)
df_filtered.show()

