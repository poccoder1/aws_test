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