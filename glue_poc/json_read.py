def validate(config):
    try:
        # Define a dictionary of validation functions and their corresponding keys
        validation_functions = {
            "LENGTH": validate_length,
            "VALUE": validate_value,
            # Add more validation functions here as needed
        }

        # Iterate over the keys in the config and call the corresponding validation function
        for key in config:
            if key in validation_functions:
                validation_functions[key](config[key])
            else:
                logging.warning(f"No validation function found for key '{key}' in config: {config}")

    except Exception as e:
        logging.error(f"Error validating with config {config}: {str(e)}")


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

        # Iterate over the validation type (LESS_THAN or EQUAL)
        for validation in length_config[validation_type]:
            for col, val in validation.items():
                # call the length validation method with the column name and length
                if validation_type == "LESS_THAN":
                    validate_length_generic(col, val, "LESS_THAN")
                elif validation_type == "EQUAL":
                    validate_length_generic(col, val, "EQUAL")

    except Exception as e:
        logging.error(f"Error validating length with config {length_config}: {str(e)}")


def validate_value(value_config):
    try:
        # do value validation logic here
        print(f"Validating value with config: {value_config}")
        logging.info(f"Validating value with config: {value_config}")
    except Exception as e:
        logging.error(f"Error validating value with config {value_config}: {str(e)}")


def validate_length_generic(column, length, validation_type):
    try:
        if validation_type == "LESS_THAN":
            print(f"Validating column '{column}' is less than {length}")
            logging.info(f"Validating column '{column}' is less than {length}")
        elif validation_type == "EQUAL":
            print(f"Validating column '{column}' is equal to {length}")
            logging.info(f"Validating column '{column}' is equal to {length}")
        else:
            logging.warning(f"Unknown validation type '{validation_type}' for column '{column}'")
    except Exception as e:
        logging.error(f"Error validating length for column '{column}': {str(e)}")
