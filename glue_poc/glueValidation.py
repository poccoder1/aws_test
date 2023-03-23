import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import explode
from pyspark.sql.functions import col
from pyspark.sql.functions import lit
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = glueContext.Job(args['JOB_NAME'])

## Read XML File
xml_source = "s3://path/to/xml/file"
xml_df = spark.read.format("com.databricks.spark.xml").option("rowTag", "FIXML").load(xml_source)

## Create a function to flatten the nested XML tags
def flatten_xml(nested):
    flat_dict = {}
    for key, value in nested.items():
        if isinstance(value, dict):
            flat_dict.update(flatten_xml(value))
        else:
            flat_dict[key] = value
    return flat_dict

flatten_udf = udf(flatten_xml, StringType())

## Apply the flatten function to each row of the DataFrame
flat_df = xml_df.select(explode(col("AsgnRpt")).alias("AsgnRpt")) \
    .withColumn("flat_AsgnRpt", flatten_udf(col("AsgnRpt"))) \
    .select([col("flat_AsgnRpt." + c).alias(c) for c in flat_df.columns])

## Write flattened DataFrame to output file
output_path = "s3://path/to/output/file"
flat_df.write.format("csv").option("header", "true").mode("overwrite").save(output_path)

job.commit()
