from __future__ import annotations

import glob
from pathlib import Path

import hvplot.pandas  # noqa: F401
import numpy as np
import pandas as pd
import panel as pn

import ioc_cleanup as C

IOC = C.get_meta()
MAX = 2
YEAR = 2020


def extract_waves(time, eta, crossing="up"):
    """
    Extract wave properties using zero-crossing method.

    Parameters
    ----------
    time : pd.Series or np.ndarray
        Time vector
    eta : pd.Series or np.ndarray
        Surface elevation
    crossing : str
        'up' or 'down'

    Returns
    -------
    pd.DataFrame
        Columns: ['wave', 'H', 'T', 't_crest', 't_trough']
    """

    eta = np.asarray(eta)
    time = np.asarray(time)

    fluc = eta - eta.mean()
    sgn = np.sign(fluc)

    # Zero-crossing indices
    if crossing == "up":
        zc = np.where((sgn[:-1] < 0) & (sgn[1:] > 0))[0]
    else:  # down-crossing
        zc = np.where((sgn[:-1] > 0) & (sgn[1:] < 0))[0]

    waves = []

    for i in range(len(zc) - 1):
        i0 = zc[i] + 1
        i1 = zc[i + 1]

        if i1 - i0 < MAX:
            continue

        segment = fluc[i0:i1]
        seg_time = time[i0:i1]

        crest_idx = np.argmax(segment)
        trough_idx = np.argmin(segment)

        a_crest = segment[crest_idx]
        a_trough = segment[trough_idx]

        waves.append(
            {
                "wave": i + 1,
                "H": a_crest + abs(a_trough),
                "T": time[i1] - time[i0],
                "t_crest": seg_time[crest_idx],
                "t_trough": seg_time[trough_idx],
            },
        )

    return pd.DataFrame(waves)


# cleaned stations
clean_stations_list = []
not_yet_clean_stations_list = []

# kamchaptka tsunami
start = pd.Timestamp("2025-07-01")
end = pd.Timestamp("2025-10-01")
folder = Path("./data")
recorded_tsunamis = {}
for station in IOC.ioc_code.tolist():
    candidates = sorted(glob.glob(f"./transformations/{station}*.json"))
    if len(candidates) == 0:
        pass
    else:
        for path in candidates:
            t = C.load_transformation_from_path(path)
            # cleaned station test
            if not t.skip:
                clean_stations_list.append(station)
                if t.start.year > YEAR:
                    not_yet_clean_stations_list.append(station)

            # tsunami test
            for ts in t.tsunami:
                if ts[0] > start and ts[1] < end:
                    surge = C.load_surge_ts_for_year(t.ioc_code, t.sensor, 2025, folder, demean=True)
                    s_ = surge.loc[ts[0] : ts[1]] - surge.loc[ts[0] : ts[1]].mean()
                    tsunami_waves = extract_waves(s_.index, s_).sort_values(by="H", ascending=False, ignore_index=True)
                    recorded_tsunamis[station] = {
                        "wave number": tsunami_waves.loc[0, "wave"],
                        "tsunami wave height": tsunami_waves.loc[0, "H"],
                        "tsunami wave period": tsunami_waves.loc[0, "T"],
                    }

# Kamchatka tsunami
kamchatka = pd.DataFrame(recorded_tsunamis).T.join(
    IOC.set_index("ioc_code")[["lon", "lat"]],
    how="left",
)
kamchatka["tsunami wave height"] = kamchatka["tsunami wave height"].astype(float)
kamchatka.head()
map_ = kamchatka.hvplot.points(
    geo=True,
    x="lon",
    y="lat",
    tiles=True,
    c="tsunami wave height",
    s=100,
    clim=(0, 2),
    line_color="k",
    cmap="rainbow4",
    title="tsunami wave heights recorded for Kamchatka tsunami",
    hover_cols="index",
)
pane_ = pn.Row(
    pn.pane.HoloViews(
        map_.opts(responsive=True),
        sizing_mode="stretch_width",
        height=700,
    ),
    width_policy="max",
)
pane_.save("docs/tsunami_map.html")


# All IOC stations export
all_ioc_map = IOC.hvplot.points(
    geo=True,
    x="lon",
    y="lat",
    c="k",
    s=2,
    label="All IOC stations",
    hover_cols="ioc_code",
)
clean_ioc_map = IOC[IOC.ioc_code.isin(clean_stations_list)].hvplot.points(
    geo=True,
    x="lon",
    y="lat",
    c="g",
    s=50,
    tiles=True,
    title="Cleaned IOC stations",
    label="Cleaned IOC stations",
    hover_cols="ioc_code",
    legend="bottom_right",
)
not_yet_clean_ioc_map = IOC[IOC.ioc_code.isin(not_yet_clean_stations_list)].hvplot.points(
    geo=True,
    x="lon",
    y="lat",
    c="orange",
    s=50,
    tiles=True,
    label="Remaining raw IOC stations",
    hover_cols="ioc_code",
    legend="bottom_right",
)
map_ = clean_ioc_map * not_yet_clean_ioc_map * all_ioc_map
pane_ = pn.Row(
    pn.pane.HoloViews(
        map_.opts(responsive=True),
        sizing_mode="stretch_width",
        height=700,
    ),
    width_policy="max",
)
pane_.save("docs_/cleaned_map.html")
