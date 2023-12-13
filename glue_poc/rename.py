import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql import SparkSession
import boto3

# Create a SparkSession
spark = SparkSession.builder.getOrCreate()

# Create a GlueContext
glueContext = GlueContext(SparkContext.getOrCreate())

# Get the job arguments
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'source_path', 'target_path', 'database_name', 'table_name'])

# Read the source file into a Spark DataFrame
source_df = spark.read.format("csv").option("header", "true").load(args['source_path'])

# Convert the DataFrame to a DynamicFrame
source_dyf = glueContext.create_dynamic_frame.from_catalog(database=args['database_name'], table_name=args['table_name'], frame=source_df)

# Apply any required mappings or transformations
# ...

# Write the DynamicFrame back to S3 using glueContext.getSink()
sink = glueContext.getSink(connection_type="s3", path=args['target_path'], enableUpdateCatalog=True, partitionKeys=[])

sink.setFormat("csv")
sink.setCatalogInfo(catalogDatabase=args['database_name'], catalogTableName=args['table_name'])

sink.writeFrame(source_dyf)

# Rename the output file to the desired name
s3 = boto3.resource('s3')
bucket_name = args['target_path'].split('/')[0]
output_file_name = args['target_path'].split('/')[1]
output_file_path = f"{bucket_name}/{output_file_name}"
new_output_file_path = f"{bucket_name}/test.csv"
s3.Object(bucket_name, new_output_file_path).copy_from(CopySource=output_file_path)
s3.Object(bucket_name, output_file_path).delete()

# Create a Glue table for the data in the target S3 location
glueContext.create_dynamic_frame.from_catalog(database=args['database_name'], table_name=args['table_name'], transformation_ctx="datasource").toDF().createOrReplaceTempView(args['table_name'])

# Commit the job
job.commit()
