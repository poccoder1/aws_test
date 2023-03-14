import xml.etree.ElementTree as ET
import pandas as pd

# Parse XML file and get root element
tree = ET.parse('filename.xml')
root = tree.getroot()

# Create list to hold dictionaries of element data
elements_list = []

# Iterate over all child elements of root
for elem in root.iter():
    # Get element tag and attributes
    tag = elem.tag
    attributes = elem.attrib

    # Create dictionary to hold element data
    element_dict = {'tag': tag}

    # Add attributes to dictionary
    if attributes:
        element_dict.update(attributes)

    # Add text of element to dictionary
    if elem.text and elem.text.strip():
        element_dict['text'] = elem.text.strip()

    # Append dictionary to list
    elements_list.append(element_dict)

# Convert list of dictionaries to pandas DataFrame
df = pd.DataFrame(elements_list)

# Output DataFrame as table
print(df.to_string(index=False))
