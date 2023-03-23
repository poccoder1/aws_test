from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import from_unixtime

# create SparkSession
spark = SparkSession.builder.appName("XMLReader").getOrCreate()

# read XML file
xml_df = spark.read \
    .format("com.databricks.spark.xml") \
    .option("rowTag", "AsgnRpt") \
    .load("path/to/xml/file.xml")

# flatten all nested tags
flat_df = xml_df.selectExpr("*", "explode(PTY) as PTY_expanded", "explode(Qty) as Qty_expanded") \
    .drop("PTY", "Qty") \
    .selectExpr("*", "PTY_expanded._id as PTY_ID", "PTY_expanded._r as PTY_R", "Qty_expanded._short as Qty_Short", "Qty_expanded._typ as Qty_Typ") \
    .drop("PTY_expanded", "Qty_expanded") \
    .withColumn("RptID", xml_df["_RptID"]) \
    .withColumn("BizDt", from_unixtime(xml_df["_BizDt"], "yyyy-MM-dd")) \
    .withColumn("SetSesID", xml_df["_SetSesID"]) \
    .withColumn("UndSetPx", xml_df["_UndSetPx"]) \
    .withColumn("AsgnMeth", xml_df["_AsgnMeth"]) \
    .withColumnRenamed("_Ccy", "Ccy") \
    .withColumn("Sub_Id", xml_df["PTY.Sub._Id"]) \
    .withColumn("Sub_Type", xml_df["PTY.Sub._type"]) \
    .withColumn("Instrmt_ID", xml_df["Instrmt._ID"]) \
    .withColumn("SecType", xml_df["Instrmt._SecType"]) \
    .withColumn("MMY", xml_df["Instrmt._MMY"]) \
    .withColumn("Exch", xml_df["Instrmt._Exch"]) \
    .withColumn("StrKPx", xml_df["Instrmt._StrKPx"]) \
    .withColumn("PutCall", xml_df["Instrmt._PutCall"]) \
    .withColumn("Fctr", xml_df["Instrmt._Fctr"]) \
    .withColumn("PCFctr", xml_df["Instrmt._PCFctr"]) \
    .withColumn("Undly_ID", xml_df["Undly._ID"]) \
    .withColumn("SecTyp", xml_df["Undly._SecTyp"]) \
    .withColumn("Undly_MMY", xml_df["Undly._MMY"]) \
    .withColumn("Undly_Exch", xml_df["Undly._Exch"]) \
    .drop("_RptID", "_BizDt", "_SetSesID", "_UndSetPx", "_AsgnMeth", "PTY.Sub._Id", "PTY.Sub._type", "Instrmt._ID", "Instrmt._SecType", "Instrmt._MMY", "Instrmt._Exch", "Instrmt._StrKPx", "Instrmt._PutCall", "Instrmt._Fctr", "Instrmt._PCFctr", "Undly._ID", "Undly._SecTyp", "Undly._MMY", "Undly._Exch")

# show flattened data
flat_df.show()

###

