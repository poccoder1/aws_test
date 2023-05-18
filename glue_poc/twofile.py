write glue job script that will read 2 files from s3. file1 has col1, col2, col3 col4, col5, col7 and
file2 has col1, col2, col3 col4, col5. Check file1 col1 and col2 are match with file2 col4 and col5 then select file1 all columns and file2
col1 and col2 along with file1 and generate output file.


import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql import SparkSession

# Initialize the Spark and Glue contexts
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Obtain the AWS Glue job arguments
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Create a dynamic frame for file1
file1 = glueContext.create_dynamic_frame.from_catalog(database="your_database_name", table_name="file1_table_name", transformation_ctx="file1")

# Create a dynamic frame for file2
file2 = glueContext.create_dynamic_frame.from_catalog(database="your_database_name", table_name="file2_table_name", transformation_ctx="file2")

# Convert the dynamic frames to DataFrames
file1_df = file1.toDF()
file2_df = file2.toDF()

# Perform the join operation
joined_df = file1_df.join(file2_df, (file1_df["col1"] == file2_df["col4"]) & (file1_df["col2"] == file2_df["col5"]))

# Select the required columns
output_df = joined_df.select(file1_df["col1"], file1_df["col2"], file1_df["col3"], file1_df["col4"], file1_df["col5"], file1_df["col7"], file2_df["col1"], file2_df["col2"])

# Convert the DataFrame back to a dynamic frame
output_dynamic_frame = DynamicFrame.fromDF(output_df, glueContext, "output_dynamic_frame")

# Write the dynamic frame to S3 as a CSV file
glueContext.write_dynamic_frame.from_options(output_dynamic_frame, connection_type="s3", connection_options={"path": "s3://your_output_bucket/path/to/output/file"}, format="csv")


====================================================================

import sys
import json
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql import SparkSession

# Initialize the Spark and Glue contexts
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Obtain the AWS Glue job arguments
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Read the configuration file
with open('config.json') as f:
    config = json.load(f)

# Process each file in the configuration
for file_config in config['files']:
    file_path = file_config['path']
    table_name = file_config['table_name']
    join_columns = file_config['join_columns']

    # Create a dynamic frame for the current file
    dynamic_frame = glueContext.create_dynamic_frame.from_catalog(database="your_database_name", table_name=table_name, transformation_ctx=table_name)
    data_frame = dynamic_frame.toDF()

    # Register the current file as a temporary table
    data_frame.createOrReplaceTempView(table_name)

# Perform the join operations
join_query = ''
for join_config in config['join_conditions']:
    join_table = join_config['table']
    join_columns1 = join_config['columns1']
    join_columns2 = join_config['columns2']

    # Build the join condition
    join_condition = ' AND '.join(f"{table}.{col1} = {join_table}.{col2}" for col1, col2 in zip(join_columns1, join_columns2))
    join_query += f"JOIN {join_table} ON {join_condition} "

# Perform the join query
joined_df = spark.sql(f"SELECT * FROM {config['files'][0]['table_name']} {join_query}")

# Select the required columns
output_df = joined_df.select(*[col['table'] + '.' + col['column'] for col in config['output_columns']])

# Convert the DataFrame back to a dynamic frame
output_dynamic_frame = DynamicFrame.fromDF(output_df, glueContext, "output_dynamic_frame")

# Write the dynamic frame to S3 as a CSV file
glueContext.write_dynamic_frame.from_options(output_dynamic_frame, connection_type="s3", connection_options={"path": "s3://your_output_bucket/path/to/output/file"}, format="csv")


## json

{
    "files": [
        {
            "path": "s3://your_bucket/file1",
            "table_name": "file1_table",
            "join_columns": ["col1", "col2"]
        },
        {
            "path": "s3://your_bucket/file2",
            "table_name": "file2_table",
            "join_columns": ["col4", "col5"]
        }
    ],
    "join_conditions": [
        {
            "table": "file1_table",
            "columns1": ["col1", "col2"],
            "columns2": ["col4", "col5"]
        }
    ],
    "output_columns": [
        {
            "table": "file1_table",
            "column": "col1"
        },
        {
            "table": "file1_table",
            "column": "col2"
        },
        {
            "table": "

===
==============================================================  without table===

import sys
import json
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql import SparkSession

# Initialize the Spark and Glue contexts
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Obtain the AWS Glue job arguments
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Read the configuration file
with open('config.json') as f:
    config = json.load(f)

# Read each file from the configuration
data_frames = {}
for file_config in config['files']:
    file_path = file_config['path']
df = spark.read.option("header", "true").csv(file_path)
table_name = file_config['table_name']
data_frames[table_name] = df

# Perform the join operations
joined_df = None
for join_config in config['join_conditions']:
    table1 = join_config['table1']
table2 = join_config['table2']
join_columns1 = join_config['columns1']
join_columns2 = join_config['columns2']

# Perform the join operation
join_condition = [df1[col1] == df2[col2] for col1, col2 in zip(join_columns1, join_columns2)]
join_type = join_config.get('type', 'inner')  # Default to inner join if not specified
join_df = data_frames[table1].join(data_frames[table2], join_condition, join_type)

# Update the joined DataFrame
if joined_df is None:
    joined_df = join_df
else:
    joined_df = joined_df.join(join_df, join_condition, join_type)

# Select the required columns
output_columns = [f"{table}.{col}" for table, col in config['output_columns']]
output_df = joined_df.select(*output_columns)

# Write the DataFrame to S3 as a CSV file
output_path = config['output_path']
output_df.write.option("header", "true").csv(output_path)
