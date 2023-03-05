# Define logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Redirect printSchema() output to logger
logger.info("Schema:")
dynamic_frame.printSchema(log_level=logging.INFO)