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
for key, value in schema_definition_length.items():
    schema += key + " string, "

# Remove trailing comma and space
schema = schema[:-2]

# Create dataframe with extracted columns
df = data.select(
    *[substring(data.value, sum([schema_definition_length[key] for key in schema_definition_length.keys() if key < col]) + 1, value)
          .alias(col)
      for col, value in schema_definition_length.items()]
)

# Create a temporary view
df.createOrReplaceTempView("temp_table")

# Select the columns in the desired order
final_df = spark.sql("SELECT " + schema + " FROM temp_table")

# Show the final dataframe
final_df.show()
