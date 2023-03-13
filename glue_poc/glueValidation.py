import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from pyspark.context import SparkContext
from pyspark.sql.functions import *
from pyspark.sql import SparkSession
import logging

# Set up logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Create GlueContext and SparkContext
glueContext = GlueContext(SparkContext.getOrCreate())
spark = glueContext.spark_session

# Get input and output paths from arguments
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'INPUT_PATH', 'OUTPUT_PATH'])

# Read the input XML file as DynamicFrame
input_dynamic_frame = glueContext.create_dynamic_frame.from_options(
        format='xml',
        connection_options={
            'paths': [args['INPUT_PATH']],
            'recurse': True
        },
        transformation_ctx="input_dynamic_frame"
)

# Convert the DynamicFrame to DataFrame
input_dataframe = input_dynamic_frame.toDF()

# Flatten the nested structure of the DataFrame
flattened_dataframe = input_dataframe.select(
    col("*"),
    *[col(column).alias("_".join(column.split("."))) for column in input_dataframe.schema.names if "." in column]
).drop(*[column for column in input_dataframe.schema.names if "." in column])

# Write the DataFrame to CSV format
try:
    flattened_dataframe.write.mode("overwrite").csv(args['OUTPUT_PATH'])
    logger.info(f"Converted XML file to CSV format and saved at {args['OUTPUT_PATH']}")
except Exception as e:
    logger.error(f"Error converting XML file to CSV format: {e}")

# End the job
glueContext.end_of_job()
