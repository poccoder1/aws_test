from pyspark.sql import SparkSession
from pyspark.sql.functions import explode

# Create a Spark session
spark = SparkSession.builder.appName("XML to CSV").getOrCreate()

# Read the XML file as a Spark DataFrame
df = spark.read.format("xml").option("rowTag", "AsgnRpt").load("path/to/xml/file.xml")

# Flatten the nested structure of the PTY and Sub elements
df_flat = df.selectExpr("RptID", "BizDt", "Ccy", "SetSesID", "UndSetPx", "AsgnMeth",
                        "explode(PTY) as PTY", "Instrmt.*", "Undly.*", "explode(Qty) as Qty")

# Extract the desired columns and rename them
df_csv = df_flat.selectExpr(
    "RptID",
    "BizDt",
    "Ccy",
    "SetSesID",
    "UndSetPx",
    "AsgnMeth",
    "PTY.@ID as PTY_ID",
    "PTY.@R as PTY_R",
    "PTY.Sub.@Id as Sub_Id",
    "PTY.Sub.@type as Sub_type",
    "ID as Instrmt_ID",
    "SecType as Instrmt_SecType",
    "MMY as Instrmt_MMY",
    "Exch as Instrmt_Exch",
    "StrKPx as Instrmt_StrKPx",
    "PutCall as Instrmt_PutCall",
    "Fctr as Instrmt_Fctr",
    "PCFctr as Instrmt_PCFctr",
    "_ID as Undly_ID",
    "_SecTyp as Undly_SecTyp",
    "_MMY as Undly_MMY",
    "_Exch as Undly_Exch",
    "Qty.@Short as Qty_Short",
    "Qty.@Typ as Qty_Typ"
)

# Write the CSV file
df_csv.write.csv("path/to/csv/file.csv", header=True)
