from typing import List, Dict


class TransformationEngine:

    def __init__(self, sink, config):
        self.sink = sink
        self.config = config

    def execute(self, raw_data: List[Dict]) -> None:

        analysis = self.config["analysis"]

        if analysis == "top10":
            result = self.top_10(raw_data)

        elif analysis == "bottom10":
            result = self.bottom_10(raw_data)

        elif analysis == "growth_rate":
            result = self.growth_rate(raw_data)

        elif analysis == "average_by_continent":
            result = self.average_by_continent(raw_data)

        elif analysis == "global_trend":
            result = self.total_global_trend(raw_data)

        elif analysis == "fastest_continent":
            result = self.fastest_growing_continent(raw_data)

        elif analysis == "consistent_decline":
            result = self.consistent_decline(raw_data)

        elif analysis == "contribution":
            result = self.contribution_to_global(raw_data)

        else:
            result = [{"error": "Invalid analysis type"}]

        self.sink.write(result)

   def top_10_countries(self, data, continent, start_year, end_year):

    # Step 1: Filter by continent AND year range
    filtered = list(filter(
        lambda x: x["Continent"] == continent and
                  start_year <= int(x["Year"]) <= end_year,
        data
    ))

    # Step 2: Aggregate GDP by country
    country_totals = {}

    for record in filtered:
        country = record["Country Name"]
        value = float(record["Value"])

        country_totals[country] = country_totals.get(country, 0) + value

    # Step 3: Convert dictionary to list of dict
    result = [{"Country": k, "Total GDP": v}
              for k, v in country_totals.items()]

    # Step 4: Sort descending
    result = sorted(result, key=lambda x: x["Total GDP"], reverse=True)

    return result[:10]
    # 2 BOTTOM 10
    # -------------------------


def bottom_10_countries(self, data, continent, start_year, end_year):

    filtered = list(filter(
        lambda x: x["Continent"] == continent and
                  start_year <= int(x["Year"]) <= end_year,
        data
    ))

    country_totals = {}

    for record in filtered:
        country = record["Country Name"]
        value = float(record["Value"])

        country_totals[country] = country_totals.get(country, 0) + value

    result = [{"Country": k, "Total GDP": v}
              for k, v in country_totals.items()]

    result = sorted(result, key=lambda x: x["Total GDP"])

    return result[:10]

    # -------------------------
    # 3 GROWTH RATE
    # -------------------------
    def growth_rate(self, data):
        continent = self.config["continent"]
        start = str(self.config["start_year"])
        end = str(self.config["end_year"])

        result = []

        for row in data:
            if row["Continent"] == continent:
                if row.get(start) and row.get(end):
                    growth = ((row[end] - row[start]) / row[start]) * 100
                    result.append({
                        "Country": row["Country Name"],
                        "Growth Rate (%)": round(growth, 2)
                    })

        return result

    # -------------------------
    # 4 AVERAGE BY CONTINENT
    # -------------------------
    def average_by_continent(self, data):
        start = str(self.config["start_year"])
        end = str(self.config["end_year"])

        continent_totals = {}

        for row in data:
            continent = row["Continent"]

            if row.get(start) and row.get(end):
                avg = (row[start] + row[end]) / 2

                if continent not in continent_totals:
                    continent_totals[continent] = []

                continent_totals[continent].append(avg)

        result = []

        for cont, values in continent_totals.items():
            result.append({
                "Continent": cont,
                "Average GDP": round(sum(values) / len(values), 2)
            })

        return result

    # -------------------------
    # 5 GLOBAL TREND
    # -------------------------
    def total_global_trend(self, data):
        start = self.config["start_year"]
        end = self.config["end_year"]

        result = []

        for year in range(start, end + 1):
            year_str = str(year)
            total = sum(
                row.get(year_str, 0) or 0
                for row in data
            )

            result.append({
                "Year": year,
                "Total Global GDP": total
            })

        return result
    # 6 FASTEST CONTINENT
    # -------------------------
    def fastest_growing_continent(self, data):
        start = str(self.config["start_year"])
        end = str(self.config["end_year"])

        growth = {}

        for row in data:
            cont = row["Continent"]
            if row.get(start) and row.get(end):

                rate = ((row[end] - row[start]) / row[start]) * 100

                if cont not in growth:
                    growth[cont] = []

                growth[cont].append(rate)

        result = []

        for cont, rates in growth.items():
            avg_growth = sum(rates) / len(rates)
            result.append({
                "Continent": cont,
                "Average Growth (%)": round(avg_growth, 2)
            })

        result.sort(key=lambda x: x["Average Growth (%)"], reverse=True)

        return result

    # -------------------------
    # 7 CONSISTENT DECLINE
    # -------------------------
    def consistent_decline(self, data):
        x = self.config["x_years"]
        end = self.config["end_year"]

        result = []

        for row in data:
            years = [str(end - i) for i in range(x)]

            values = [row.get(y) for y in years if row.get(y)]

            if len(values) == x:
                if all(values[i] > values[i+1] for i in range(len(values)-1)):
                    result.append({
                        "Country": row["Country Name"]
                    })

        return result
   # 8 CONTRIBUTION
    # -------------------------
    def contribution_to_global(self, data):
        start = self.config["start_year"]
        end = self.config["end_year"]

        continent_totals = {}
        global_total = 0

        for row in data:
            for year in range(start, end + 1):
                val = row.get(str(year)) or 0
                global_total += val

                cont = row["Continent"]
                continent_totals[cont] = continent_totals.get(cont, 0) + val

        result = []

        for cont, total in continent_totals.items():
            percent = (total / global_total) * 100 if global_total else 0
            result.append({
                "Continent": cont,
                "Contribution (%)": round(percent, 2)
            })

        return result