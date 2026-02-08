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
    plt.figure(figsize=(14, 6))

    # drawing a bar chart
    # country name - x axis
    # gdp values - y axis
    plt.bar(countries, values, color='steelblue')

    # rotating x axis labels so country names
    # so they remain readable
    plt.xticks(rotation=90, ha='right')

    # setting title of the graph
    plt.title(f"GDP of {continent} in {year}", fontsize=16, fontweight='bold')

    # x - axis label
    plt.xlabel("Country", fontsize=12)

    # y - axis label
    plt.ylabel("GDP (in US Dollars)", fontsize=12)

    plt.grid(axis='y', alpha=0.3)

    # adjusting layout to prevent labels cuttoff
    plt.tight_layout()

    # displaying bar chart
    plt.show()

def plot_region_gdp_pie(data, continent, year):
    #this function creates a pie chart showing gdp distribution as percentages for countries in a continent
    # extracting country names from data
    countries = list(
        map(
            lambda x: x["Country Name"],
            data
        )
    )
   
    # extract gdp values from data
    values = list(
        map(
            lambda x: x["Value"],
            data
        )
    )

    # if there are more than 10 countries, we'll show only the top 10
    # and group the rest as "Others"
    if len(countries) > 10:
        # create a list of tuples: (country, value)
        country_value_pairs = list(zip(countries, values))
       
        # sort by gdp value in descending order 
        # using lambda to tell sort which element to use (x[1] is the value)
        sorted_pairs = sorted(
            country_value_pairs,
            key=lambda x: x[1],  # sort by gdp value
            reverse=True  # largest first
        )
       
        # take only the top 10
        top_10 = sorted_pairs[:10]
       
        # calculate the sum of all remaining countries
        remaining = sorted_pairs[10:]  # all countries after top 10
        others_sum = sum(map(lambda x: x[1], remaining))  # sum their GDPs
       
        # extract countries and values from top 10
        countries = list(map(lambda x: x[0], top_10))  # x[0] is country name
        values = list(map(lambda x: x[1], top_10))  # x[1] is GDP value
       
        # add "others" category if there were remaining countries
        if others_sum > 0:
            countries.append("Others")
            values.append(others_sum)
   
    # create a larger figure for the pie chart
    plt.figure(figsize=(10, 8))
   

    # autopct='%1.1f%%' shows percentage with 1 decimal place
    # startangle=90 rotates the chart to start from top
    plt.pie(
        values,  # the gdp values determine slice sizes
        labels=countries,  # country names for each slice
        autopct='%1.1f%%',  # format: shows "25.5%" for example
        startangle=90,  # start from top (90 degrees)
        textprops={'fontsize': 9}  # make text slightly smaller to fit
    )
   
    # set title
    plt.title(
        f"GDP Distribution in {continent} ({year})",
        fontsize=14,
        fontweight='bold'
    )
   
    # adjust layout
    plt.tight_layout()
   
    # display the pie chart
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
    plt.figure(figsize=(10, 6))

    # plot a histogram of gdp values
    # bins=10 divides the data into 10 ranges
    # edgecolor='black' adds black borders around bars
    plt.hist(
        values,
        bins=10,
        color='skyblue',
        edgecolor='black'
    )

    # title of the histogram
    plt.title(f"GDP Distribution in {year}", fontsize=16, fontweight='bold')

    # gdp values - x axis
    plt.xlabel("GDP (in US Dollars)", fontsize=12)

    # frequency - y axis
    plt.ylabel("Frequency (Number of Countries)", fontsize=12)

    # add a grid for easier reading
    plt.grid(axis='y', alpha=0.3)
   
    # adjust layout
    plt.tight_layout()

    # display histogram
    plt.show()


def plot_year_scatter(data, year):
    #this function creates a scatter plot showing gdp values
    #for each country in a specific year.
    # extract country names
    countries = list(
        map(
            lambda x: x["Country Name"],
            data
        )
    )
   
    # extract GDP values
    values = list(
        map(
            lambda x: x["Value"],
            data
        )
    )
    # we use range(len(countries)) to create positions for each country
    # for example: if there are 5 countries, this creates [0, 1, 2, 3, 4]
    x_positions = list(range(len(countries)))
   
    # create a wider figure
    plt.figure(figsize=(14, 6)) 

    # x_positions: where each point goes horizontally (0, 1, 2, ...)
    # values: where each point goes vertically (the GDP)
    # s=100: size of each point (bigger number = bigger dots)
    # alpha=0.6: transparency (0.6 means 60% opaque, slightly see-through)
    # color='coral': orange-red color for the points
    plt.scatter(
        x_positions,
        values,
        s=100,  # size of dots
        alpha=0.6,  # transparency
        color='coral',  # color of dots
        edgecolors='black',  # black border around each dot
        linewidth=0.5  # thickness of border
    )
   
    # set x-axis ticks to show country names instead of numbers
    # we replace positions [0, 1, 2, ...] with actual country names
    plt.xticks(
        x_positions,  # where to put labels (0, 1, 2, ...)
        countries,  # what labels to show (country names)
        rotation=90,  # rotate 90 degrees
        ha='right'  # align to the right
    )
   
    # set title
    plt.title(
        f"GDP Scatter Plot for {year}",
        fontsize=16,
        fontweight='bold'
    )
   
    # set x-axis label
    plt.xlabel("Country", fontsize=12)
   
    # set y-axis label
    plt.ylabel("GDP (in US Dollars)", fontsize=12)
   
    # add a horizontal grid to help read GDP values
    plt.grid(axis='y', alpha=0.3)
   
    # ajust layout
    plt.tight_layout()
   
    # display scatter plot
    plt.show()
