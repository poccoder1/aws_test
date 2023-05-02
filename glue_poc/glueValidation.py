import boto3
import pandas as pd
import gzip

# Initialize AWS Glue context and S3 client
glueContext = GlueContext(SparkContext.getOrCreate())
s3_client = boto3.client('s3')

# Define the S3 bucket and file paths for input and output
bucket_name = 'your-bucket-name'
input_files = ['file1.gz', 'file2.gz', 'file3.gz']
output_file = 'merged_file.csv'

# Function to read gzipped CSV file from S3 and return DataFrame
def read_csv_from_s3(bucket, file_path):
    s3_object = s3_client.get_object(Bucket=bucket, Key=file_path)
    gzipped_content = s3_object['Body'].read()
    content = gzip.decompress(gzipped_content)
    df = pd.read_csv(content)
    return df

# List to hold individual DataFrames
dfs = []

# Read each gzipped CSV file and add its DataFrame to the list
for file in input_files:
    df = read_csv_from_s3(bucket_name, file)
    dfs.append(df)

# Concatenate all DataFrames into a single DataFrame
merged_df = pd.concat(dfs, ignore_index=True)

# Convert the merged DataFrame to CSV
output_csv = merged_df.to_csv(index=False)

# Write the merged CSV file to S3
s3_client.put_object(Body=output_csv, Bucket=bucket_name, Key=output_file)
