from __future__ import annotations

import functools
import logging
import os
import typing as T
from pathlib import Path

import geopandas as gpd
import pandas as pd
import searvey

logger = logging.getLogger(__name__)


@functools.cache
def get_meta() -> gpd.GeoDataFrame:
    meta_web = searvey.get_ioc_stations()
    meta_api = (
        pd.read_json("http://www.ioc-sealevelmonitoring.org/service.php?query=stationlist&showall=all")
        .drop_duplicates()
        .rename(columns={"Code": "ioc_code"})
    )

    merged = pd.merge(
        meta_web.drop(columns=["lon", "lat", "geometry"]),
        meta_api[["ioc_code", "Lon", "Lat"]].rename(columns={"Lon": "lon", "Lat": "lat"}).drop_duplicates(),
        on=["ioc_code"],
    )
    merged = T.cast(
        gpd.GeoDataFrame,
        merged.assign(geometry=gpd.points_from_xy(merged.lon, merged.lat, crs="EPSG:4326")),
    )
    return merged


def download_raw(ioc_codes: list[str], start: pd.Timestamp, end: pd.Timestamp) -> dict[str, pd.DataFrame]:
    no_codes = len(ioc_codes)
    start_dates = pd.DatetimeIndex([start] * no_codes)
    end_dates = pd.DatetimeIndex([end] * no_codes)
    dataframes: dict[str, pd.DataFrame] = searvey._ioc_api._fetch_ioc(
        station_ids=ioc_codes,
        start_dates=start_dates,
        end_dates=end_dates,
        http_client=None,
        rate_limit=None,
        multiprocessing_executor=None,
        multithreading_executor=None,
        progress_bar=False,
    )
    return dataframes


def download_year_station(
    station: str,
    year: int,
    data_folder: str = "./data",
) -> None:
    data_folder = os.path.abspath(data_folder)
    year_folder = os.path.join(data_folder, str(year))
    os.makedirs(year_folder, exist_ok=True)
    try:
        start = pd.Timestamp(f"{year}-01-01")
        end = pd.Timestamp(f"{year}-12-31T23:59:59")
        dict_df = download_raw([station], start, end)
        df = dict_df[station]
        if not df.empty:
            df.to_parquet(f"{year_folder}/{station}.parquet")
            logger.info(f"  Saved {station} for {year}")
    except Exception as e:
        logger.error(f"Error for {station} in {year}: {e}")


def load_station(
    station: str,
    data_dir: Path = Path("./data"),
    start_year: int = 2011,
    end_year: int = 2024,
) -> pd.DataFrame:
    dfs = []
    for year in range(start_year, end_year):
        path = data_dir / str(year) / f"{station}.parquet"
        if not os.path.exists(path):
            continue
        df = pd.read_parquet(path)
        if df.empty:
            continue
        dfs.append(df)

    if dfs:
        return pd.concat(dfs)
    else:
        logger.error(f"No data found for station {station}")
        return pd.DataFrame()
