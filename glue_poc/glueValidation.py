import xml.etree.ElementTree as ET
import csv
import json
import logging

logging.basicConfig(filename='xml_parser.log', level=logging.ERROR)

def parse_xml_to_csv(xml_file_path, csv_file_path):
    try:
        # Open the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Open the CSV file for writing
        with open(csv_file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)

            # Write the header row
            header_row = []
            for child in root[0]:
                header_row.append(child.tag)
            writer.writerow(header_row)

            # Write each row of data
            for item in root:
                data_row = []
                for child in item:
                    if len(child) > 0:
                        # If the child has nested data, convert it to JSON format
                        data_row.append(json.dumps(xml_to_dict(child)))
                    else:
                        data_row.append(child.text)
                writer.writerow(data_row)
    except Exception as e:
        logging.exception(f'Error while parsing {xml_file_path}: {e}')

def xml_to_dict(xml):
    # Convert an XML element to a dictionary
    if len(xml) == 0:
        return xml.text
    result = {}
    for child in xml:
        if child.tag in result:
            if type(result[child.tag]) is not list:
                result[child.tag] = [result[child.tag]]
            result[child.tag].append(xml_to_dict(child))
        else:
            result[child.tag] = xml_to_dict(child)
    return result
