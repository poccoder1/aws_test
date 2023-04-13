from pyspark.sql.types import StructType, StructField, StringType, ArrayType, DoubleType

# Define the schema for the XML file
schema = StructType([
    StructField("Report", StructType([
        StructField("rptHdr", StructType([
            StructField("exchNam", StringType(), True),
            StructField("rptCod", StringType(), True)
        ]), True),
        StructField("reportNameGrp", StructType([
            StructField("cm", StructType([
                StructField("rptSubHdr", StructType([
                    StructField("membLglNam", StringType(), True),
                    StructField("membId", StringType(), True)
                ]), True),
                StructField("acctTyGrp", ArrayType(StructType([
                    StructField("Name", StringType(), True),
                    StructField("LiquidationGrp", StructType([
                        StructField("Name", StringType(), True),
                        StructField("currMarComp", StructType([
                            StructField("Name", StringType(), True),
                            StructField("MarketRisk_Aggr_T", DoubleType(), True),
                            StructField("MarketRisk_Aggr_T-1", DoubleType(), True),
                            StructField("LiquAdj", ArrayType(StructType([
                                StructField("component", StringType(), True),
                                StructField("value", DoubleType(), True)
                            ]), True), True)
                        ]), True),
                        StructField("LiquAdj", ArrayType(StructType([
                            StructField("component", StringType(), True),
                            StructField("value", DoubleType(), True)
                        ]), True), True)
                    ]), True))
            ]), True)
        ]), True),
        StructField("RC", ArrayType(StructType([
            StructField("rptSubHdr", StructType([
                StructField("membLglNam", StringType(), True),
                StructField("membId", StringType(), True)
            ]), True),
            StructField("acctTyGrp", ArrayType(StructType([
                StructField("Name", StringType(), True),
                StructField("LiquidationGrp", StructType([
                    StructField("Name", StringType(), True),
                    StructField("currMarComp", StructType([
                        StructField("Name", StringType(), True),
                        StructField("MarketRisk_Aggr_T", DoubleType(), True),
                        StructField("MarketRisk_Aggr_T-1", DoubleType(), True),
                        StructField("LiquAdj", ArrayType(StructType([
                            StructField("component", StringType(), True),
                            StructField("value", DoubleType(), True)
                        ]), True), True)
                    ]), True),
                    StructField("LiquAdj", ArrayType(StructType([
                        StructField("component", StringType(), True),
                        StructField("value", DoubleType(), True)
                    ]), True), True)
                ]), True))
        ]), True))
    ]), True)
]), True)
]), True)
])

# Read the XML file with the defined schema
df = spark.read.format("com.databricks.spark.xml").option("rowTag", "Report").schema(schema).load("path/to/xml/file")

# Get the array type fields
array_fields = [field.name for field in df.schema.fields if isinstance(field.dataType, ArrayType)]

# Print the array type fields
print(array_fields)
