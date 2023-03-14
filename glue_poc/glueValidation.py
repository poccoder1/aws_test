import xml.etree.ElementTree as ET
import pandas as pd

def parse_xml_to_df(xml_str):
    root = ET.fromstring(xml_str)
    rows = []
    columns = []
    for child in root:
        if not columns:
            columns.append('Index')
            for element in child.iter():
                columns.append(element.tag)
            columns = [col.replace('{http://www.fixprotocol.org/FIXML-5-0-SP2}', '') for col in columns]
            columns = [col.replace('_', ' ') for col in columns]
        row = [str(i) for i in range(len(rows)+1)]
        for element in child.iter():
            if element.text:
                row.append(element.text)
            else:
                row.append('')
        rows.append(row)
    return pd.DataFrame(rows, columns=columns)