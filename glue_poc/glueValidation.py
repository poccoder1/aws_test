import xml.etree.ElementTree as ET
import csv


s3_client = boto3.client('s3')
s3_object = s3_client.get_object(Bucket='your-bucket-name', Key='your-file-name.xml')
xml_data = s3_object['Body'].read().decode('utf-8')



def xml_to_csv(xml_data):
    # parse the XML data
    root = ET.fromstring(xml_data)

    # get the column names from the XML data
    column_names = []
    for child in root[0]:
        if len(child.attrib) > 0:
            column_names.append(list(child.attrib.keys())[0])
        else:
            for subchild in child:
                column_names.append(list(subchild.attrib.keys())[0])

    # write the CSV data
    csv_data = []
    csv_data.append(column_names)
    for child in root:
        row = []
        for column_name in column_names:
            if root[0].findall(f'*[@{column_name}]'):
                row.append(child.attrib[column_name])
            else:
                subchild = child.find(f'./*/*[@{column_name}]')
                if subchild is not None:
                    row.append(subchild.attrib[column_name])
                else:
                    row.append('')
        csv_data.append(row)

    # convert the CSV data to a string
    csv_string = ''
    for row in csv_data:
        csv_string += ','.join(row) + '\n'

    return csv_string
