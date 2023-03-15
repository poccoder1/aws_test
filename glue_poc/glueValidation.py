import xml.etree.ElementTree as ET
import pandas as pd

def xml_to_dataframe(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extract all unique tags as column names
    all_tags = set([elem.tag for elem in root.iter()])
    column_names = list(all_tags)

    # Extract all attributes as additional column names
    all_attributes = set([attr for elem in root.iter() for attr in elem.attrib.keys()])
    column_names += list(all_attributes)

    # Loop through each element and extract its values
    rows = []
    for elem in root.iter():
        row = {}
        for column in column_names:
            if column in elem.attrib:
                row[column] = elem.attrib[column]
            else:
                if elem.find(column) is not None:
                    if elem.find(column).text is not None:
                        row[column] = elem.find(column).text
                    else:
                        row[column] = ''
                else:
                    row[column] = ''
        rows.append(row)

    # Convert to a Pandas DataFrame
    df = pd.DataFrame(rows, columns=column_names)

    return df
