import xml.etree.ElementTree as ET
from pyspark.sql.types import StructType, StructField, StringType

# Parse the XML file
xml_file = "path/to/your/xml/file.xml"
tree = ET.parse(xml_file)
root = tree.getroot()

# Define a function to generate the schema for a given XML element
def generate_schema(elem, unique_tags):
    schema = []
    for child in elem:
        if child.tag in unique_tags:
            continue
        else:
            unique_tags.add(child.tag)
        if child.tag not in [e.tag for e in elem.findall("*")]:
            # Add a new field to the schema for scalar values
            schema.append(StructField("@" + child.tag, StringType()))
        else:
            # Add a new field to the schema for nested structures
            field = StructField(child.tag, generate_schema(child, unique_tags), True)
            for attr in child.attrib:
                field.add(StructField("@" + attr, StringType()))
            schema.append(field)
    return StructType(schema)

# Generate the input schema dynamically
input_schema = generate_schema(root, set())
