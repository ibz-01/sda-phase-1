def validate(config): #validating config, 1-required fields, 2-data types

    fields = ["continent", "year", "operation"]
    
    missing_keys = list(
    filter(lambda key: key not in config or config[key] in [None, ""], fields)
    ) #checking either key doesnt exist, or key's value is "" or null

    if missing_keys:
        raise Exception(f"Missing required config fields: {missing_keys}")
    
    if not isinstance(config["year"], int):
        raise Exception("Year must be an integer")

    # operation validation
    if config["operation"] not in ["average", "sum"]:
        raise Exception("Operation must be 'average' or 'sum'")

    # optional country, must be string
    if "country" in config and config["country"] not in [None, ""]:
        
        if not isinstance(config["country"], str):
            raise Exception("Country must be a string")

    return True






        