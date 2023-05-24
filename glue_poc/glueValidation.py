
# Generate CSV schema based on JSON schema
def process_schema(schema, parent_key=''):
    csv_schema = []
    for key, value in schema.items():
        current_key = f"{parent_key}.{key}" if parent_key else key
        if value.get('type') == 'object':
            nested_schema = value.get('properties', {})
            nested_csv_schema = process_schema(nested_schema, parent_key=current_key)
            csv_schema.extend(nested_csv_schema)
        else:
            csv_schema.append((current_key, value.get('type')))
    return csv_schema

csv_schema = process_schema(json_schema['data']['items']['properties'])

# Convert CSV to JSON using the provided schema
json_data_frame = ApplyMapping.apply(
    frame=data_frame,
    mappings=[
        (column_name, column_type, column_name)
        for column_name, column_type in csv_schema
    ]
)