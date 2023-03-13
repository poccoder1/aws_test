from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from pyspark.sql.functions import explode
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.functions import col

# Get the Glue context
glueContext = GlueContext(SparkContext.getOrCreate())

# Get the input arguments
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Define the input path and file format
input_path = "s3://bucket-name/path-to-xml-data"
input_format = "com.databricks.spark.xml"

# Read the XML data into a DynamicFrame
dynamic_frame = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    format=input_format,
    connection_options={"paths": [input_path]},
    transformation_ctx="dynamic_frame"
)

# Convert the DynamicFrame to a DataFrame
data_frame = dynamic_frame.toDF()

# Flatten the DataFrame to handle the nested elements in the XML data
flattened_df = data_frame.select("level1.*", "level1.PTY.*", "level1.PTY.sub.*", "level1.Instragram.*", "level1.undy.*", "level1.QNTY.*")

# Define the schema for the flattened DataFrame
schema = StructType([
    StructField("reportID", StringType(), True),
    StructField("BD", StringType(), True),
    StructField("ccc", StringType(), True),
    StructField("type", StringType(), True),
    StructField("PPP", StringType(), True),
    StructField("inr", StringType(), True),
    StructField("PTY_ID", StringType(), True),
    StructField("PTY_R", StringType(), True),
    StructField("PTY_sub_Id", StringType(), True),
    StructField("PTY_sub_type", StringType(), True),
    StructField("Instragram_ID", StringType(), True),
    StructField("Instragram_secType", StringType(), True),
    StructField("Instragram_mmy", StringType(), True),
    StructField("Instragram_change", StringType(), True),
    StructField("Instragram_low", StringType(), True),
    StructField("Instragram_high", StringType(), True),
    StructField("Instragram_mid", StringType(), True),
    StructField("undy_ID", StringType(), True),
    StructField("undy_sectype", StringType(), True),
    StructField("undy_check", StringType(), True),
    StructField("undy_by", StringType(), True),
    StructField("QNTY_short", StringType(), True),
    StructField("QNTY_Typ", StringType(), True)
])

# Create a new DataFrame with the flattened and transformed data
new_df = flattened_df.select([col(c).alias(schema.fields[i].name) for i, c in enumerate(flattened_df.columns)])

# Convert the DataFrame to CSV format and write it to S3
new_df.write.mode('overwrite').csv('s3://bucket-name/output-path', header=True)
