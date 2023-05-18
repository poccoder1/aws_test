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
