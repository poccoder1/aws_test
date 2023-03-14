def parse_xml_to_df(xml_string):
    root = ET.fromstring(xml_string)
    df = pd.DataFrame(columns=[child.tag for child in root[0]])

    for child in root:
        row = {}
        for element in child:
            if len(element) == 0:
                row[element.tag] = element.text
            else:
                row[element.tag] = json.dumps(xml_to_dict(element))
        df = df.append(row, ignore_index=True)

    df.set_index('name', inplace=True)
    return df
