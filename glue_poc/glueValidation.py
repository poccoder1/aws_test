from pyspark.sql.functions import col
from pydeequ.checks import *
from pydeequ.verification import *

checks = [
    Analysis(
        Column("col1"),
        MaximumLength(len_=10),
        "col1 has maximum length of 10"
    ),
    Analysis(
        Column("col2"),
        IsEqualTo("constant_value"),
        "col2 is equals to some constant value"
    ),
    Analysis(
        Column("col3"),
        IsNotNull(),
        "col3 is not null"
    ),
]

# Run the checks
results = VerificationSuite(spark) \
    .onData(df) \
    .addChecks(checks) \
    .run()
