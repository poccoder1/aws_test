############# working 1#########

import xml.etree.ElementTree as ET
import csv

# Parse the XML file
tree = ET.parse('input.xml')
root = tree.getroot()

# Extract the data
rows = []
for asgn_rpt in root.findall('AsgnRpt'):
    row = []
    row.append(asgn_rpt.get('RptID'))
    row.append(asgn_rpt.get('BizDt'))
    row.append(asgn_rpt.get('Ccy'))
    row.append(asgn_rpt.get('SetSesID'))
    row.append(asgn_rpt.get('UndSetPx'))
    row.append(asgn_rpt.get('AsgnMeth'))
    for pty in asgn_rpt.findall('PTY'):
        row.append(pty.get('ID'))
        row.append(pty.get('R'))
        sub = pty.find('Sub')
        if sub is not None:
            row.append(sub.get('Id'))
            row.append(sub.get('type'))
    instrmt = asgn_rpt.find('Instrmt')
    row.append(instrmt.get('ID'))
    row.append(instrmt.get('SecType'))
    row.append(instrmt.get('MMY'))
    row.append(instrmt.get('Exch'))
    row.append(instrmt.get('StrKPx'))
    row.append(instrmt.get('PutCall'))
    row.append(instrmt.get('Fctr'))
    row.append(instrmt.get('PCFctr'))
    undly = asgn_rpt.find('Undly')
    row.append(undly.get('ID'))
    row.append(undly.get('SecTyp'))
    row.append(undly.get('MMY'))
    row.append(undly.get('Exch'))
    for qty in asgn_rpt.findall('Qty'):
        row.append(qty.get('Short'))
        row.append(qty.get('Typ'))
    rows.append(row)

# Write the data into a CSV file
with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['RptID', 'BizDt', 'Ccy', 'SetSesID', 'UndSetPx', 'AsgnMeth', 'PTY ID', 'PTY R', 'Sub ID', 'Sub type', 'Instrmt ID', 'Instrmt SecType', 'Instrmt MMY', 'Instrmt Exch', 'Instrmt StrKPx', 'Instrmt PutCall', 'Instrmt Fctr', 'Instrmt PCFctr', 'Undly ID', 'Undly SecTyp', 'Undly MMY', 'Undly Exch', 'Qty Short', 'Qty Typ'])
    for row in rows:
        writer.writerow(row)
##########

import xml.etree.ElementTree as ET
import pandas as pd

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

        # Iterate over each attribute of the element and add it to the row dictionary
        for attr, value in element.attrib.items():
            row[attr] = value

        # Iterate over each child element and add its attributes to the row dictionary
        for child in element:
            for attr, value in child.attrib.items():
                row[child.tag + '_' + attr] = value

        # Append the row to the list of rows
        rows.append(row)

    # Create a pandas DataFrame from the list of rows
    df = pd.DataFrame(rows)

    # Write the DataFrame to a CSV file
    df.to_csv(csv_file, index=False)

# Example usage
xml_to_csv('input.xml', 'example.csv')
