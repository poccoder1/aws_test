import xml.etree.ElementTree as ET
from pyspark.sql.types import StructType, StructField, StringType

# Parse the XML file
xml_file = "path/to/your/xml/file.xml"
tree = ET.parse(xml_file)
root = tree.getroot()

# Define a function to generate the schema for a given XML element
def generate_schema(elem):
    schema = []
    for child in elem:
        if child.tag not in [e.tag for e in elem.findall("*")]:
            # Add a new field to the schema for scalar values
            schema.append(StructField("@" + child.tag, StringType()))
        else:
            # Add a new field to the schema for nested structures
            schema.append(StructField(child.tag, generate_schema(child), True))
    return StructType(schema)

# Generate the input schema dynamically
input_schema = generate_schema(root)
