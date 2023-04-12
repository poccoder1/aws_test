from pyspark.sql.functions import explode, flatten, array, struct, lit

# Load the XML data
xml_data = spark.read.format('xml').option('rowTag', 'Report').load('path/to/xml_file.xml')

# Convert the DataFrame to a format that can be flattened
converted_data = xml_data.selectExpr("to_xml(struct(*)) AS xmls")

# Flatten the nested columns
flattened_data = spark.read.option("rowTag", "root").xml(converted_data.rdd.map(lambda r: r.xmls))

flattened_data = flattened_data.select(flatten(flattened_data.schema.names))

# Explode arrays
exploded_data = flattened_data.select('*', explode(flattened_data.acctTyGrp).alias('acctTyGrp_exp'))
exploded_data = exploded_data.select('*', explode(exploded_data.acctTyGrp_exp.LiquidationGrp).alias('LiquidationGrp_exp'))
exploded_data = exploded_data.select('*', explode(exploded_data.LiquidationGrp_exp.currMarComp.LiquAdj).alias('LiquAdj_exp'))

# Select only the necessary columns
output_data = exploded_data.select(
    'rptHdr.exchNam',
    'rptHdr.rptCod',
    'reportNameGrp.cm.rptSubHdr.membLglNam',
    'reportNameGrp.cm.rptSubHdr.membId',
    'acctTyGrp_exp._Name',
    'LiquidationGrp_exp._Name',
    'currMarComp._Name',
    'MarketRisk_Aggr_T',
    'MarketRisk_Aggr_T-1',
    struct(
        array(lit('LiquAdj_exp._component'), lit('LiquAdj_exp._VALUE'))
    ).alias('LiquAdj_exp')
)

# Write the output to a CSV file
output_data.write.csv('path/to/output_file.csv', header=True)
