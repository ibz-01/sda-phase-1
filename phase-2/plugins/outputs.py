import json
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


class GraphicsChartWriter:

    def __init__(self, output_dir: str = "charts"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def write(self, records: dict) -> None:
        print(f"\n[GraphicsChartWriter] Saving charts to '{self.output_dir}/'...\n")

        handlers = {
            "Top 10 Countries":             self._chart_top_bottom,
            "Bottom 10 Countries":          self._chart_top_bottom,
            "GDP Growth Rate":              self._chart_growth_rate,
            "Average GDP by Continent":     self._chart_avg_gdp_continent,
            "Global GDP Trend":             self._chart_global_trend,
            "Fastest Growing Continent":    self._chart_fastest_growing,
            "Consistent Decline":           self._chart_consistent_decline,
            "Contribution to Global GDP":   self._chart_contribution_pie,
        }

        for title, data in records.items():
            handler = handlers.get(title)
            if handler:
                try:
                    handler(title, data)
                    print(f"  ✔ {title}")
                except Exception as e:
                    print(f"  ✘ {title} — Error: {e}")

        print(f"\n[GraphicsChartWriter] Done.\n")

    # ---- helpers ----

    def _safe_filename(self, title: str) -> str:
        return os.path.join(self.output_dir, title.replace(" ", "_").lower() + ".png")

    def _save(self, title: str):
        plt.tight_layout()
        plt.savefig(self._safe_filename(title), dpi=150)
        plt.show()
        plt.close()

    # ---- chart methods ----

    def _chart_top_bottom(self, title: str, data: list):
        if not data:
            return

        countries = [d["Country"] for d in data]
        gdps = [d["Total GDP"] / 1e12 for d in data]   # trillions

        colors = ["#2ecc71" if "Top" in title else "#e74c3c"] * len(countries)

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(countries[::-1], gdps[::-1], color=colors)
        ax.set_xlabel("Total GDP (Trillions USD)")
        ax.set_title(title)
        ax.bar_label(bars, fmt="%.2f T", padding=4, fontsize=8)
        self._save(title)

    def _chart_growth_rate(self, title: str, data: list):
        if not data:
            return

        data_sorted = sorted(data, key=lambda x: x["Growth Rate (%)"], reverse=True)
        countries = [d["Country"] for d in data_sorted]
        rates = [d["Growth Rate (%)"] for d in data_sorted]
        colors = ["#27ae60" if r >= 0 else "#c0392b" for r in rates]

        fig, ax = plt.subplots(figsize=(max(12, len(countries) * 0.4), 6))
        ax.bar(countries, rates, color=colors)
        ax.axhline(0, color="black", linewidth=0.8)
        ax.set_ylabel("Growth Rate (%)")
        ax.set_title(title)
        plt.xticks(rotation=90, fontsize=7)

        pos_patch = mpatches.Patch(color="#27ae60", label="Positive Growth")
        neg_patch = mpatches.Patch(color="#c0392b", label="Negative Growth")
        ax.legend(handles=[pos_patch, neg_patch])

        self._save(title)

    def _chart_avg_gdp_continent(self, title: str, data: list):
        if not data:
            return

        data_sorted = sorted(data, key=lambda x: x["Average GDP"], reverse=True)
        continents = [d["Continent"] for d in data_sorted]
        gdps = [d["Average GDP"] / 1e9 for d in data_sorted]   # billions

        palette = ["#3498db", "#e67e22", "#2ecc71", "#9b59b6", "#e74c3c", "#1abc9c", "#f39c12"]
        colors = [palette[i % len(palette)] for i in range(len(continents))]

        fig, ax = plt.subplots(figsize=(9, 5))
        bars = ax.bar(continents, gdps, color=colors)
        ax.set_ylabel("Average GDP (Billions USD)")
        ax.set_title(title)
        ax.bar_label(bars, fmt="%.1f B", padding=3, fontsize=8)
        self._save(title)

    def _chart_global_trend(self, title: str, data: list):
        if not data:
            return

        years = [d["Year"] for d in data]
        totals = [d["Total Global GDP"] / 1e12 for d in data]

        fig, ax = plt.subplots(figsize=(9, 5))
        ax.plot(years, totals, marker="o", color="#2980b9", linewidth=2.5)
        ax.fill_between(years, totals, alpha=0.15, color="#2980b9")
        ax.set_xlabel("Year")
        ax.set_ylabel("Total Global GDP (Trillions USD)")
        ax.set_title(title)
        ax.set_xticks(years)

        for x, y in zip(years, totals):
            ax.annotate(f"{y:.1f}T", (x, y), textcoords="offset points",
                        xytext=(0, 8), ha="center", fontsize=8)

        self._save(title)

    def _chart_fastest_growing(self, title: str, data: list):
        if not data:
            return

        continents = [d["Continent"] for d in data]
        growth = [d["Average Growth (%)"] for d in data]
        colors = ["#27ae60" if g >= 0 else "#c0392b" for g in growth]

        fig, ax = plt.subplots(figsize=(9, 5))
        bars = ax.bar(continents, growth, color=colors)
        ax.axhline(0, color="black", linewidth=0.8)
        ax.set_ylabel("Average Growth (%)")
        ax.set_title(title)
        ax.bar_label(bars, fmt="%.2f%%", padding=3, fontsize=9)
        self._save(title)

    def _chart_consistent_decline(self, title: str, data: list):
        if not data:
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.text(0.5, 0.5, "No countries with consistent decline found",
                    ha="center", va="center", transform=ax.transAxes, fontsize=12)
            ax.set_title(title)
            ax.axis("off")
            self._save(title)
            return

        countries = [d["Country"] for d in data]
        y_pos = list(range(len(countries)))

        fig, ax = plt.subplots(figsize=(8, max(4, len(countries) * 0.4)))
        ax.barh(y_pos, [1] * len(countries), color="#e74c3c", alpha=0.7)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(countries, fontsize=9)
        ax.set_xticks([])
        ax.set_title(title)
        ax.set_xlabel("(Countries flagged for consistent GDP decline)")
        self._save(title)

    def _chart_contribution_pie(self, title: str, data: list):
        if not data:
            return

        labels = [d["Continent"] for d in data]
        sizes = [d["Contribution (%)"] for d in data]

        palette = ["#3498db", "#e67e22", "#2ecc71", "#9b59b6",
                   "#e74c3c", "#1abc9c", "#f39c12"]
        colors = [palette[i % len(palette)] for i in range(len(labels))]

        fig, ax = plt.subplots(figsize=(8, 8))
        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, autopct="%1.1f%%",
            colors=colors, startangle=140,
            pctdistance=0.82, wedgeprops=dict(edgecolor="white", linewidth=1.5)
        )
        for at in autotexts:
            at.set_fontsize(9)

        ax.set_title(title, fontsize=14, pad=20)
        self._save(title)






class ConsoleWriter:

    def write(self, records):

        print("\n================ GDP ANALYSIS DASHBOARD ================\n")

        for title, data in records.items():

            print(f"\n----- {title} -----\n")

            if isinstance(data, list):
                for row in data:
                    print(row)

            else:
                print(data)

        print("\n================ END OF REPORT =========================\n")