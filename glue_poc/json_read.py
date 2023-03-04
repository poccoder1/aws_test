import json
import logging

# set up logging
logging.basicConfig(filename='example.log', level=logging.INFO)

# define the methods to be called
def validate(config):
    try:
        # do validation logic here
        print(f"Validating with config: {config}")
        logging.info(f"Validating with config: {config}")
    except Exception as e:
        logging.error(f"Error validating with config {config}: {str(e)}")

def enrich(config):
    try:
        # do enrichment logic here
        print(f"Enriching with config: {config}")
        logging.info(f"Enriching with config: {config}")
    except Exception as e:
        logging.error(f"Error enriching with config {config}: {str(e)}")

def append(config):
    try:
        # do append logic here
        print(f"Appending with config: {config}")
        logging.info(f"Appending with config: {config}")
    except Exception as e:
        logging.error(f"Error appending with config {config}: {str(e)}")

def produce(config):
    try:
        # do produce logic here
        print(f"Producing with config: {config}")
        logging.info(f"Producing with config: {config}")
    except Exception as e:
        logging.error(f"Error producing with config {config}: {str(e)}")

def archive(config):
    try:
        # do archive logic here
        print(f"Archiving with config: {config}")
        logging.info(f"Archiving with config: {config}")
    except Exception as e:
        logging.error(f"Error archiving with config {config}: {str(e)}")

def writer(config):
    try:
        # do writer logic here
        print(f"Writing with config: {config}")
        logging.info(f"Writing with config: {config}")
    except Exception as e:
        logging.error(f"Error writing with config {config}: {str(e)}")

# read the JSON configuration from a file
with open('config.json', 'r') as f:
    config_dict = json.load(f)

print(f"Config dict: {config_dict}")

# define a dictionary that maps each key name to the corresponding method
method_map = {
    'validator': validate,
    'enricher': enrich,
    'appender': append,
    'producer': produce,
    'archiver': archive,
    'writer': writer
}

print(f"Method map: {method_map}")

# loop over the "config" list and call the appropriate method for each item in order
for item in config_dict['config']:
    for key, value in item.items():
        if key in method_map:
            method_map[key](value)
        else:
            logging.warning(f"No method found for key: {key}")


#=========

{"config":[{"validator":{"LENGTH":{"LESS_THAN":[{"col1":10},{"col2":13},{"col3":63},{"col4":43},{"col5":33},{"col6":23}],"EQUAL":[{"col2":13},{"col3":63},{"col4":43}]}}},{"enricher":{"DATA_MAN":{"sql":"select * from temp"}}},{"appender":{"DATA_MAN":{"sql":"select * from temp"}}},{"enricher":{"DATA_MAN":{"sql":"select * from temp"}}},{"producer":{"DATA_MAN":{"sql":"select * from temp"}}},{"archiver":{"DATA_MAN":{"sql":"select * from temp"}}}]}