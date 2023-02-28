# Define the mapping as a dictionary with dynamic values
mapping = {'name': 'customer_name', 'age': 'customer_age', 'gender': 'customer_gender'}

# Add hardcoded currency column with header set to 'currency'
transformed_df = transformed_dyf.toDF()
transformed_df = transformed_df \
    .withColumn('currency', lit('USD').alias('currency'))

# Skip first row and collect remaining rows in a new DataFrame
rows = transformed_df \
    .rdd \
    .zipWithIndex() \
    .filter(lambda x: x[1] > 0) \
    .map(lambda x: x[0]) \
    .collect()
new_df = spark.createDataFrame(rows, transformed_df.schema)

# Rename columns dynamically based on a dictionary of column mappings
for current_name, new_name in mapping.items():
    new_df = new_df.withColumnRenamed(current_name, new_name)

# Write DataFrame to a single file
new_df \
    .coalesce(1) \
    .write \
    .format('parquet') \
    .mode('overwrite') \
    .option('compression', 'snappy') \
    .save('s3://my-bucket/output')
