import boto3
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.dynamicframe import DynamicFrame
from glue_dynamicframe_util import merge_frame

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Create a GlueContext object
glueContext = GlueContext(SparkContext.getOrCreate())

# Read the multiple S3 input files into a DynamicFrame object
dynamic_frame = glueContext.create_dynamic_frame_from_options(
    connection_type="s3",
    connection_options={
        "paths": ["s3://bucket/path/to/file1", "s3://bucket/path/to/file2"]
    },
    format="csv",
    format_options={"delimiter": ","},
)

# Merge the multiple DynamicFrame objects into a single DynamicFrame
merged_dynamic_frame = merge_frame(dynamic_frame)

# Write the merged DynamicFrame to S3
glueContext.write_dynamic_frame.from_options(
    frame=merged_dynamic_frame,
    connection_type="s3",
    connection_options={
        "path": "s3://bucket/path/to/combined-file",
        "partitionKeys": []
    },
    format="csv",
    format_options={"delimiter": ","},
)
