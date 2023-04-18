from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType, FloatType

schema = StructType([
    StructField("Batch", StructType([
        StructField("PostRpt", StructType([
            StructField("@RptID", StringType()),
            StructField("@BizDt", DateType()),
            StructField("@SetPx", FloatType()),
            StructField("Pty", StructType([
                StructField("@ID", StringType()),
                StructField("@R", IntegerType()),
                StructField("Sub", StructType([
                    StructField("@ID", IntegerType()),
                    StructField("@Typ", StringType())
                ]))
            ])),
            StructField("Instrmt", StructType([
                StructField("@ID", StringType()),
                StructField("@SecTyp", StringType()),
                StructField("@MMY", StringType()),
                StructField("@Exch", StringType()),
                StructField("@UOM", StringType())
            ])),
            StructField("Qty", StructType([
                StructField("@Long", IntegerType()),
                StructField("@Short", IntegerType()),
                StructField("@Typ", StringType())
            ])),
            StructField("Amt", StructType([
                StructField("@Typ", StringType()),
                StructField("@Amt", FloatType()),
                StructField("@Ccy", StringType())
            ]))
        ])),
        StructField("TrdCaptRpt", StructType([
            StructField("@RptID", StringType()),
            StructField("@BizDt", DateType()),
            StructField("Instrmt", StructType([
                StructField("@ID", StringType()),
                StructField("@Fctr", IntegerType())
            ])),
            StructField("Amt", StructType([
                StructField("@Typ", StringType()),
                StructField("@Amt", FloatType()),
                StructField("@Ccy", StringType())
            ])),
            StructField("Pty", StructType([
                StructField("@ID", StringType()),
                StructField("@R", IntegerType()),
                StructField("Sub", StructType([
                    StructField("@ID", IntegerType()),
                    StructField("@Typ", StringType())
                ]))
            ])),
            StructField("RegTrdID", StructType([
                StructField("@ID", StringType())
            ]))
        ]))
    ]))
