# Transformation JSON schema

## Example

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
  "breakpoints": [],
  "tsunami": []
}
```
## Field descriptions
| Field                 | Description                 |
| --------------------- | --------------------------- |
| `ioc_code`            | IOC station code            |
| `sensor`              | Sensor identifier           |
| `start`, `end`        | Valid data window           |
| `dropped_date_ranges` | Continuous ranges to remove |
| `dropped_timestamps`  | Individual timestamps       |
| `breakpoints`         | Sensor regime changes       |
| `tsunami`             | Eventual tsunami(s) date ranges|
| `skip`                | Ignore station              |
| `wip`                 | Work in progress            |
