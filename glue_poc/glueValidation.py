import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import col
import redis

# Get Glue job arguments
args = getResolvedOptions(sys.argv, ['JOB_NAME', 's3_input_path', 's3_output_path', 'elastic_cache_endpoint'])

# Initialize Spark and Glue contexts
sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session

# Connect to ElastiCache Redis cluster
r = redis.StrictRedis(host=args['elastic_cache_endpoint'], port=6379, db=0)

# Read CSV file from S3 and convert to DataFrame
input_dyf = glue_context.create_dynamic_frame_from_options(
    's3',
    {'paths': [args['s3_input_path']], 'format': 'csv', 'csvFirstRowIsHeader': 'true', 'delimiter': ','}
)
input_df = input_dyf.toDF()

# Fetch data from Redis cache and convert to DataFrame
redis_data = r.get('your-key')
redis_df = spark.read.json(sc.parallelize([redis_data]))

# Merge data from CSV and Redis
merged_df = input_df.join(redis_df, on='join_column')

# Write merged data to S3 as CSV file
merged_dyf = DynamicFrame.fromDF(merged_df, glue_context, 'merged_dyf')
glue_context.write_dynamic_frame.from_options(
    frame=merged_dyf,
    connection_type='s3',
    connection_options={'path': args['s3_output_path']},
    format='csv'
)
