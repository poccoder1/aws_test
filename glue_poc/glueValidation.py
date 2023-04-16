from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("Excel to CSV").getOrCreate()

df = spark.read.format("com.crealytics.spark.excel") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load("/path/to/excel/file.xlsx")

df.write.format("csv") \
    .option("header", "true") \
    .save("/path/to/csv/file.csv")


<dependency>
<groupId>com.crealytics</groupId>
<artifactId>spark-excel_2.12</artifactId>
<version>0.13.7</version>
</dependency>