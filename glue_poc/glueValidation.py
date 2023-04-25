from pyspark.sql import SparkSession
from pyspark.sql.functions import substring

import json

# Create SparkSession
spark = SparkSession.builder.appName("Fix_Delimited_Extractor").getOrCreate()

# Read the text file
data = spark.read.text("<path_to_text_file>")

# Read the config.json file
with open("config.json") as f:
    config_data = json.load(f)

# Extract schema definition length from config file
schema_definition_length = config_data["extractor"]["Fix_Delimited"]["schemaDefinitionLength"]

# Define the schema based on schema definition length
schema = ""
start_index = 0
for key, value in schema_definition_length.items():
    end_index = start_index + value
    schema += f"{key} string, "
    start_index = end_index

# Remove trailing comma and space
schema = schema[:-2]

# Create dataframe with extracted columns
cols = []
for col, value in schema_definition_length.items():
    end_index = start_index + value
    if end_index > len(data.value):
        raise ValueError(f"End index for {col} column exceeds the length of the input string")
    cols.append(substring(data.value, start_index + 1, end_index).alias(col))
    start_index = end_index

df = data.select(cols)

# Create a temporary view
df.createOrReplaceTempView("temp_table")

# Select the columns in the desired order
final_df = spark.sql(f"SELECT {schema} FROM temp_table")

# Show the final dataframe
final_df.show()
