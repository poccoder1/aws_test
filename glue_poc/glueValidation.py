from pyspark.sql import SparkSession
from pyspark.sql.functions import substring, when

# Create SparkSession
spark = SparkSession.builder.appName("Fix_Delimited_Extractor").getOrCreate()

# Read the text file
data = spark.read.text("<path_to_text_file>")

# Read the config.json file
config = spark.read.json("<path_to_config_file>")

# Extract schema definition length from config file
schema_definition_length = config.select("extractor.Fix_Delimited.schemaDefinitionLength").collect()[0][0]

# Define the schema based on schema definition length
schema = ""
for key, value in schema_definition_length.items():
    schema += key + " string, "

# Remove trailing comma and space
schema = schema[:-2]

# Create dataframe with extracted columns
df = data.select(
    *[when(length(data.value) >= sum([schema_definition_length[key] for key in schema_definition_length.keys() if key < col]) + value,
           substring(data.value, sum([schema_definition_length[key] for key in schema_definition_length.keys() if key < col]) + 1, value))
          .otherwise(None)
          .alias(col)
      for col, value in schema_definition_length.items()]
)

# Filter out null values
df = df.filter(df[col].isNotNull())

# Create a temporary view
df.createOrReplaceTempView("temp_table")

# Select the columns in the desired order
final_df = spark.sql("SELECT " + schema + " FROM temp_table")

# Show the final dataframe
final_df.show()
