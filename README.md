# sda-phase-1

[config.json] ──────────────────────────┐
                                        │
[User Input] ───────────────────────────┤
                                        ▼
                              ┌─────────────────┐
                              │  dashboard.py   │  (Orchestrator)
                              └─────────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    ▼                   ▼                   ▼
            ┌──────────────┐    ┌──────────────┐   ┌──────────────┐
            │ validation.py│    │data_loader.py│   │              │
            │              │    │              │   │              │
            │ validate()   │    │loadFileData()│   │              │
            └──────────────┘    └──────────────┘   │              │
                    │                   │           │              │
                    └───────┬───────────┘           │              │
                            ▼                       ▼              ▼
                    ┌─────────────────┐    ┌──────────────────────────┐
                    │data_processor.py│    │   dashboard_visuals.py   │
                    │                 │    │                          │
                    │ filter_data()   │    │ plot_region_gdp()        │
                    │ compute_stat()  │    │ plot_region_gdp_pie()    │
                    └─────────────────┘    │ plot_year_distribution() │
                            │              │ plot_year_scatter()      │
                            │              └──────────────────────────┘
                            ▼                       ▼
                    [Statistical Results]    [4 Visualizations]
                            │                       │
                            └───────┬───────────────┘
                                    ▼
                            [User Sees Results]


1 - data is loaded from file
2 - dataset is cleaned
3 - data is filtered by region, year, country
4 - queries are computed
5 - displayed