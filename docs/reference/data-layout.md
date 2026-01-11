# Data layout

IOC data is archived by year:

```
./data/
├── 2020
├── 2021
├── 2022
├── 2023
├── 2024
└── 2025
```

This structure allows scalable extension to additional years.

## Naming convention

The JSON files adopts the following naming convention:

```php-template
./transformations/<ioc_code>_<sensor>.json
```

## Usage
Using the function `#!python download_year_station()` will put the **raw** data directly in the data tree.

for example this function:

```python
import ioc_cleanup as C
ioc_all = C.get_meta()
year = 2025
for station in ioc_all.ioc_code.tolist():
  C.download_year_station(station, year, data_folder="../data")
```

downloads all **IOC stations data** for 2025 as Parquet files into:

```
./data/
└── 2025
```
