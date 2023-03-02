================connect mysql terrafrom=====
locals {
  db_cluster_identifier = "<DB_CLUSTER_IDENTIFIER>"
  db_name = "<DB_NAME>"
  db_username = "<DB_USERNAME>"
  db_password = "<DB_PASSWORD>"
  region = "<REGION>"
}

resource "aws_iam_policy" "glue_aurora_mysql_policy" {
  name_prefix = "glue-aurora-mysql-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid = "VisualEditor0"
        Effect = "Allow"
        Action = [
          "rds-db:connect",
          "rds-db:executeSql"
        ]
        Resource = [
          "arn:aws:rds-db:${local.region}:${data.aws_caller_identity.current.account_id}:dbuser:${local.db_cluster_identifier}/${local.db_username}",
          "arn:aws:rds:${local.region}:${data.aws_caller_identity.current.account_id}:db:${local.db_cluster_identifier}"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "glue_aurora_mysql_policy" {
  policy_arn = aws_iam_policy.glue_aurora_mysql_policy.arn
  role = aws_iam_role.glue_job_role.name
}

data "aws_caller_identity" "current" {}

resource "aws_iam_role" "glue_job_role" {
  name = "glue_job_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_glue_job" "example" {
  name = "example"
  role_arn = aws_iam_role.glue_job_role.arn
  command {
    name = "glueetl"
    python_version = "3"
    script_location = "s3://<S3_BUCKET>/glue_scripts/example.py"
  }
  default_arguments = {
    "--job-language" = "python"
    "--job-bookmark-option" = "job-bookmark-enable"
  }
  connections {
    name = aws_glue_connection.aurora_mysql.name
  }
}

resource "aws_glue_connection" "aurora_mysql" {
  provider_type = "JDBC"
  connection_properties = {
    "jdbc_url" = "jdbc:mysql://<DB_CLUSTER_ENDPOINT>/${local.db_name}"
    "username" = local.db_username
    "password" = local.db_password
  }
  physical_connection_requirements {
    subnet_id = "<SUBNET_ID>"
    security_group_id_list = ["<SECURITY_GROUP_ID>"]
  }
}



=======================python code to execute sql query=======


import sys
import logging
import pyspark.sql.functions as F
from awsglue.dynamicframe import DynamicFrame
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from pyspark.sql import SQLContext
import pymysql

## Initialize Glue and Spark contexts
sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session
sql_context = SQLContext(sc)

## Define connection details for Aurora MySQL database
database = "<DB_NAME>"
host = "<DB_HOST>"
port = <DB_PORT>
username = "<DB_USERNAME>"
password = "<DB_PASSWORD>"

## Connect to Aurora MySQL database using PyMySQL
conn = pymysql.connect(host=host, port=port, user=username, passwd=password, db=database)
cursor = conn.cursor()

## Read data from an S3 bucket and create a DynamicFrame from it
s3_bucket = "<S3_BUCKET_NAME>"
s3_key = "<S3_OBJECT_KEY>"
s3_path = "s3://{}/{}".format(s3_bucket, s3_key)
raw_dynamic_frame = glue_context.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": [s3_path]},
    format="csv",
    format_options={"delimiter": ","},
    transformation_ctx="raw_dynamic_frame"
)

## Perform some data validation on the raw DynamicFrame using PySpark DataFrame API
validated_dynamic_frame = raw_dynamic_frame.filter(
    F.col("<COLUMN_NAME>").isNotNull()
)

## Apply some ETL operations on the validated DynamicFrame using PySpark DataFrame API
transformed_dynamic_frame = validated_dynamic_frame.select(
    "<COLUMN_1>",
    "<COLUMN_2>",
    F.to_date("<COLUMN_3>", "yyyy-MM-dd").alias("<COLUMN_3>")
)

## Convert the transformed DynamicFrame back to a DataFrame
transformed_df = transformed_dynamic_frame.toDF()

## Write the transformed DataFrame to a new table in the Aurora MySQL database using PyMySQL
table_name = "<NEW_TABLE_NAME>"
transformed_df.write.format("jdbc").options(
    url="jdbc:mysql://{}:{}/{}".format(host, port, database),
    driver="com.mysql.jdbc.Driver",
    dbtable=table_name,
    user=username,
    password=password
).mode("append").save()

## Close the PyMySQL database connection
conn.close()


==================  json read====
opetion 1:
==========

import json

def process_data(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                process_data(value)
            else:
                print(f'{key}: {value}')
    elif isinstance(data, list):
        for item in data:
            process_data(item)

# Open the JSON file
with open('myfile.json') as f:
    data = json.load(f)

# Process the data recursively
process_data(data)



Option 2:
==========
import json
import logging

def get_data_by_key(data, key, results):
    if isinstance(data, dict):
        if key in data:
            results.append(data[key])
        for value in data.values():
            if isinstance(value, (dict, list)):
                get_data_by_key(value, key, results)
    elif isinstance(data, list):
        for item in data:
            get_data_by_key(item, key, results)

# Set up the logger
logging.basicConfig(filename='example.log', level=logging.ERROR)

try:
    # Open the JSON file
    with open('myfile.json') as f:
        data = json.load(f)

    # Get all child data under a specific key
    results = []
    get_data_by_key(data, 'my_key', results)
    print(results)
except Exception as e:
    # Log the error
    logging.error(str(e))
