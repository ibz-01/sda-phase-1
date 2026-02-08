import json
from data_loader import loadFileData
from data_processor import filter_data, compute_statistic
from validation import validate
# importing required  functions from the dashboard_visuals for visualisation
from dashboard_visuals import plot_region_gdp, plot_year_distribution, plot_region_gdp_pie, plot_year_scatter


try:
    with open("config.json", "r") as file:
        config = json.load(file)
except FileNotFoundError:
    config = {}

if "continent" not in config or not config["continent"]:
    config["continent"] = input("Enter Continent: ")

if "year" not in config or config["year"] is None:
    while True:
        try:
            config["year"] = int(input("Enter Year: "))
            break
        except ValueError:
            print("Year must be an integer, try again.")

if "country" not in config or config["country"] in [None, ""]:
    config["country"] = input("Enter Country (optional, press Enter to skip): ") or None

if "operation" not in config or not config["operation"]:
    while True:
        op = input("Enter Operation (average/sum): ").lower()
        if op in ["average", "sum"]:
            config["operation"] = op
            break
        else:
            print("Invalid operation, try again.")

validate(config) #config validated (inputs)

df_formatted = loadFileData("gdp_with_continent_filled.xlsx - GDP.csv") # file loaded

#filtering

filtered_data = filter_data(
    df_formatted,
    continent=config["continent"],
    year=config["year"],
    country=config.get("country")
)

#compute stats
result = compute_statistic(filtered_data, config["operation"])


print("\n===== GDP ANALYTICS DASHBOARD =====")
print(f"Continent: {config['continent']}")
print(f"Year: {config['year']}")
print(f"Country: {config.get('country')}")
print(f"Operation: {config['operation']}")
print("----------------------------------")

if result is None:
    print("No data found for the given configuration.")
else:
    print("Computed Result:", result)




# check if filtered_data is empty
# prevent plotting empty data set
if filtered_data:
    
    # plot gdp values of all countries of that continent
    # the continent name is taken from dictionary
    # The year shows which years gdp is being shown
    plot_region_gdp(
        filtered_data,           # filtered data set after conditions applied
        config["continent"],      # selected continent
        config["year"]            # selected year for gdp compare
    )

    # pie chart
    # shows GDP as percentage/proportion of total
    plot_region_gdp_pie(
       filtered_data,           # same filtered data
        config["continent"],     # same continent
        config["year"]           # same year
    )

    
    # plot the gdp distribution for the selected year
    # focus on the year specified in the config
    plot_year_distribution(
        filtered_data,            # same filtered data
        config["year"]            # year for which distribution is plotted
    )

    #scatter plot
    #each country a point
    plot_year_scatter(
    filtered_data,           # same filtered data        
    config["year"]           # same year
    )