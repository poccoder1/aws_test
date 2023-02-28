import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Set up GlueContext and logger
glueContext = GlueContext(SparkContext.getOrCreate())
logger = glueContext.get_logger()

# Get Glue job arguments
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'input_bucket', 'input_prefix', 'output_bucket', 'output_prefix'])

# Read data from S3 bucket
input_bucket = args['input_bucket']
input_prefix = args['input_prefix']
input_path = f's3://{input_bucket}/{input_prefix}'
input_dyf = glueContext.create_dynamic_frame_from_options('s3', {'paths': [input_path], 'recurse': True})

# Validate data
if input_dyf.count() == 0:
    logger.error(f'No data found in {input_path}. Exiting Glue job.')
    sys.exit(1)

# ETL data
input_df = input_dyf.toDF()
# Add your ETL code here to transform the data as per your requirements

# Create DynamicFrame from transformed data
output_dyf = DynamicFrame.fromDF(input_df, glueContext, 'output_dyf')

# Write processed data to S3 bucket
output_bucket = args['output_bucket']
output_prefix = args['output_prefix']
output_path = f's3://{output_bucket}/{output_prefix}/test.csv'
glueContext.write_dynamic_frame.from_options(
    frame=output_dyf,
    connection_type='s3',
    connection_options={'path': output_path},
    format='csv',
    format_options={'withHeader': True},
    transformation_ctx='output'
)

# Job completed successfully
logger.info(f'Glue job completed successfully. Processed data stored at {output_path}.')


#============================

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Set up GlueContext and logger
glueContext = GlueContext(SparkContext.getOrCreate())
logger = glueContext.get_logger()

# Get Glue job arguments
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'input_bucket', 'input_prefix', 'output_bucket', 'output_prefix'])

try:
    # Read data from S3 bucket
    input_bucket = args['input_bucket']
    input_prefix = args['input_prefix']
    input_path = f's3://{input_bucket}/{input_prefix}'
    input_dyf = glueContext.create_dynamic_frame_from_options('s3', {'paths': [input_path], 'recurse': True})

    # Validate data
    if input_dyf.count() == 0:
        raise ValueError(f'No data found in {input_path}. Exiting Glue job.')

    # ETL data
    input_df = input_dyf.toDF()
    # Add your ETL code here to transform the data as per your requirements

    # Create DynamicFrame from transformed data
    output_dyf = DynamicFrame.fromDF(input_df, glueContext, 'output_dyf')

    # Write processed data to S3 bucket
    output_bucket = args['output_bucket']
    output_prefix = args['output_prefix']
    output_path = f's3://{output_bucket}/{output_prefix}/test.csv'
    glueContext.write_dynamic_frame.from_options(
        frame=output_dyf,
        connection_type='s3',
        connection_options={'path': output_path},
        format='csv',
        format_options={'withHeader': True},
        transformation_ctx='output'
    )

    # Job completed successfully
    logger.info(f'Glue job completed successfully. Processed data stored at {output_path}.')
except Exception as e:
    # Handle exceptions
    error_message = f'Error processing data: {str(e)}'
    logger.error(error_message)
    raise
