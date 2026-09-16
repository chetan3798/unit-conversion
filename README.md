# Unit Converter

A fast, no-frills unit converter covering everyday and industrial measurements, built with Flask and [Pint](https://pint.readthedocs.io).

## Features

- **60+ categories** — from everyday units (length, weight, temperature, volume) to industrial ones (pressure, torque, flow rate, electrical, radiation, viscosity) and specialist scales (API gravity, pH, AWG wire gauge, steel hardness)
- **Dropdown category picker** with a smooth fade transition when switching categories
- **Two separate swap actions** — one swaps the *units* (from ↔ to), the other swaps the *values* (drops the current result back into the input), since these are genuinely different actions
- **Convert to all units at once** — toggle a category into "All units" mode to see one value converted into every unit in that category simultaneously; tap any row to make it the new starting value
- **Reset button** — restores the current category's default value and unit pair
- **Correct handling of non-linear conversions** — temperature (offset formula), fuel efficiency (reciprocal-dimension handling between mpg and L/100km), API gravity, pH, and AWG wire gauge all use their real defining formulas rather than an approximated ratio
- **Dimensional guardrails** — categories are split by genuine physical dimension (e.g. dynamic vs. kinematic viscosity, or voltage vs. current) so you can never accidentally convert between things that aren't actually the same kind of quantity

## Tech stack

- **Backend:** Python 3, Flask, [Pint](https://pint.readthedocs.io) (unit registry and conversion math)
- **Frontend:** Jinja2 templates, vanilla JavaScript, plain CSS — no frontend framework
- **Data:** no database. All category/unit definitions live in `conversions/pint_convert.py`

## Project structure

```
.
├── app.py                      # Flask routes + UI_CATEGORIES (dropdown metadata)
├── conversions/
│   ├── __init__.py
│   └── pint_convert.py         # All conversion logic -- every category routes through convert()
├── templates/
│   ├── index.html              # Main converter page
│   └── about.html
└── static/
    ├── style.css
    └── script.js                # Builds the UI from UI_CATEGORIES, calls /api/convert(-all)
```

## Setup

```bash
pip install flask pint
python app.py
```

Then open `http://127.0.0.1:5000`.

## Verify the conversion engine before trusting it

`pint_convert.py` was written without a live Pint installation to test against. Run it directly after installing Pint:

```bash
python conversions/pint_convert.py
```

It prints `OK` or `MISMATCH` against ~40 known reference conversions covering every category. A handful of less common unit names (`oil_barrel`, `british_thermal_unit`, `standard_atmosphere`, `short_ton`, `bushel`, `therm`, `ampere_hour`, `oersted`, `standard_gravity`, `delta_degF`) are the most likely to need a one-line name correction depending on your installed Pint version — the script output will tell you exactly which ones, if any.

The non-Pint special cases (wire gauge, pH, temperature) are pure Python and have already been tested independently of Pint.

## API

**`POST /api/convert`**
```json
{ "category": "length", "from_unit": "in", "to_unit": "cm", "value": 1 }
```
→ `{ "result": 2.54 }`

**`POST /api/convert-all`**
```json
{ "category": "length", "from_unit": "in", "value": 1 }
```
→ `{ "results": [{ "unit": "mm", "result": 25.4 }, { "unit": "cm", "result": 2.54 }, ...] }`

## Categories currently in the dropdown

`UI_CATEGORIES` in `app.py` exposes 11 everyday categories in the site's UI: length, weight, temperature, volume, area, speed, pressure, energy, power, digital storage, time.

`pint_convert.py`'s conversion engine supports many more (force, torque, flow rate, density, viscosity, electrical quantities, radiation, and more) that aren't wired into the dropdown yet — add an entry to `UI_CATEGORIES` to expose any of them in the UI.

## Deliberately not supported

A few units were left out on purpose rather than implemented incorrectly:

| Unit | Why |
|---|---|
| Mach number | Not a fixed unit — depends on local speed of sound |
| Lumen ↔ lux | Different physical dimensions (flux vs. flux-per-area) |
| TEU (shipping) | Industry convention, not a fixed physical unit |
| Deadweight tonnage | Already just weight in metric tons — use the weight category |
| Paper basis weight (lb) | Varies by paper grade, not standardized |
| Turbidity (NTU) | Empirical optical measurement with no conversion formula to anything else |

Sheet metal gauge and steel hardness scales (Rockwell/Brinell/Vickers) *are* implemented, but as approximate lookup/correlation tables written from memory — verify against ASTM A480 / E140 before relying on them for real engineering decisions.
