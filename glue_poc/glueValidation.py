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


filtered_dict = {k: v for k, v in my_dict.items() if  v.startswith('ArrayType[string]')}


for i, k in enumerate(my_dict):
    key_list = [k2 for k2 in my_dict.keys() if k2 != k]
    print(f"{k}: {key_list}")