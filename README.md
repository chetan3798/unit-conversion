# Unit Converter

A fast, interactive unit converter covering everyday, scientific, and industrial measurements, built with Python, Flask, and Pint.

## Features

* **60+ Engine Categories:** Supports 60+ physical dimensions under the hood, with 27+ categories exposed directly in the UI dropdown (Length, Weight, Temperature, Volume, Area, Speed, Acceleration, Force, Torque, Density, Pressure, Energy, Power, Voltage, Resistance, Frequency, Digital Storage, Viscosity, Radiation, and more).
* **Smart Category Search:** Quickly filter and jump to any category using the instant search bar.
* **Dual Display Modes:**
  * **Single Conversion:** Direct unit-to-unit conversions with interactive unit swap (`from ↔ to`), value swap (drop result back into input), and copy-to-clipboard.
  * **Multi-Unit View ("All Units" Mode):** Convert a single input into every unit within a category simultaneously. Click any converted row to make it the new starting value.
* **Precision Controls:** Custom rounding options including **Auto**, **2 decimals**, **4 decimals**, **6 decimals**, or **Scientific notation**.
* **Conversion Equations:** Expandable mathematical formula display showing the exact defining equation for active conversions.
* **Non-Linear Conversion Handling:** Accurately calculates non-linear scales such as Temperature (offset formulas), Fuel Efficiency (reciprocal dimension mapping between mpg and L/100km), API Gravity, pH, and AWG Wire Gauge.
* **Dimensional Guardrails:** Categorized by genuine physical dimension (e.g., separating dynamic vs. kinematic viscosity, or voltage vs. current) to prevent impossible cross-dimension conversions.
* **Interactive UI:** Light/dark theme toggle, reset shortcut (`Esc`), and smooth transitions when switching categories.

## Tech Stack

* **Backend:** Python 3, Flask, Pint (Unit registry and conversion math)
* **Frontend:** Jinja2 templates, Vanilla JavaScript (ES6+), CSS3 (Custom design & theme variables)
* **Data Layer:** Database-free. All unit mappings and registry definitions reside in `conversions/pint_convert.py`.

## Project Structure

```text
.
├── app.py                      # Flask routes & UI_CATEGORIES dropdown metadata
├── conversions/
│   ├── __init__.py
│   └── pint_convert.py         # Central conversion engine using Pint
├── templates/
│   ├── index.html              # Main converter web view
│   └── about.html              # Information & documentation page
└── static/
    ├── style.css               # Application layout & theme styling
    └── script.js               # Frontend UI logic & API handler
```

## Setup & Installation

### Prerequisites

* Python 3.8 or higher

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/chetan3798/unit-conversion.git](https://github.com/chetan3798/unit-conversion.git)
   cd unit-converter
   ```

2. **Install dependencies:**
   ```bash
   pip install flask pint
   ```

3. **Verify the conversion engine:**
   Run the test script to check conversion engine output against known reference conversions:
   ```bash
   python conversions/pint_convert.py
   ```
   *The script prints `OK` or `MISMATCH` for ~40 reference tests across categories.*

4. **Launch the application:**
   ```bash
   python app.py
   ```

5. **Open in browser:**
   Navigate to `http://127.0.0.1:5000`.

## API Documentation

### Single Conversion
`POST /api/convert`

**Request Body:**
```json
{
  "category": "length",
  "from_unit": "in",
  "to_unit": "cm",
  "value": 1
}
```

**Response:**
```json
{
  "result": 2.54
}
```

### Multi-Unit Conversion
`POST /api/convert-all`

**Request Body:**
```json
{
  "category": "length",
  "from_unit": "in",
  "value": 1
}
```

**Response:**
```json
{
  "results": [
    { "unit": "mm", "result": 25.4 },
    { "unit": "cm", "result": 2.54 },
    { "unit": "m", "result": 0.0254 }
  ]
}
```

## Exposing Additional Categories

The conversion engine (`conversions/pint_convert.py`) supports over 60 categories. To display an additional category in the web frontend, add its key and metadata to `UI_CATEGORIES` in `app.py`.

## Deliberately Unsupported Units

The following units are intentionally excluded to prevent inaccurate or misleading conversions:

| Unit | Reason |
| :--- | :--- |
| **Mach number** | Dynamic quantity dependent on local temperature and sound speed |
| **Lumen ↔ Lux** | Non-equivalent physical dimensions (luminous flux vs. illuminance) |
| **TEU (Shipping)** | Industry nominal estimate, not a standardized physical unit |
| **Deadweight tonnage** | Equivalent to mass in metric tons (handled via Weight category) |
| **Paper basis weight (lb)** | Non-standardized; varies by paper grade definitions |
| **Turbidity (NTU)** | Empirical optical measurement without fixed mathematical conversions |

*Note: Sheet metal gauge and steel hardness scales (Rockwell/Brinell/Vickers) use correlation tables—verify against ASTM A480 / E140 standards for production engineering applications.*

## License

Distributed under the MIT License. See `LICENSE` for details.
