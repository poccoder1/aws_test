import xml.etree.ElementTree as ET
import pandas as pd

def process_element(element, row):
    # Add attributes of this element to the row dictionary
    for attr, value in element.attrib.items():
        row[attr] = value

    # Add the text value of the element to the row dictionary
    if element.text:
        row[element.tag] = element.text.strip()

    # Process child elements
    for child in element:
        # If the child has no child elements, add its attributes and text value to the row dictionary
        if not child:
            for attr, value in child.attrib.items():
                row[child.tag + '_' + attr] = value
            if child.text:
                row[child.tag] = child.text.strip()
        # If the child has child elements, process them recursively
        else:
            process_element(child, row)

def xml_to_csv(xml_file, csv_file):
    # Parse the XML file into an ElementTree object
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Create an empty list to store the rows of the DataFrame
    rows = []

    # Iterate over each element in the root
    for element in root:
        # Create an empty dictionary to store the values for this row
        row = {}

        # Process the element recursively
        process_element(element, row)

        # Append the row to the list of rows
        rows.append(row)

    # Create a pandas DataFrame from the list of rows
    df = pd.DataFrame(rows)

    # Write the DataFrame to a CSV file
    df.to_csv(csv_file, index=False)

xml_to_csv('input.xml', 'example.csv')
