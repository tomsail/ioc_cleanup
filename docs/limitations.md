# Caveats and limitations
Please be aware of the following:

## No dataset
This repository does **NOT** contain IOC data

  - Data download is not handled internally
  - Examples (in this `README` or in `tests`) use the [`searvey`](https://github.com/oceanmodeling/searvey) package
  - A release of cleaned data through Zenodo is considered (although not planned yet)

## Steps in the data
 - Step changes in data are currently only flagged via the `breakpoints` item in the JSON
 - No offset correction is applied

## Vertical datum
Vertical datums are not addressed

## Noise vs. Physical phenomena
Distinguishing noise (e.g. boat wakes) from real physical events can be difficult for noisy sensors
### Examples
(to be added)

## Subjectivity
- Cleaning decisions are inherently subjective
- Different operators may disagree on what should be discarded
