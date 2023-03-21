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
        Check(spark, CheckLevel.Warning, "Maximum length check for all columns", [
            SizeConstraint(column, ">", 0) for column in df.columns
        ]),
        Check(spark, CheckLevel.Warning, "Null check for all columns", [
            CompletenessConstraint(column) for column in df.columns
        ])
    ],
)

# run the checks and get the results
result = VerificationSuite(spark).onData(df).addChecks(checks).run()

# print the results
print(result.checkResults)
