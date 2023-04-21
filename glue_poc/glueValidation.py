import json
import csv
import pandas as pd

# Load JSON config
with open('config.json') as f:
    config = json.load(f)

# Get schema definition length for Fix_Delimited source
schema_definition_length = config['producer']['Fix_Delimited']['schemaDefinitionLength']

# Read CSV file into a DataFrame
df = pd.read_csv('data.csv')

# Iterate through columns in the DataFrame
for col_name in df.columns:
    # Check if column is specified in schema definition
    if col_name in schema_definition_length:
        col_len = schema_definition_length[col_name]
        # Trim data if length specified in schema definition
        df[col_name] = df[col_name].astype(str).str[:col_len]
        # Add whitespace padding if data is shorter than specified length
        df[col_name] = df[col_name].str.ljust(col_len)

# Write the DataFrame to a CSV file
df.to_csv('processed_data.csv', index=False)
