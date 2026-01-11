# IOC Cleanup

`ioc_cleanup` provides a reproducible, transparent, and traceable workflow
for cleaning tide gauge data from [IOC](https://www.ioc-sealevelmonitoring.org/list.php) (Intergovernmental Oceanographic Commission) stations worldwide.

## Getting Started

### Prerequisites

- Python 3.11+ (recommended)
- ~24 GB free disk space for raw IOC 2020-2025 data

### Installation

```bash
git clone https://github.com/seareport/ioc_cleanup.git
pip install -r requirements.txt
```

### Minimal example
```python
import searvey
import ioc_cleanup as C

station = "abed"
df_raw = searvey.fetch_ioc_station(station, "2020-01-01", "2026-01-01")

trans = C.load_transformation_from_path(
    "../transformations/abed_bub.json"
)

df_clean = C.transform(df_raw, trans)
```


Example for `maya` station:

![example](./assets/maya_example.png)
