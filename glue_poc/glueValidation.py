from pyspark.sql.types import StructType

def get_all_columns(schema, prefix=''):
    columns = []
    for field in schema.fields:
        name = prefix + field.name
        if isinstance(field.dataType, StructType):
            columns += get_all_columns(field.dataType, name + '.')
        else:
            columns.append(name)
    return columns

# Assuming df is your PySpark DataFrame
all_columns = get_all_columns(df.schema)
print(all_columns)
