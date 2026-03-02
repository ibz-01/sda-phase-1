from typing import List, Dict


class TransformationEngine:

    def __init__(self, sink, config):
        self.sink = sink
        self.config = config

    # ===============================
    # MAIN EXECUTION
    # ===============================
    def execute(self, data):

        continent = self.config["continent"]
        start_year = self.config["start_year"]
        end_year = self.config["end_year"]

        results = {}

        results["Top 10 Countries"] = self.top_10_countries(
            data, continent, start_year, end_year
        )

        results["Bottom 10 Countries"] = self.bottom_10_countries(
            data, continent, start_year, end_year
        )

        results["GDP Growth Rate"] = self.gdp_growth_rate(
            data, continent, start_year, end_year
        )

        results["Average GDP by Continent"] = self.avg_gdp_by_continent(
            data, start_year, end_year
        )

        results["Global GDP Trend"] = self.global_gdp_trend(
            data, start_year, end_year
        )

        results["Fastest Growing Continent"] = self.fastest_growing_continent(
            data, start_year, end_year
        )

        results["Consistent Decline"] = self.consistent_decline(
            data, continent
        )

        results["Contribution to Global GDP"] = self.continent_contribution(
            data, start_year, end_year
        )

        self.sink.write(results)

    # ===============================
    # 1 TOP 10
    # ===============================
    def top_10_countries(self, data, continent, start_year, end_year):

        country_totals = {}

        for row in data:
            if row["Continent"] != continent:
                continue

            total = 0
            for year in range(start_year, end_year + 1):
                value = row.get(str(year))
                if value:
                    total += float(value)

            country_totals[row["Country Name"]] = total

        result = [{"Country": k, "Total GDP": v}
                  for k, v in country_totals.items()]

        result.sort(key=lambda x: x["Total GDP"], reverse=True)

        return result[:10]

    # ===============================
    # 2 BOTTOM 10
    # ===============================
    def bottom_10_countries(self, data, continent, start_year, end_year):

        country_totals = {}

        for row in data:
            if row["Continent"] != continent:
                continue

            total = 0
            for year in range(start_year, end_year + 1):
                value = row.get(str(year))
                if value:
                    total += float(value)

            country_totals[row["Country Name"]] = total

        result = [{"Country": k, "Total GDP": v}
                  for k, v in country_totals.items()]

        result.sort(key=lambda x: x["Total GDP"])

        return result[:10]

    # ===============================
    # 3 GDP GROWTH RATE
    # ===============================
    def gdp_growth_rate(self, data, continent, start_year, end_year):

        result = []

        for row in data:
            if row["Continent"] != continent:
                continue

            start_val = row.get(str(start_year))
            end_val = row.get(str(end_year))

            if start_val and end_val and float(start_val) != 0:
                growth = ((float(end_val) - float(start_val)) /
                          float(start_val)) * 100

                result.append({
                    "Country": row["Country Name"],
                    "Growth Rate (%)": round(growth, 2)
                })

        return result

    # ===============================
    # 4 AVERAGE GDP BY CONTINENT
    # ===============================
    def avg_gdp_by_continent(self, data, start_year, end_year):

        continent_totals = {}

        for row in data:
            continent = row["Continent"]

            total = 0
            count = 0

            for year in range(start_year, end_year + 1):
                value = row.get(str(year))
                if value:
                    total += float(value)
                    count += 1

            if count > 0:
                avg = total / count

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

    # ===============================
    # 5 GLOBAL GDP TREND
    # ===============================
    def global_gdp_trend(self, data, start_year, end_year):

        result = []

        for year in range(start_year, end_year + 1):
            total = 0

            for row in data:
                value = row.get(str(year))
                if value:
                    total += float(value)

            result.append({
                "Year": year,
                "Total Global GDP": total
            })

        return result

    # ===============================
    # 6 FASTEST GROWING CONTINENT
    # ===============================
    def fastest_growing_continent(self, data, start_year, end_year):

        continent_growth = {}

        for row in data:
            start_val = row.get(str(start_year))
            end_val = row.get(str(end_year))

            if start_val and end_val and float(start_val) != 0:

                growth = ((float(end_val) - float(start_val)) /
                          float(start_val)) * 100

                cont = row["Continent"]

                if cont not in continent_growth:
                    continent_growth[cont] = []

                continent_growth[cont].append(growth)

        result = []

        for cont, values in continent_growth.items():
            avg_growth = sum(values) / len(values)

            result.append({
                "Continent": cont,
                "Average Growth (%)": round(avg_growth, 2)
            })

        result.sort(key=lambda x: x["Average Growth (%)"], reverse=True)

        return result

    # ===============================
    # 7 CONSISTENT DECLINE
    # ===============================
    def consistent_decline(self, data, continent):

        x = self.config["x_years"]
        end_year = self.config["end_year"]

        result = []

        for row in data:
            if row["Continent"] != continent:
                continue

            values = []

            for i in range(x):
                year = str(end_year - i)
                val = row.get(year)
                if val:
                    values.append(float(val))

            if len(values) == x:
                if all(values[i] > values[i + 1]
                       for i in range(len(values) - 1)):

                    result.append({
                        "Country": row["Country Name"]
                    })

        return result

    # ===============================
    # 8 CONTRIBUTION TO GLOBAL GDP
    # ===============================
    def continent_contribution(self, data, start_year, end_year):

        continent_totals = {}
        global_total = 0

        for row in data:
            cont = row["Continent"]

            for year in range(start_year, end_year + 1):
                value = row.get(str(year))
                if value:
                    val = float(value)
                    global_total += val
                    continent_totals[cont] = continent_totals.get(cont, 0) + val

        result = []

        for cont, total in continent_totals.items():
            percent = (total / global_total) * 100 if global_total else 0

            result.append({
                "Continent": cont,
                "Contribution (%)": round(percent, 2)
            })

        return result