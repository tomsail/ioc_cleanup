from __future__ import annotations

import pathlib
from importlib.metadata import version

import pandas as pd

DATA_DIR = pathlib.Path("data")
SPLIT_DIR = pathlib.Path("split")
TRANSFORMATIONS_DIR = pathlib.Path("transformations")

START = pd.Timestamp("2020-01-01T00:00:00")
END = pd.Timestamp("2026-01-01T00:00:00")

PACKAGE = {
    "source_data": "IOC sea-level data downloaded from https://www.ioc-sealevelmonitoring.org/",
    "cleaning_method": "https://github.com/oceanmodeling/ioc_cleanup",
    "cleaning_method_version": version("ioc_cleanup"),
}
