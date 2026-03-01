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

    # -------------------------
    # 1 TOP 10
    # -------------------------
    def top_10(self, data):
        continent = self.config["continent"]
        year = str(self.config["year"])

        filtered = list(
            filter(lambda r: r["Continent"] == continent and r.get(year), data)
        )

        sorted_data = sorted(filtered, key=lambda r: r[year], reverse=True)

        return sorted_data[:10]
    # 2 BOTTOM 10
    # -------------------------
    def bottom_10(self, data):
        continent = self.config["continent"]
        year = str(self.config["year"])

        filtered = list(
            filter(lambda r: r["Continent"] == continent and r.get(year), data)
        )

        sorted_data = sorted(filtered, key=lambda r: r[year])

        return sorted_data[:10]

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