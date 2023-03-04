import json
import logging


def validate_length_less_than(column, length):
    try:
        print(f"Validating column '{column}' is less than {length}")
        logging.info(f"Validating column '{column}' is less than {length}")
        # add validation logic here
    except Exception as e:
        logging.error(f"Error validating length for column '{column}': {str(e)}")


def validate_length_equal(column, length):
    try:
        print(f"Validating column '{column}' is equal to {length}")
        logging.info(f"Validating column '{column}' is equal to {length}")
        # add validation logic here
    except Exception as e:
        logging.error(f"Error validating length for column '{column}': {str(e)}")


def validate_length(length_config):
    try:
        # Check for the presence of a validation type (LESS_THAN or EQUAL)
        if "LESS_THAN" in length_config:
            validation_type = "LESS_THAN"
        elif "EQUAL" in length_config:
            validation_type = "EQUAL"
        else:
            logging.warning(f"No length validation type found in config: {length_config}")
            return

        # Define a dictionary of length validation functions and their corresponding validation types
        length_validation_functions = {
            "LESS_THAN": validate_length_less_than,
            "EQUAL": validate_length_equal,
            # Add more length validation functions here as needed
        }

        # Iterate over the validation type (LESS_THAN or EQUAL) and call the corresponding validation function
        for validation in length_config[validation_type]:
            for col, val in validation.items():
                if validation_type in length_validation_functions:
                    length_validation_functions[validation_type](col, val)
                else:
                    logging.warning(f"No length validation function found for validation type '{validation_type}'")
                    return

    except Exception as e:
        logging.error(f"Error validating length with config {length_config}: {str(e)}")


def enrich_data(data_man_config):
    try:
        sql = data_man_config["sql"]
        print(f"Enriching data using SQL: {sql}")
        logging.info(f"Enriching data using SQL: {sql}")
        # add enrichment logic here
    except Exception as e:
        logging.error(f"Error enriching data with config {data_man_config}: {str(e)}")


def append_data(data_man_config):
    try:
        sql = data_man_config["sql"]
        print(f"Appending data using SQL: {sql}")
        logging.info(f"Appending data using SQL: {sql}")
        # add append logic here
    except Exception as e:
        logging.error(f"Error appending data with config {data_man_config}: {str(e)}")


def produce_data(data_man_config):
    try:
        sql = data_man_config["sql"]
        print(f"Producing data using SQL: {sql}")
        logging.info(f"Producing data using SQL: {sql}")
        # add production logic here
    except Exception as e:
        logging.error(f"Error producing data with config {data_man_config}: {str(e)}")


def archive_data(data_man_config):
    try:
        sql = data_man_config["sql"]
        print(f"Archiving data using SQL: {sql}")
        logging.info(f"Archiving data using SQL: {sql}")
        # add archive logic here
    except Exception as e:
        logging.error(f"Error archiving data with config {data_man_config}: {str(e)}")


def write_data(data_man_config):
    try:
        sql = data_man_config["sql"]
        print(f"Writing data using SQL: {sql}")
        logging
