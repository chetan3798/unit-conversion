from flask import Flask, render_template, request, jsonify
from conversions.pint_convert import convert, round_result

app = Flask(__name__)

# Metadata for populating the category dropdown in the template.
# Keys here must match the category names convert() expects in pint_convert.py.
# Add more entries from CATEGORY_UNITS / RATIO_CATEGORIES in pint_convert.py
# if you want them selectable in the UI too.
UI_CATEGORIES = {
    "length": {
        "label": "Length", "icon": "ruler",
        "units": ["mm", "cm", "m", "km", "in", "ft", "yd", "mile"],
        "default": ["in", "cm"],
    },
    "weight": {
        "label": "Weight", "icon": "weight-scale",
        "units": ["mg", "g", "kg", "ton", "lb", "oz", "short_ton", "long_ton", "stone", "troy_oz"],
        "default": ["kg", "lb"],
    },
    "temperature": {
        "label": "Temperature", "icon": "temperature-half",
        "units": ["C", "F", "K"],
        "default": ["C", "F"],
    },
    "volume": {
        "label": "Volume", "icon": "droplet",
        "units": ["mL", "L", "gal", "gal_uk", "qt", "pt", "cup", "tbsp", "tsp", "floz", "barrel", "bushel", "acre_ft", "board_ft"],
        "default": ["L", "gal"],
    },
    "area": {
        "label": "Area", "icon": "vector-square",
        "units": ["mm2", "cm2", "m2", "km2", "ft2", "yd2", "acre", "hectare", "sqmile"],
        "default": ["acre", "hectare"],
    },
    "speed": {
        "label": "Speed", "icon": "gauge",
        "units": ["kmh", "mph", "ms", "knot"],
        "default": ["mph", "kmh"],
    },
    "pressure": {
        "label": "Pressure", "icon": "wind",
        "units": ["Pa", "kPa", "MPa", "bar", "atm", "psi", "mmHg", "inHg", "torr"],
        "default": ["psi", "kPa"],
    },
    "energy": {
        "label": "Energy", "icon": "bolt",
        "units": ["J", "kJ", "MJ", "cal", "kcal", "BTU", "kWh", "therm"],
        "default": ["kcal", "kJ"],
    },
    "power": {
        "label": "Power", "icon": "plug",
        "units": ["W", "kW", "MW", "hp", "BTU_hr", "ton_ref"],
        "default": ["hp", "kW"],
    },
    "digital_storage": {
        "label": "Digital storage", "icon": "floppy-disk",
        "units": ["bit", "byte", "KB", "MB", "GB", "TB", "PB", "KiB", "MiB", "GiB", "TiB"],
        "default": ["GB", "MB"],
    },
    "time": {
        "label": "Time", "icon": "clock",
        "units": ["sec", "min", "hour", "day", "week", "year"],
        "default": ["hour", "min"],
    },
    "voltage": {
        "label": "Voltage", "icon": "bolt",
        "units": ["V", "mV", "kV"],
        "default": ["V", "mV"],
    },
    "current": {
        "label": "Electric Current", "icon": "bolt-lightning",
        "units": ["A", "mA", "uA"],
        "default": ["A", "mA"],
    },
    "resistance": {
        "label": "Resistance", "icon": "microchip",
        "units": ["ohm", "kohm", "Mohm"],
        "default": ["ohm", "kohm"],
    },
    "frequency": {
        "label": "Frequency", "icon": "wave-square",
        "units": ["Hz", "kHz", "MHz", "GHz"],
        "default": ["Hz", "kHz"],
    },
    "flow_rate": {
        "label": "Volumetric Flow Rate", "icon": "faucet-drip",
        "units": ["cfm", "gpm", "Ls", "m3hr"],
        "default": ["cfm", "Ls"],
    },
    "viscosity": {
        "label": "Viscosity", "icon": "oil-can",
        "units": ["cP", "cSt", "Pas"],
        "default": ["cP", "Pas"],
    },
    "force": {
        "label": "Force", "icon": "hand-fist",
        "units": ["N", "kN", "lbf"],
        "default": ["N", "lbf"],
    },
    "torque": {
        "label": "Torque", "icon": "rotate",
        "units": ["Nm", "lbft"],
        "default": ["Nm", "lbft"],
    },
    "density": {
        "label": "Density", "icon": "cube",
        "units": ["kgm3", "gcm3", "lbft3"],
        "default": ["kgm3", "lbft3"],
    },
    "acceleration": {
        "label": "Acceleration", "icon": "forward-fast",
        "units": ["ms2", "g"],
        "default": ["ms2", "g"],
    },
    "angle_rotation": {
        "label": "Angles & Rotation", "icon": "compass",
        "units": ["deg", "rad", "rpm"],
        "default": ["deg", "rad"],
    },
    "data_transfer_rate": {
        "label": "Data Transfer Speed", "icon": "network-wired",
        "units": ["Mbps", "Gbps", "MBs"],
        "default": ["Mbps", "MBs"],
    },
    "sound_level": {
        "label": "Signal / Sound Level", "icon": "volume-high",
        "units": ["dB", "dBA", "dBm"],
        "default": ["dB", "dBA"],
    },
    "illuminance_luminance": {
        "label": "Illuminance & Luminance", "icon": "lightbulb",
        "units": ["lx", "fc", "nit", "lm"],
        "default": ["lx", "fc"],
    },
    "fuel_efficiency": {
        "label": "Fuel Economy", "icon": "gas-pump",
        "units": ["mpg_us", "mpg_uk", "l_per_100km", "km_per_l"],
        "default": ["mpg_us", "l_per_100km"],
    },
    "radiation_dose": {
        "label": "Radiation Dose", "icon": "radiation",
        "units": ["Sv", "Gy", "rem"],
        "default": ["Sv", "rem"],
    },
}


@app.route('/')
def index():
    return render_template('index.html', categories=UI_CATEGORIES)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/api/convert', methods=['POST'])
def api_convert():
    data = request.get_json() or {}
    category = data.get('category')
    from_unit = data.get('from_unit')
    to_unit = data.get('to_unit')
    value_raw = data.get('value')

    if category not in UI_CATEGORIES:
        return jsonify({'error': 'Invalid category'}), 400

    if value_raw is None or value_raw == '':
        return jsonify({'error': 'Enter a value'}), 400

    try:
        value = float(value_raw)
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid number'}), 400

    valid_units = UI_CATEGORIES[category]['units']
    if from_unit not in valid_units or to_unit not in valid_units:
        return jsonify({'error': 'Invalid unit'}), 400

    try:
        result = convert(category, from_unit, to_unit, value)
    except KeyError as e:
        return jsonify({'error': f'Unknown unit: {e}'}), 400

    return jsonify({'result': round_result(result)})


@app.route('/api/convert-all', methods=['POST'])
def api_convert_all():
    data = request.get_json() or {}
    category = data.get('category')
    from_unit = data.get('from_unit')
    value_raw = data.get('value')

    if category not in UI_CATEGORIES:
        return jsonify({'error': 'Invalid category'}), 400

    if value_raw is None or value_raw == '':
        return jsonify({'error': 'Enter a value'}), 400

    try:
        value = float(value_raw)
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid number'}), 400

    valid_units = UI_CATEGORIES[category]['units']
    if from_unit not in valid_units:
        return jsonify({'error': 'Invalid unit'}), 400

    results = []
    for unit in valid_units:
        try:
            converted = convert(category, from_unit, unit, value)
            results.append({'unit': unit, 'result': round_result(converted)})
        except KeyError:
            continue

    return jsonify({'results': results})


if __name__ == '__main__':
    app.run(debug=True)