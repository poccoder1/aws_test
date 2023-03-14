import xml.etree.ElementTree as ET
import pandas as pd

def parse_xml_to_df(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    df = pd.DataFrame(columns=[child.tag for child in root[0]])

    for child in root:
        row = {}
        for element in child:
            if len(element) == 0:
                row[element.tag] = element.text
            else:
                row[element.tag] = json.dumps(xml_to_dict(element))
        df = df.append(row, ignore_index=True)

    return df

def xml_to_dict(xml_element):
    if len(xml_element) == 0:
        return xml_element.text
    else:
        return {child.tag: xml_to_dict(child) for child in xml_element}

# Example usage:
xml_file = "example.xml"

df = parse_xml_to_df(xml_file)
print(df)
