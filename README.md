# IOC Cleanup

`ioc_cleanup` provides a reproducible, transparent, and traceable workflow for cleaning tide gauge (sea level) data from IOC (Intergovernmental Oceanographic Commission) stations worldwide.

![demo](./docs/assets/presentation.png)

## Motivation & Concept

Cleaning tide gauge data is often:
 * manual,
 * poorly documented,
 * hard to reproduce,
 * and difficult to review or share.

This project proposes a community-driven, version-controlled approach to data cleaning, where all cleaning decisions are explicitly recorded and can be audited or improved over time.

**What this approach enables**

 * Flagging timestamps or time ranges affected by:
   * bad or corrupt data
   * sensor breakpoints
   * singular phenomena (e.g. tsunamis, meteo-tsunamis, seiches, or unidentified events)
 * Fully reproducible cleaning
 * Transparent and traceable decisions stored in plain JSON
 * Peer review of cleaning decisions via GitHub
 * Easy extension to other datasets (e.g. GESLA, NDBC)
 * Gradual growth in station coverage through community contributions

## Repository Overview

This repository contains a set of Python routines to **clean IOC sea level data** using **declarative JSON transformations**.

### Core idea

The core asset of this repository is the set of **JSON files** located in `./transformations/`.

Each JSON file describes:

 * the valid time window
 * dropped timestamps
 * dropped time ranges
 * breakpoints
 * metadata and notes

Together, these JSON files define the transformation from **raw data to clean signal**.

## Caveats and limitations
Please be aware of the following:
 * ❌ This repository does NOT contain IOC data
   * Data download is not handled internally
   * Examples (in this `README` or in `tests`) use the [`searvey`](https://github.com/oceanmodeling/searvey) package
 * Step changes in data are currently only flagged via the `breakpoints` item in the JSOn
   * No offset correction is applied
 * Vertical datums are not addressed
 * Distinguishing noise (e.g. boat wakes) from real physical events can be difficult for noisy sensors
 * Cleaning decisions are inherently subjective
   * Different operators may disagree on what should be discarded


## Getting Started
### Prerequisites
 * Python 3.11 (recommended).
 * **~24GB** of free disk space for storing raw and processed data.

### Installation

```bash
git clone https://github.com/seareport/ioc_cleanup.git
pip install -r requirements.txt
```

## Usage
example with one station: `abed` (Aberdeen), sensor `bub`
```python
station = "abed"
sensor = "bub"
```

### Download Raw Data:

```python
import searvey
df_raw = searvey.fetch_ioc_station(station, "2020-01-01", "2026-01-01")
```

### Apply Cleaning Transformation:

```python
import ioc_cleanup as C

trans = C.load_transformation_from_path(
  "../transformations/maya_pwl.json"
)
df_clean = C.transform(df, trans)
```

Example for `maya` station:

![example](./assets/maya_example.png)

## Transformation Files (JSON)
All transformation logic lives in `./transformations/`.
### Example JSON:
```json
{
  "ioc_code": "abed",
  "sensor": "bub",
  "notes": "",
  "skip": false,
  "wip": false,
  "start": "2020-01-01T00:00:00",
  "end": "2026-01-01T00:00:00",
  "high": null,
  "low": null,
  "dropped_date_ranges": [
    ["2022-03-27 03:00:00", "2022-03-27 03:45:00"],
    ["2023-03-26 03:00:00", "2023-03-26 03:45:00"]
  ],
  "dropped_timestamps": [
    "2022-09-30T14:45:00",
    "2022-09-30T15:30:00",
    "2022-10-02T06:45:00",
    "2022-10-02T07:00:00",
    "2023-06-21T00:15:00",
    "2024-04-24T11:00:00",
    "2024-09-07 12:00:00"
  ],
  "breakpoints": []
}
```
#### Field descriptions

 * `ioc_code` : IOC station code
 * `sensor` : sensor identifier
 * `notes` : free-text comments
 * `skip` : skip this station entirely
 * `wip` : mark transformation as work-in-progress
 * `start`, `end` : valid data window
 * `high`, `low` : optional value thresholds
 * `dropped_date_ranges` : continuous time ranges to remove
 * `dropped_timestamps` : individual timestamps to remove
 * `breakpoints` : timestamps where sensor behavior changes

## Downloading IOC Data in Bulk
Shortcut functions are provided to download, load, and clean data.

### Example: download all IOC stations for 2025


```python
import ioc_cleanup as C
ioc_all = C.get_meta()
year = 2025
for station in ioc_all.ioc_code.tolist():
  C.download_year_station(station, year, data_folder="../data")
```
This downloads station data as Parquet files into:
```bash
./data/2025
```
### Important: the architecture used for archiving the files is as follows:
```
./data/
├── 2020
├── 2021
├── 2022
├── 2023
├── 2024
└── 2025
```
to be able to scale up the number of years for the cleaning in the future

## Interactive Cleaning Dashboard

### Run the dashboard

```bash
python -mpanel serve dashboard/cleanup_dashboard.py
```

you will directed to this to:

![dashboard](./assets/dashboard_light.png)

#### How stations are discovered

 * The station list is defined by files in `./transformations/`
 * To add a station, create a file following this convention:

```php-template
./transformations/<ioc_code>_<sensor>.json
```

### Error handling

If a JSON file contains a syntax error or invalid field, the dashboard will show:

![error](./assets/dashboard_error.png)

### Dark mode

You can activate dark mode by clicking on the top right switch

![error](./assets/dashboard_dark.png)

## Contributing

Contributions are very welcome!

### How to contribute

 1. Fork the repository
 2. Add or update a JSON transformation file
 3. Use the dashboard to clean or flag data
 4. Submit a pull request with a clear description of your changes

### Areas for improvement

 * Add more IOC stations
 * Extend the cleaned time range (currently 2020–2025)
