from pyspark.sql.types import StructType, StructField, StringType, ArrayType, DoubleType

# Define the schema for the XML file
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, ArrayType

schema = StructType([
    StructField("Report", StructType([
        StructField("rptHdr", StructType([
            StructField("exchNam", StringType()),
            StructField("rptCod", StringType())
        ])),
        StructField("reportNameGrp", StructType([
            StructField("cm", StructType([
                StructField("rptSubHdr", StructType([
                    StructField("membLglNam", StringType()),
                    StructField("membId", StringType())
                ])),
                StructField("acctTyGrp", StructType([
                    StructField("LiquidationGrp", StructType([
                        StructField("Name", StringType()),
                        StructField("LiquAdj", ArrayType(StructType([
                            StructField("component", StringType()),
                            StructField("value", DoubleType())
                        ])))
                    ]))
                ]))
            ])),
            StructField("RC", ArrayType(StructType([
                StructField("rptSubHdr", StructType([
                    StructField("membLglNam", StringType()),
                    StructField("membId", StringType())
                ])),
                StructField("acctTyGrp", ArrayType(StructType([
                    StructField("LiquidationGrp", StructType([
                        StructField("Name", StringType()),
                        StructField("currMarComp", StructType([
                            StructField("Name", StringType()),
                            StructField("MarketRisk_Aggr_T", DoubleType()),
                            StructField("MarketRisk_Aggr_T-1", DoubleType()),
                            StructField("LiquAdj", ArrayType(StructType([
                                StructField("component", StringType()),
                                StructField("value", DoubleType())
                            ])))
                        ])),
                        StructField("LiquAdj", ArrayType(StructType([
                            StructField("component", StringType()),
                            StructField("value", DoubleType())
                        ])))
                    ]))
                ])))
            ]))
        ]))
    ]))
])


# Read the XML file with the defined schema
df = spark.read.format("com.databricks.spark.xml").option("rowTag", "Report").schema(schema).load("path/to/xml/file")

# Get the array type fields
array_fields = [field.name for field in df.schema.fields if isinstance(field.dataType, ArrayType)]

# Print the array type fields
print(array_fields)
