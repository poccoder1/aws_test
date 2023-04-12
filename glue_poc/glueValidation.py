from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, flatten

# Create a SparkSession
spark = SparkSession.builder.appName('XML to CSV').getOrCreate()

# Load the XML data
xml_data = spark.read.format('xml').option('rowTag', 'Report').load('path/to/xml_file.xml')

# Flatten the nested columns
flattened_data = xml_data.select(flatten(xml_data.columns))

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
    'LiquAdj_exp._component',
    'LiquAdj_exp._VALUE'
)

# Write the output to a CSV file
output_data.write.csv('path/to/output_file.csv', header=True)

# Stop the SparkSession
spark.stop()
