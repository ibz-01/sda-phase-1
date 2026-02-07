def filter_data(data, continent=None, year=None, country=None):
    # data is a list of dictionaries
    data_list = data.to_dict("records")  # convert data to list of dicts

    if continent:
        data_list = list(filter(lambda x: x["Continent"] == continent, data_list))

    if year:
        data_list = list(filter(lambda x: x["Year"] == year, data_list))

    if country:
        data_list = list(filter(lambda x: x["Country Name"] == country, data_list))

    return data_list

def compute_statistic(data, operation="average"):
    # extract gdp values using map
    values = list(map(lambda x: x["Value"], data))

    if not values:  # checking if the list is empty or not
        return None

    if operation == "average":
        return sum(values) / len(values)
    elif operation == "sum":
        return sum(values)
    else:
        raise Exception("Invalid operation")




# example use
config = {
    "continent": "Asia",
    "year": 2020,
    "country": "Pakistan",
    "operation": "average"
}

# filtering
filtered_data = filter_data(df_long, continent=config["continent"], year=config["year"], country=config["country"])

# computing
result = compute_statistic(filtered_data, config["operation"])

print("Result:", result)
#
filtered_asia_2020 = filter_data(df_long, continent="Asia", year=2020)
sum_asia_2020 = compute_statistic(filtered_asia_2020, "sum")
print("Total GDP of Asia in 2020:", sum_asia_2020)