from awsglue.dynamicframe import DynamicFrame
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import explode
from pyspark.sql.session import SparkSession
from pyspark.sql.types import StructType, StructField, StringType

# Get the Glue job arguments
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'input_path', 'output_path'])

# Create a Spark context and session
sc = SparkContext()
spark = SparkSession(sc)

# Define the input schema
input_schema = StructType([
    StructField("AsgnRpt", StructType([
        StructField("@RptID", StringType()),
        StructField("@BizDt", StringType()),
        StructField("@Ccy", StringType()),
        StructField("@SetSesID", StringType()),
        StructField("@UndSetPx", StringType()),
        StructField("@AsgnMeth", StringType()),
        StructField("PTY", StructType([
            StructField("@ID", StringType()),
            StructField("@R", StringType()),
            StructField("Sub", StructType([
                StructField("@Id", StringType()),
                StructField("@type", StringType())
            ]))
        ], True),
                    StructField("Instrmt", StructType([
                        StructField("@ID", StringType()),
                        StructField("@SecType", StringType()),
                        StructField("@MMY", StringType()),
                        StructField("@Exch", StringType()),
                        StructField("@StrKPx", StringType()),
                        StructField("@PutCall", StringType()),
                        StructField("@Fctr", StringType()),
                        StructField("@PCFctr", StringType())
                    ], True),
                                StructField("Undly", StructType([
                                    StructField("@ID", StringType()),
                                    StructField("@SecTyp", StringType()),
                                    StructField("@MMY", StringType()),
                                    StructField("@Exch", StringType())
                                ], True),
                                            StructField("Qty", StructType([
                                                StructField("@Short", StringType()),
                                                StructField("@Typ", StringType())
                                            ], True))
    ], True))
])

# Read the input XML file
input_df = spark.read \
    .format("com.databricks.spark.xml") \
    .option("rowTag", "AsgnRpt") \
    .option("rootTag", "FIXML") \
    .schema(input_schema) \
    .load(args['input_path'])

# Flatten the input dataframe
output_df = input_df.selectExpr(
    "AsgnRpt.@RptID AS AsgnRpt_RptID",
    "AsgnRpt.@BizDt AS AsgnRpt_BizDt",
    "AsgnRpt.@Ccy AS AsgnRpt_Ccy",
    "AsgnRpt.@SetSesID AS AsgnRpt_SetSesID",
    "AsgnRpt.@UndSetPx AS AsgnRpt_UndSetPx",
    "AsgnRpt.@AsgnMeth AS AsgnRpt_AsgnMeth",
    "explode(PTY) AS PTY",
    "Instrmt.@ID AS AsgnRpt_Instrmt_ID",
    "Instrmt.@SecType AS AsgnRpt_Instrmt_SecType",
    "Instrmt.@MMY AS AsgnRpt_Instrmt_MMY",
    "Instrmt.@Exch AS AsgnRpt_Instrmt_Exch",
    "Instrmt.@StrKPx AS AsgnRpt_In")


#===========

from pyspark.sql.functions import explode

# Flatten the nested XML structure using spark-xml
df = spark.read.format("xml") \
    .option("rowTag", "AsgnRpt") \
    .load("path/to/xml/file")

# Create a flattened dataframe by exploding each nested array of structs
flat_df = df.selectExpr(
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

# Select the columns in the desired order and rename them as needed
output_df = flat_df.select(
    "RptID",
    "BizDt",
    "Ccy",
    "SetSesID",
    "UndSetPx",
    "AsgnMeth",
    "PTY.ID",
    "PTY.R",
    "PTY.Sub.Id",
    "PTY.Sub.type",
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
    "Qty.Short",
    "Qty.Typ"
).toDF(*[field.name.replace(".", "_") for field in schema])

output_df.show()


