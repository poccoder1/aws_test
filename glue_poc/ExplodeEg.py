from pyspark.sql.functions import explode

df = spark.read.format("com.databricks.spark.xml") \
    .option("rowTag", "AsgnRpt") \
    .load("file.xml")

df_exploded_pty = df.selectExpr(
    "RptID", "BizDt", "Ccy", "SetSesID", "UndSetPx", "AsgnMeth",
    "explode(PTY) as PTY"
).selectExpr(
    "RptID", "BizDt", "Ccy", "SetSesID", "UndSetPx", "AsgnMeth",
    "PTY.ID as PTY_ID", "PTY.R as PTY_R"
)

df_exploded_qty = df.selectExpr(
    "RptID", "BizDt", "Ccy", "SetSesID", "UndSetPx", "AsgnMeth",
    "explode(Qty) as Qty"
).selectExpr(
    "RptID", "BizDt", "Ccy", "SetSesID", "UndSetPx", "AsgnMeth",
    "Qty.Short as Qty_Short", "Qty.Typ as Qty_Typ"
)

df_final = df.selectExpr(
    "RptID", "BizDt", "Ccy", "SetSesID", "UndSetPx", "AsgnMeth",
    "Instrmt.ID as Instrmt_ID", "Instrmt.SecType as Instrmt_SecType",
    "Instrmt.MMY as Instrmt_MMY", "Instrmt.Exch as Instrmt_Exch",
    "Instrmt.StrKPx as Instrmt_StrKPx", "Instrmt.PutCall as Instrmt_PutCall",
    "Instrmt.Fctr as Instrmt_Fctr", "Instrmt.PCFctr as Instrmt_PCFctr",
    "Undly.ID as Undly_ID", "Undly.SecTyp as Undly_SecTyp",
    "Undly.MMY as Undly_MMY", "Undly.Exch as Undly_Exch"
)

df_final = df_final.crossJoin(df_exploded_pty).crossJoin(df_exploded_qty).select(
    "RptID", "BizDt", "Ccy", "SetSesID", "UndSetPx", "AsgnMeth",
    "PTY_ID", "PTY_R", "Qty_Short", "Qty_Typ",
    "Instrmt_ID", "Instrmt_SecType", "Instrmt_MMY", "Instrmt_Exch",
    "Instrmt_StrKPx", "Instrmt_PutCall", "Instrmt_Fctr", "Instrmt_PCFctr",
    "Undly_ID", "Undly_SecTyp", "Undly_MMY", "Undly_Exch"
)

df_final.show()
