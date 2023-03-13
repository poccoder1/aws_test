from pyspark.sql.functions import explode
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# define the schema for the XML data
schema = StructType([
    StructField("reportID", StringType()),
    StructField("BD", StringType()),
    StructField("ccc", StringType()),
    StructField("type", StringType()),
    StructField("PPP", StringType()),
    StructField("inr", StringType()),
    StructField("PTY", StructType([
        StructField("ID", StringType()),
        StructField("R", IntegerType())
    ])),
    StructField("Instragram", StructType([
        StructField("ID", StringType()),
        StructField("secType", StringType()),
        StructField("mmy", StringType()),
        StructField("change", StringType()),
        StructField("low", IntegerType()),
        StructField("high", IntegerType()),
        StructField("mid", IntegerType())
    ])),
    StructField("undy", StructType([
        StructField("ID", StringType()),
        StructField("sectype", StringType()),
        StructField("check", StringType()),
        StructField("by", StringType())
    ])),
    StructField("QNTY", StructType([
        StructField("short", IntegerType()),
        StructField("Typ", StringType())
    ]))
])

# read the XML data into a DataFrame
df = spark.read.format("xml") \
    .option("rowTag", "level1") \
    .schema(schema) \
    .load("s3://path/to/xml/file.xml")

# explode the PTY and QNTY columns to create a new row for each entry
df = df.selectExpr("reportID", "BD", "ccc", "type", "PPP", "inr", "Instragram.ID as instaID",
                   "Instragram.secType", "Instragram.mmy", "Instragram.change", "Instragram.low",
                   "Instragram.high", "Instragram.mid", "undy.ID as undyID", "undy.sectype",
                   "undy.check", "undy.by", "PTY.*", "QNTY.*") \
    .withColumn("PTY", explode("PTY")) \
    .withColumn("QNTY", explode("QNTY"))

# write the DataFrame to CSV or table format
df.write.format("csv").option("header", "true").save("s3://path/to/output/csv")
df.write.format("parquet").saveAsTable("database.table")
