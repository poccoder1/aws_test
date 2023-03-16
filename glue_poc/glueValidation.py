import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame

# Define the job parameters
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'input_path', 'output_path'])

# Create a SparkContext and GlueContext
sc = SparkContext()
glueContext = GlueContext(sc)

# Read the input XML file as a DynamicFrame
input_dyf = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": [args['input_path']]},
    format="xml",
    transformation_ctx="input_dyf"
)

# Define a function to convert an XML node into a dictionary
def xml_node_to_dict(node):
    if node.getChildren():
        return {child.name: xml_node_to_dict(child) for child in node.getChildren()}
    else:
        return node.value

# Extract the root node from the input file
root_node = input_dyf.root

# Extract the child nodes from the root node
child_nodes = root_node.getChildren()

# Create an empty list to hold the table rows
table_rows = []

# Loop over the child nodes and extract the data into table rows
for child_node in child_nodes:
    table_row = {}
    for field in child_node.getFields():
        if isinstance(field.value, list):
            table_row[field.name] = []
            for list_item in field.value:
                table_row[field.name].append(xml_node_to_dict(list_item))
        else:
            table_row[field.name] = xml_node_to_dict(field)
    table_rows.append(table_row)

# Convert the table rows into a DynamicFrame
output_dyf = DynamicFrame.fromDF(
    spark.createDataFrame(table_rows),
    glueContext,
    "output_dyf"
)

# Write the output DynamicFrame to S3 in tabular format
glueContext.write_dynamic_frame.from_options(
    frame=output_dyf,
    connection_type="s3",
    connection_options={"path": args['output_path'], "partitionKeys": []},
    format="csv",
    transformation_ctx="output_dyf"
)
