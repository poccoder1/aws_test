import json
from pyspark.sql.functions import substring

# Read the JSON schema definition from the config file
with open('config.json') as f:
    config = json.load(f)

schema = config['Fix_Delimited']['schemaDefinitionLength']

# Define the start and end indices for each column
indices = [0]
for col_len in schema.values():
    indices.append(indices[-1] + col_len)

# Read the text file into a DataFrame
text_data = spark.read.text('path/to/text/file')

# Create columns based on the schema definition
for i, (col_name, col_len) in enumerate(schema.items(), start=1):
    start_idx, end_idx = indices[i-1], indices[i]
    text_data = text_data.withColumn(col_name, substring('value', start_idx+1, col_len))

text_data.show()
