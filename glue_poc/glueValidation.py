import json
from pyspark.sql.functions import substring, length, when

# Read the JSON schema definition from the config file
with open('config.json') as f:
    config = json.load(f)

schema = config['Fix_Delimited']['schemaDefinitionLength']
skip_first_row = config['Fix_Delimited']['skipFirstRow']

# Define the start and end indices for each column
indices = [0]
for col_len in schema.values():
    indices.append(indices[-1] + col_len)

# Read the text file into a DataFrame, skipping the first row if specified in the schema
if skip_first_row:
    text_data = spark.read.text('path/to/text/file', wholetext=True).rdd.zipWithIndex().filter(lambda x: x[1] > 0).map(lambda x: x[0]).toDF()
else:
    text_data = spark.read.text('path/to/text/file')

# Create columns based on the schema definition
for i, (col_name, col_len) in enumerate(schema.items(), start=1):
    start_idx, end_idx = indices[i-1], indices[i]
    text_data = text_data.withColumn(col_name, when(length('value') >= end_idx, substring('value', start_idx+1, col_len)).otherwise(None))

# Drop the 'value' column
text_data = text_data.drop('value')

# Write the DataFrame to a CSV file
text_data.write.format('csv').option('header', True).save('path/to/output/file.csv')
