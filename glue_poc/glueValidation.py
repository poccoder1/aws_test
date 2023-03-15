import xml.etree.ElementTree as ET
import pandas as pd

def xml_to_df(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    rows = []
    column_names = set()
    for child in root:
        row = {}
        for sub_child in child.iter():
            column_names.add(sub_child.tag)
            row[sub_child.tag] = sub_child.text
        rows.append(row)
    df = pd.DataFrame(rows, columns=sorted(column_names))
    return df
