# importing required  functions from the dashboard_visuals for visualisation
from dashboard_visuals import plot_region_gdp, plot_year_distribution

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
    
    # plot the gdp distribution for the selected year
    # focus on the year specified in the config
    plot_year_distribution(
        filtered_data,            # same filtered data
        config["year"]            # year for which distribution is plotted
    )
