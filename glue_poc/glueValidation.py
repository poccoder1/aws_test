import json
from pyspark.sql.functions import substring

# read the JSON configuration
with open('/path/to/config.json', 'r') as f:
    config = json.load(f)

# define the schema based on the configuration
schema = []
start_index = 0
for col_name, col_len in config['Fix_Delimited']['schemaDefinitionLength'].items():
    end_index = start_index + col_len
    schema.append((col_name, substring('value', start_index, col_len).alias(col_name)))
    start_index = end_index

# read the text file data
data = spark.read.text('/path/to/textfile.txt')

# apply the schema to create columns
for col_name, col_expr in schema:
    data = data.withColumn(col_name, col_expr)

# show the resulting dataframe
data.show()
