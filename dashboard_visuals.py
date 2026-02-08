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

