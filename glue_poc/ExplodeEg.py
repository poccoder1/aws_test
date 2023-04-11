from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, concat_ws

# Create a SparkSession
spark = SparkSession.builder.appName("XML to CSV").getOrCreate()

# Read the XML file into a DataFrame
df = spark.read.format("com.databricks.spark.xml").options(rowTag="AsgnRpt").load("input.xml")

# Select the required columns and explode the PTY and Sub columns
df = df.selectExpr(
    "RptID",
    "BizDt",
    "Ccy",
    "SetSesID",
    "UndSetPx",
    "AsgnMeth",
    "explode(PTY) as PTY",
    "Instrmt.ID as Instrmt_ID",
    "Instrmt.SecType as Instrmt_SecType",
    "Instrmt.MMY as Instrmt_MMY",
    "Instrmt.Exch as Instrmt_Exch",
    "Instrmt.StrKPx as Instrmt_StrKPx",
    "Instrmt.PutCall as Instrmt_PutCall",
    "Instrmt.Fctr as Instrmt_Fctr",
    "Instrmt.PCFctr as Instrmt_PCFctr",
    "Undly.ID as Undly_ID",
    "Undly.SecTyp as Undly_SecTyp",
    "Undly.MMY as Undly_MMY",
    "Undly.Exch as Undly_Exch",
    "explode(Qty) as Qty"
)

# Select the required columns and concatenate the sub-columns
df = df.selectExpr(
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
    "Instrmt_ID",
    "Instrmt_SecType",
    "Instrmt_MMY",
    "Instrmt_Exch",
    "Instrmt_StrKPx",
    "Instrmt_PutCall",
    "Instrmt_Fctr",
    "Instrmt_PCFctr",
    "Undly_ID",
    "Undly_SecTyp",
    "Undly_MMY",
    "Undly_Exch",
    "Qty.@Short as Qty_Short",
    "Qty.@Typ as Qty_Typ"
)

# Write the data to a CSV file
df.write.option("header", "true").csv("output.csv")

# Stop the SparkSession
spark.stop()
