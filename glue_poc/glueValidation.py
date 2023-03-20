from pyspark.sql import SparkSession
from pydeequ.checks import *
from pydeequ.verification import *

# create a SparkSession
spark = SparkSession.builder.appName("DataQualityCheck").getOrCreate()

# create a sample DataFrame
data = [("foo", "bar", 1),
        ("foo", "bar", 2),
        ("foo", "baz", 3),
        ("foo", "bar", None),
        ("foo", "bar", 5),
        ("foo", "bar", 6)]

df = spark.createDataFrame(data, ["col1", "col2", "col3"])

# define the constraints
constraints = ConstraintSet(
    [SizeConstraint(lambda x: x == 6),
     ColumnConstraint("col1", "maximum_length", lambda x: x <= 10),
     ColumnConstraint("col2", "isEqualTo", "bar"),
     ColumnConstraint("col3", "isNotNull")])

# run the verification
result = VerificationSuite(spark).onData(df).addChecks([constraints]).run()

# print the verification results
for check_result in result.checkResults:
    print(check_result)
