from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.builder.appName("FileProcessing").getOrCreate()

# Define the input and output paths
input_path = "path/to/input_folder"
output_path = "path/to/output_folder"

# Read the file paths from the input folder
file_paths = spark.sparkContext.wholeTextFiles(input_path).keys().collect()

# Process each file in parallel
def process_file(file_path):
    # Read the XML file and convert it to a DataFrame
    df = spark.read.format("com.databricks.spark.xml") \
        .option("rowTag", "FIXML") \
        .load(file_path)

    # Perform any necessary transformations on the DataFrame

    # Save the DataFrame as a CSV file
    file_name = file_path.split("/")[-1].split(".")[0]  # Extract the file name
    output_file_path = output_path + "/" + file_name + ".csv"
    df.write.csv(output_file_path, header=True, mode="overwrite")

# Parallelize the processing of files
file_paths_rdd = spark.sparkContext.parallelize(file_paths)
file_paths_rdd.foreach(process_file)

# Stop the SparkSession
spark.stop()
