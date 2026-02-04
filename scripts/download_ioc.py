from __future__ import annotations

import ioc_cleanup as C

YEARS = [2020, 2021, 2022, 2023, 2024, 2025]
station = "nuku"

for year in YEARS[::-1]:
    C.download_year_station(station, year, data_folder="./data")
