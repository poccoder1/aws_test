from pyspark.sql.functions import explode

# Load the XML data into a DataFrame
df = spark.read.format("xml").options(rowTag="AsgnRpt").load("path/to/xml/file.xml")

# Flatten the DataFrame
flattened_df = df.selectExpr("AsgnRpt.*", "explode(PTY) as PTY", "PTY.*", "Instrmt.*", "Undly.*", "explode(Qty) as Qty")

# Display the resulting table
flattened_df.show()
