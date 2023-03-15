import xml.etree.ElementTree as ET
import pandas as pd

# load the XML file
tree = ET.parse('example.xml')
root = tree.getroot()

# create an empty list to store dictionaries
rows = []

# iterate over the AsgnRpt tags
for asgn_rpt in root.findall('.//AsgnRpt'):
    row = {}

    # iterate over the child tags of each AsgnRpt
    for child in asgn_rpt:
        # check if the tag has any sub-tags
        if len(child) > 0:
            # if it has sub-tags, iterate over them and add their values to the row dictionary
            for sub in child:
                row[sub.tag] = sub.text
        else:
            # if the tag has no sub-tags, add its value to the row dictionary
            row[child.tag] = child.text

    # add the row dictionary to the rows list
    rows.append(row)

# create a pandas DataFrame from the rows list
df = pd.DataFrame(rows)

# print the resulting DataFrame
print(df)
