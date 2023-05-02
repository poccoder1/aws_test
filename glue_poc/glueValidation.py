import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext

# Create a GlueContext
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Get the job parameters
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Create a DynamicFrame from the input .gz files
input_path = "s3://your-bucket/input-folder/*.gz"

input_paths = [
    "s3://your-bucket/input-folder/file1.gz",
    "s3://your-bucket/input-folder/file2.gz",
    "s3://your-bucket/input-folder/file3.gz"
]
datasource = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    format="csv",
    connection_options={"paths": [input_path]},
    format_options={"compression": "gzip"},
    transformation_ctx="datasource"
)

# Merge the CSV files into a single DynamicFrame
merged_frame = ApplyMapping.apply(
    frame=datasource,
    mappings=[
        # Specify your column mappings if needed
    ],
    transformation_ctx="merged_frame"
)

# Write the merged DynamicFrame to a single CSV file
output_path = "s3://your-bucket/output-folder/merged.csv"
glueContext.write_dynamic_frame.from_options(
    frame=merged_frame,
    connection_type="s3",
    connection_options={"path": output_path},
    format="csv",
    format_options={"compression": "gzip"},
    transformation_ctx="output"
)
