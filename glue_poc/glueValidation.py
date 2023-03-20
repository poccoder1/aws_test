from pyspark.sql import SparkSession
from pyspark.sql.functions import current_date
from pydeequ.checks import Check, CheckLevel, CheckStatus
from pydeequ.verification import VerificationSuite

# Create a SparkSession
spark = SparkSession.builder.appName("DataQualityCheck").getOrCreate()

# Load your dataset into a Spark DataFrame
df = spark.read.format("csv").option("header", "true").load("your_data.csv")

# Define the constraints to be checked
check = Check(spark, df) \
    .hasSize(lambda x: x >= 1) \
    .isComplete("col3") \
    .hasMinLength("col1", lambda x: x >= 0) \
    .hasMaxLength("col1", lambda x: x <= 10) \
    .isContainedIn("col2", ["constant_value"]) \
    .satisfies("col4", "today's date", lambda x: x == current_date()) \
    .isNumeric("col5")

# Run the verification
results = VerificationSuite(spark) \
    .onData(df) \
    .addCheck(check) \
    .run()

# Print the verification results
for check_result in results.checkResults:
    print(f"Check: {check_result.check.description}, Status: {check_result.status}, Constraint: {check_result.constraint}")
#========================

from pydeequ.checks import *
from pydeequ.verification import *

# Define the data quality checks
checks = [
    Check(col("col1").hasMaxLength(10), "col1 has maximum length of 10"),
    Check(col("col6").hasMaxLength(10), "col6 has maximum length of 10"),
    Check(col("col7").hasMaxLength(10), "col7 has maximum length of 10"),
    Check(col("col8").hasMaxLength(10), "col8 has maximum length of 10"),
    Check(col("col2") == "constant_value", "col2 is equals to some constant value"),
    Check(col("col3").isNotNull(), "col3 is not null"),
    Check(col("col4") == current_date(), "col4 is today's date"),
    Check(col("col5").isNumeric(), "col5 is numeric")
]

# Run the checks
results = VerificationSuite(spark) \
    .onData(df) \
    .addChecks(checks) \
    .run()

# Print the results
for result in results.checkResults:
    print(result)
