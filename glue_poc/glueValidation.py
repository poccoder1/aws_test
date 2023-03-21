from pyspark.sql.functions import col
from pyspark.sql import SparkSession
from pydeequ.checks import *
from pydeequ.verification import *

# create a SparkSession
spark = SparkSession.builder.appName("Data Quality Check").getOrCreate()

# read the input data into a dataframe
df = spark.read.format("csv").option("header", True).load("path/to/your/data.csv")

# create the checks
checks = Check(
    check_level=CheckLevel.Warning,
    checks=[
        Check(col("col1"), SizeConstraint(maximum=10)),
        Check(col("col2"), EqualsConstraint("constant_value")),
        Check(col("col3"), IsNotNullConstraint()),
    ],
)

# run the checks and get the results
result = VerificationSuite(spark).onData(df).addCheck(checks).run()

# print the results
print(result.checkResults)
