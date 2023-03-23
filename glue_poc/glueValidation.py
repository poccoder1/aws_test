import xml.etree.ElementTree as ET
from pyspark.sql.types import StructType, StructField, StringType

# Define a function to recursively generate schema from XML element
def generate_schema(xml_element):
    schema = []
    for child_element in xml_element:
        field_name = child_element.tag
        field_type = StringType()
        if child_element.attrib:
            field_type = StructType([StructField("@" + k, StringType()) for k in child_element.attrib.keys()])
        child_schema = StructField(field_name, field_type, True)
        if len(child_element) > 0:
            child_schema.dataType = StructType(generate_schema(child_element))
        schema.append(child_schema)
    return schema

# Parse the XML and generate schema
xml_string = ''
