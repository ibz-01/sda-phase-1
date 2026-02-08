import matplotlib.pyplot as plt  # importing matplotlib for plotting


def plot_region_gdp(data, continent, year):
    """
    This function creates a BAR CHART showing GDP values
    of all countries in a given continent for a specific year.
    """

    #extract name of the countries from the data
    # Using map() to go through each dictionary in the data list
    # and pick the value stored under the key country name
    countries = list(
        map(
            lambda x: x["Country Name"],
            data
        )
    )

    # extracting gdp values from data
    # similar approach as above but now for extraction
    # the gdp value stored under the key value
    values = list(
        map(
            lambda x: x["Value"],
            data
        )
    )

    # creating figure for plotting
    plt.figure()

    # drawing a bar chart
    # country name - x axis
    # gdp values - y axis
    plt.bar(countries, values)

    # rotating x axis labels so country names
    # so they remain readable
    plt.xticks(rotation=90)

    # setting title of the graph
    plt.title(f"GDP of {continent} in {year}")

    # x - axis label
    plt.xlabel("Country")

    # y - axis label
    plt.ylabel("GDP")

    # adjusting layout to prevent labels cuttoff
    plt.tight_layout()

    # displaying bar chart
    plt.show()



    
def plot_year_distribution(data, year):
    """
    This function creates a HISTOGRAM showing the distribution
    of GDP values for a specific year.
    """

    # extracing gdp values from data
    # looping through each dictionary in data
    # and collect the gdp value
    values = list(
        map(
            lambda x: x["Value"],
            data
        )
    )

    # creating a new figure
    plt.figure()

    # plot a histogram of gdp values
    # bins=10 divides the data into 10 ranges
    plt.hist(values, bins=10)

    # title of the histogram
    plt.title(f"GDP Distribution in {year}")

    # gdp values - x axis
    plt.xlabel("GDP")

    # frequency - y axis
    plt.ylabel("Frequency")

    # display histogram
    plt.show()


