import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql import SparkSession
import json

# Create a Glue context
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Set up Glue job parameters
args = getResolvedOptions(sys.argv, ['JOB_NAME', 's3_input_path', 's3_output_path'])

# Read CSV file from S3
input_path = args['s3_input_path']
data_frame = spark.read.csv(input_path, header=True)

# Define the JSON schema
json_schema = {
    "type": "object",
    "properties": {
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "Name": {
                        "type": "object",
                        "properties": {
                            "First_Name": {"type": "string"},
                            "Middle_Name": {"type": "string"},
                            "Last_Name": {"type": "string"}
                        }
                    },
                    "Address": {
                        "type": "object",
                        "properties": {
                            "Address_Line1": {"type": "string"},
                            "Address_Line2": {"type": "string"},
                            "Address_Line3": {"type": "string"},
                            "city": {"type": "string"},
                            "state": {"type": "string"},
                            "pin_code": {"type": "string"}
                        }
                    }
                }
            }
        }
    },
    "required": ["data"]
}

# Convert CSV to JSON using the provided schema
json_data_frame = data_frame.selectExpr(
    json.dumps(json_schema) + " AS json_schema",
    "to_json(named_struct('Name', named_struct('First_Name', First_Name, 'Middle_Name', Middle_Name, 'Last_Name', Last_Name), 'Address', named_struct('Address_Line1', Address_Line1, 'Address_Line2', Address_Line2, 'Address_Line3', Address_Line3, 'city', city, 'state', state, 'pin_code', pin_code))) AS json_data"
)

# Write JSON data frame to S3
output_path = args['s3_output_path']
glueContext.write_dynamic_frame.from_options(
    frame=glueContext.create_dynamic_frame.fromDF(json_data_frame, glueContext, "nested"),
    connection_type="s3",
    connection_options={"path": output_path},
    format="json",
    format_options={"jsonSchema": json_schema}
)

# Commit the job and exit
job.commit()
