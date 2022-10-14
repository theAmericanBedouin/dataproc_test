import sys

from pyspark.sql import SparkSession
from pyspark.sql.types import BooleanType

if len(sys.argv) == 1:
    print("Please provide a GCS bucket name.")

bucket = sys.argv[1]
table = "bigquery-public-data:new_york_citibike.citibike_trips"

spark = SparkSession.builder \
          .appName("pyspark-example") \
          .config("spark.jars","gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.26.0.jar") \
          .getOrCreate()

df = spark.read.format("bigquery").load(table)

top_ten = df.filter(col("start_station_id") \
            .isNotNull()) \
            .groupBy("start_station_id") \
            .count() \
            .orderBy("count", ascending=False) \
            .limit(10) \
            .cache()

top_ten.show()

top_ten.write \
  .format("bigquery") \
  .option("writeMethod", "direct") \
  .save("top_ten_output.test")
