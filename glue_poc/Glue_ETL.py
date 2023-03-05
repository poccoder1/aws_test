from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame

# Initialize GlueContext
glueContext = GlueContext(SparkContext.getOrCreate())

# Define source path and format
src_path = "s3://my-bucket/my-file.csv"
src_format = "csv"

# Read data from source file into a DynamicFrame
dynamic_frame = glueContext.create_dynamic_frame_from_options(
    connection_type="s3",
    format=src_format,
    connection_options={"paths": [src_path]},
    transformation_ctx="dynamic_frame"
)

# Print schema and show data
print(dynamic_frame.schema())
dynamic_frame.show()
