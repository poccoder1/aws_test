import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from pyspark.context import SparkContext
from pyspark.sql.functions import *

# Get arguments
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Create Glue context and Spark context
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Set up data sources
database_name = 'my_database'
input_table_name = 'my_input_table'
output_table_name = 'my_output_table'
output_s3_path = 's3://my-bucket/my-output-path/'

# Read data from input table
input_dyf = glueContext.create_dynamic_frame.from_catalog(database=database_name, table_name=input_table_name)

# Apply transformations to data
transformed_dyf = input_dyf \
    .select_fields(['field1', 'field2', 'field3']) \
    .rename_field('field3', 'new_field3') \
    .apply_mapping([('field1', 'string', 'new_field1', 'string'),
                    ('field2', 'int', 'new_field2', 'int')])

# Add hardcoded currency column
transformed_df = transformed_dyf.toDF()
transformed_df = transformed_df \
    .withColumn('currency', lit('USD'))

# Apply additional transformations using Spark SQL
spark.sql("""
    SELECT new_field1,
           SUM(new_field2) AS total,
           CASE WHEN new_field2 > 100 THEN 'High'
                ELSE 'Low'
           END AS field4,
           SUBSTR(new_field1, 1, 3) AS field5,
           currency
    FROM transformed_df
    GROUP BY new_field1
""").createOrReplaceTempView('output_view')

# Convert back to DynamicFrame
output_dyf = DynamicFrame.fromDF(spark.table('output_view'), glueContext, 'output_dyf')

# Write output to output table
glueContext.write_dynamic_frame.from_catalog(output_dyf, database=database_name, table_name=output_table_name)

# Write output to S3 bucket
output_df = output_dyf.toDF()
output_df \
    .coalesce(1) \
    .write \
    .option('header', 'true') \
    .csv(output_s3_path, mode='overwrite')
