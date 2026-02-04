
# Interactive Cleaning Dashboard

## Running the dashboard

```bash
python -mpanel serve dashboard/cleanup_dashboard.py
```
![dashboard](../assets/dashboard_light.png)

## Station dropdown list

Stations are discovered automatically from the JSONs in:
```
./transformations/<ioc_code>_<sensor>.json
```

## Error handling

If a JSON file contains a syntax error or invalid field, the dashboard will show:

![error](../assets/dashboard_error.png)

## Dark mode

You can activate dark mode by clicking on the top right switch

![error](../assets/dashboard_dark.png)
