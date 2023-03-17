import sys
 from awsglue.transforms import *
 from awsglue.utils import getResolvedOptions
 from pyspark.context import SparkContext
 from awsglue.context import GlueContext
 from awsglue.dynamicframe import DynamicFrame

 # Get the input and output paths from the job arguments
 args = getResolvedOptions(sys.argv, ['input_path', 'output_path'])

 # Create a Spark context and Glue context
 sc = SparkContext()
 glueContext = GlueContext(sc)

 # Read the input XML file as a DynamicFrame
 inputDf = glueContext \
     .read \
     .format("xml") \
     .option("rowTag", "*") \
     .option("excludeAttribute", "true") \
     .load(args['input_path'])

 # Flatten the DynamicFrame by exploding the desired fields
 def flatten_fields(df, field_name):
     flat_fields = []
     for field in df.schema.fields:
         if field.dataType.simpleString() == "struct":
             flat_fields += flatten_fields(df.select(field.name + ".*"), field_name + field.name + ".")
         else:
             flat_fields.append(field_name + field.name)
     return [col(col_name).alias(col_name.replace(field_name, "")) for col_name in flat_fields]

 explodedDf = inputDf \
     .select(flatten_fields(inputDf, ""))

 # Write the output DynamicFrame to the output path
 outputDf = DynamicFrame.fromDF(explodedDf, glueContext, "outputDf")
 outputDf \
     .write \
     .format("csv") \
     .option("header", "true") \
     .option("delimiter", ",") \
     .mode("overwrite") \
     .save(args['output_path'])