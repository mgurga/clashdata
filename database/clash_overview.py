import time
from pyspark.sql import SparkSession
from pyspark import SparkConf

WORKERS = "1000"

spark = SparkSession.builder \
	.appName("ClashRoyaleOverview") \
	.config("spark.executor.instances", WORKERS) \
	.getOrCreate()

load_start_time = time.perf_counter()
df = spark.read.csv("battles_Jan01_21.csv", header=True, inferSchema=True)
load_end_time = time.perf_counter()

print("Schema:")
df.printSchema()

print("First 10000 rows:")
show_start_time = time.perf_counter()
df.show(10000, truncate=False)
show_end_time = time.perf_counter()

spark.stop()

print(f"Time to define DataFrame: {load_end_time - load_start_time:0.4f} seconds")
print(f"Time to execute df.show(10): {show_end_time - show_start_time:0.4f} seconds")
