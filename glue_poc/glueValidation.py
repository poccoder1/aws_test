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
data_frame = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": [input_path]},
    format="csv",
    format_options={"withHeader": True}
)

# Define the JSON schema
json_schema = {
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
                    },
                    "required": ["First_Name", "Last_Name"]
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
                    },
                    "required": ["Address_Line1", "city", "state", "pin_code"]
                }
            },
            "required": ["Name", "Address"]
        }
    }
}

# Generate CSV schema based on JSON schema
def process_schema(schema, parent_key=''):
    csv_schema = []
    for key, value in schema.items():
        current_key = f"{parent_key}.{key}" if parent_key else key
        if value.get('type') == 'object':
            nested_schema = value.get('properties', {})
            nested_csv_schema = process_schema(nested_schema, parent_key=current_key)
            csv_schema.extend(nested_csv_schema)
        else:
            csv_schema.append((current_key, value.get('type')))
    return csv_schema

csv_schema = process_schema(json_schema['data']['items']['properties'])

# Convert CSV to JSON using the provided schema
json_data_frame = ApplyMapping.apply(
    frame=data_frame,
    mappings=[
        (column_name, column_type, column_name.replace(".", "_"))
        for column_name, column_type in csv_schema
    ]
)

# Write JSON data frame to S3
output_path = args['s3_output_path']
glueContext.write_dynamic_frame.from_options(
    frame=json_data_frame,
    connection_type="s3",
    connection_options={"path": output_path},
    format="json",
    format_options={"jsonSchema": json.dumps(json_schema)}
)

# Commit the job and exit
job.commit()
