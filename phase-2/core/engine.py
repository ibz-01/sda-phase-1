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