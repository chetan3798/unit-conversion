import math
import pint

ureg = pint.UnitRegistry()

_CUSTOM_UNIT_DEFINITIONS = [
    "ton_of_refrigeration = 3.51685 * kilowatt = TR",
    "board_foot = 144 * inch ** 3 = FBM",
    "denier = gram / (9000 * meter) = den",
    "tex = gram / (1000 * meter)",
    "print_point = inch / 72",
    "print_pica = 12 * print_point",
    "legacy_rad = 0.01 * gray",
    "legacy_rem = 0.01 * sievert",
    "microinch = inch / 1e6 = uin",
]
for _definition in _CUSTOM_UNIT_DEFINITIONS:
    try:
        ureg.define(_definition)
    except Exception:
        pass


CATEGORY_UNITS = {

    "length": {
        "mm": "millimeter", "cm": "centimeter", "m": "meter", "km": "kilometer",
        "in": "inch", "ft": "foot", "yd": "yard", "mile": "mile",
        "nmi": "nautical_mile", "mil": "mil", "micron": "micrometer",
    },

    "weight": {
        "mg": "milligram", "g": "gram", "kg": "kilogram", "ton": "metric_ton",
        "lb": "pound", "oz": "ounce", "short_ton": "short_ton",
        "long_ton": "long_ton", "stone": "stone", "troy_oz": "troy_ounce",
    },

    "volume": {
        "mL": "milliliter", "L": "liter", "gal": "gallon", "gal_uk": "imperial_gallon",
        "qt": "quart", "pt": "pint", "cup": "cup", "tbsp": "tablespoon",
        "tsp": "teaspoon", "floz": "fluid_ounce", "barrel": "oil_barrel",
        "bushel": "bushel", "acre_ft": "acre_foot", "board_ft": "board_foot",
    },

    "area": {
        "mm2": "millimeter ** 2", "cm2": "centimeter ** 2", "m2": "meter ** 2",
        "km2": "kilometer ** 2", "ft2": "foot ** 2", "yd2": "yard ** 2",
        "acre": "acre", "hectare": "hectare", "sqmile": "mile ** 2",
    },

    "speed": {
        "kmh": "kilometer / hour", "mph": "mile / hour",
        "ms": "meter / second", "knot": "knot",
    },

    "pressure": {
        "Pa": "pascal", "kPa": "kilopascal", "MPa": "megapascal", "bar": "bar",
        "atm": "standard_atmosphere", "psi": "psi", "mmHg": "mmHg",
        "inHg": "inHg", "torr": "torr",
    },

    "energy": {
        "J": "joule", "kJ": "kilojoule", "MJ": "megajoule", "cal": "calorie",
        "kcal": "kilocalorie", "BTU": "british_thermal_unit",
        "kWh": "kilowatt_hour", "therm": "therm",
    },

    "power": {
        "W": "watt", "kW": "kilowatt", "MW": "megawatt", "hp": "horsepower",
        "BTU_hr": "british_thermal_unit / hour", "ton_ref": "ton_of_refrigeration",
    },

    "force": {
        "N": "newton", "kN": "kilonewton", "lbf": "pound_force",
        "kgf": "kilogram_force", "dyne": "dyne",
    },

    "torque": {
        "Nm": "newton * meter", "lbft": "pound_force * foot",
        "lbin": "pound_force * inch", "kgfm": "kilogram_force * meter",
    },

    "flow_rate": {
        "Lmin": "liter / minute", "Ls": "liter / second",
        "m3hr": "meter ** 3 / hour", "gpm": "gallon / minute",
        "cfm": "foot ** 3 / minute", "bbl_day": "oil_barrel / day",
    },

    "density": {
        "kgm3": "kilogram / meter ** 3", "gcm3": "gram / centimeter ** 3",
        "lbft3": "pound / foot ** 3", "lbgal": "pound / gallon",
    },

    "viscosity_dynamic": {
        "cP": "centipoise", "Pas": "pascal * second", "poise": "poise",
    },
    "viscosity_kinematic": {
        "cSt": "centistokes", "St": "stokes", "m2s": "meter ** 2 / second",
    },

    "digital_storage": {
        "bit": "bit", "byte": "byte",
        "KB": "kilobyte", "MB": "megabyte", "GB": "gigabyte", "TB": "terabyte", "PB": "petabyte",
        "KiB": "kibibyte", "MiB": "mebibyte", "GiB": "gibibyte", "TiB": "tebibyte",
    },

    "data_transfer_rate": {
        "bps": "bit / second", "Kbps": "kilobit / second",
        "Mbps": "megabit / second", "Gbps": "gigabit / second", "MBs": "megabyte / second",
    },

    "frequency": {
        "Hz": "hertz", "kHz": "kilohertz", "MHz": "megahertz", "GHz": "gigahertz",
    },

    "rotation_speed": {
        "rpm": "revolution / minute", "rads": "radian / second", "hz": "hertz",
    },

    "time": {
        "sec": "second", "min": "minute", "hour": "hour", "day": "day",
        "week": "week", "year": "year",
    },

    "angle": {
        "deg": "degree", "rad": "radian", "grad": "gradian",
        "arcmin": "arcminute", "arcsec": "arcsecond",
    },

    "voltage": {"V": "volt", "kV": "kilovolt", "mV": "millivolt"},
    "current": {"A": "ampere", "mA": "milliampere", "uA": "microampere", "kA": "kiloampere"},
    "resistance": {"ohm": "ohm", "kohm": "kiloohm", "Mohm": "megaohm"},
    "capacitance": {"F": "farad", "uF": "microfarad", "nF": "nanofarad", "pF": "picofarad"},
    "inductance": {"H": "henry", "mH": "millihenry", "uH": "microhenry"},
    "apparent_power": {"VA": "volt * ampere", "kVA": "kilovolt * ampere", "MVA": "megavolt * ampere"},

    "illuminance": {
        "lux": "lux", "fc": "footcandle",
    },

    "radiation_dose": {"Gy": "gray", "rad": "legacy_rad", "Sv": "sievert", "rem": "legacy_rem"},
    "radiation_activity": {"Bq": "becquerel", "Ci": "curie"},

    "typography_length": {"pt": "print_point", "pica": "print_pica", "in": "inch", "mm": "millimeter"},

    "print_resolution": {"dpi": "1 / inch", "dpcm": "1 / centimeter", "dpmm": "1 / millimeter"},

    "textile_linear_density": {"denier": "denier", "tex": "tex"},

    "electric_charge": {"C": "coulomb", "Ah": "ampere_hour"},
    "magnetic_flux": {"Wb": "weber"},
    "magnetic_flux_density": {"T": "tesla", "G": "gauss"},
    "magnetic_field_strength": {"Am": "ampere / meter", "Oe": "oersted"},
    "electric_field_strength": {"Vm": "volt / meter"},
    "luminous_intensity": {"cd": "candela"},
    "luminance": {"cdm2": "candela / meter ** 2"},

    "molar_concentration": {"molL": "mole / liter", "molm3": "mole / meter ** 3"},
    "molar_mass": {"gmol": "gram / mole"},
    "electrical_conductivity_solution": {
        "Sm": "siemens / meter", "uScm": "microsiemens / centimeter", "mScm": "millisiemens / centimeter",
    },
    "water_hardness": {"gpg": "grain / gallon", "mgL": "milligram / liter"},

    "specific_heat_capacity": {
        "JkgK": "joule / (kilogram * kelvin)", "BTUlbF": "british_thermal_unit / (pound * delta_degF)",
    },
    "thermal_conductivity": {
        "WmK": "watt / (meter * kelvin)", "BTUhrftF": "british_thermal_unit / (hour * foot * delta_degF)",
    },
    "thermal_resistance": {
        "Rvalue": "foot ** 2 * delta_degF * hour / british_thermal_unit",
        "RSI": "meter ** 2 * kelvin / watt",
    },
    "specific_energy_density": {
        "MJkg": "megajoule / kilogram", "Whkg": "watt_hour / kilogram", "BTUlb": "british_thermal_unit / pound",
    },
    "power_density": {"Wkg": "watt / kilogram", "Wm3": "watt / meter ** 3"},

    "acceleration": {"ms2": "meter / second ** 2", "fts2": "foot / second ** 2", "g": "standard_gravity"},
    "angular_acceleration": {"rads2": "radian / second ** 2"},
    "surface_tension": {"Npm": "newton / meter", "dynecm": "dyne / centimeter"},
    "surface_roughness": {"um": "micrometer", "uin": "microinch"},
    "cutting_speed": {"sfm": "foot / minute", "mmin": "meter / minute"},

    "air_changes_per_hour": {"ach": "1 / hour", "acm": "1 / minute"},
    "heat_transfer_coefficient": {
        "Wm2K": "watt / (meter ** 2 * kelvin)", "BTUhrft2F": "british_thermal_unit / (hour * foot ** 2 * delta_degF)",
    },
}


RATIO_CATEGORIES = {
    "concentration_ratio": {"ppm": 1e-6, "ppb": 1e-9, "ppt": 1e-12, "percent": 1e-2},
    "sound_level": {"dB": 1.0, "dBA": 1.0, "dBm": 1.0, "Bel": 10.0, "Np": 8.6859},
    "viscosity": {"Pas": 1.0, "cP": 0.001, "cSt": 0.001},
    "angle_rotation": {"rad": 1.0, "deg": math.pi / 180.0, "rpm": (2.0 * math.pi) / 60.0},
    "illuminance_luminance": {"lx": 1.0, "fc": 10.7639104167, "nit": math.pi, "lm": 1.0},
}


TEMPERATURE_UNITS = {"C": "degC", "F": "degF", "K": "kelvin"}

def convert_temperature(from_unit, to_unit, value):
    def to_celsius(unit, v):
        if unit == "C": return v
        if unit == "F": return (v - 32) * 5 / 9
        return v - 273.15
    def from_celsius(c, unit):
        if unit == "C": return c
        if unit == "F": return c * 9 / 5 + 32
        return c + 273.15
    return from_celsius(to_celsius(from_unit, value), to_unit)


def convert_fuel_efficiency(from_unit, to_unit, value):
    if value <= 0:
        return 0.0
    if from_unit == 'km_per_l':
        kml = value
    elif from_unit == 'mpg_us':
        kml = value * (1.609344 / 3.785411784)
    elif from_unit == 'mpg_uk':
        kml = value * (1.609344 / 4.54609)
    elif from_unit == 'l_per_100km':
        kml = 100.0 / value
    else:
        raise KeyError(f"Unknown fuel unit: {from_unit}")

    if to_unit == 'km_per_l':
        return kml
    elif to_unit == 'mpg_us':
        return kml / (1.609344 / 3.785411784)
    elif to_unit == 'mpg_uk':
        return kml / (1.609344 / 4.54609)
    elif to_unit == 'l_per_100km':
        return 100.0 / kml
    else:
        raise KeyError(f"Unknown fuel unit: {to_unit}")


WATER_DENSITY_KGM3 = 999.016

def convert_density(from_unit, to_unit, value):
    density_units = CATEGORY_UNITS["density"]

    def to_kgm3(unit, v):
        if unit == "api_gravity":
            specific_gravity = 141.5 / (v + 131.5)
            return specific_gravity * WATER_DENSITY_KGM3
        return ureg.Quantity(v, density_units[unit]).to("kilogram / meter ** 3").magnitude

    def from_kgm3(kgm3, unit):
        if unit == "api_gravity":
            specific_gravity = kgm3 / WATER_DENSITY_KGM3
            return (141.5 / specific_gravity) - 131.5
        return ureg.Quantity(kgm3, "kilogram / meter ** 3").to(density_units[unit]).magnitude

    return from_kgm3(to_kgm3(from_unit, value), to_unit)


def awg_to_mm(awg):
    return 0.127 * 92 ** ((36 - awg) / 39)

def mm_to_awg(diameter_mm):
    return 36 - 39 * math.log(diameter_mm / 0.127, 92)

def convert_wire_gauge(from_unit, to_unit, value):
    def to_mm(unit, v):
        if unit == "AWG": return awg_to_mm(v)
        if unit == "mm": return v
        if unit == "in": return v * 25.4
        raise KeyError(f"Unknown wire_gauge unit: {unit}")
    def from_mm(mm, unit):
        if unit == "AWG": return mm_to_awg(mm)
        if unit == "mm": return mm
        if unit == "in": return mm / 25.4
        raise KeyError(f"Unknown wire_gauge unit: {unit}")
    return from_mm(to_mm(from_unit, value), to_unit)


def ph_to_concentration(ph):
    return 10 ** (-ph)

def concentration_to_ph(h_conc_mol_l):
    return -math.log10(h_conc_mol_l)

def convert_ph(from_unit, to_unit, value):
    if from_unit == to_unit:
        return value
    if from_unit == "pH" and to_unit == "molL":
        return ph_to_concentration(value)
    if from_unit == "molL" and to_unit == "pH":
        return concentration_to_ph(value)
    raise KeyError(f"Unknown ph unit pair: {from_unit} -> {to_unit}")


_HARDNESS_TABLE_STEEL = [
    (20, 226, 238), (25, 253, 266), (30, 286, 302),
    (35, 327, 345), (40, 371, 392), (45, 421, 446),
    (50, 481, 513), (55, 550, 595), (60, 634, 697), (65, 739, 817),
]

def _interpolate_hardness(value, from_index, to_index):
    table = _HARDNESS_TABLE_STEEL
    if value <= table[0][from_index]:
        return table[0][to_index]
    if value >= table[-1][from_index]:
        return table[-1][to_index]
    for row1, row2 in zip(table, table[1:]):
        if row1[from_index] <= value <= row2[from_index]:
            fraction = (value - row1[from_index]) / (row2[from_index] - row1[from_index])
            return row1[to_index] + fraction * (row2[to_index] - row1[to_index])
    raise ValueError("Value out of interpolation range")

def convert_hardness_steel(from_unit, to_unit, value):
    index = {"HRC": 0, "HB": 1, "HV": 2}
    if from_unit not in index or to_unit not in index:
        raise KeyError(f"Unknown hardness_steel unit: {from_unit} or {to_unit}")
    if from_unit == to_unit:
        return value
    return _interpolate_hardness(value, index[from_unit], index[to_unit])


STEEL_SHEET_GAUGE_MM = {
    7: 4.55, 8: 4.18, 9: 3.80, 10: 3.42, 11: 3.04, 12: 2.66,
    13: 2.28, 14: 1.90, 16: 1.52, 18: 1.21, 20: 0.912,
    22: 0.759, 24: 0.607, 26: 0.455, 28: 0.379, 30: 0.304,
}

def convert_sheet_metal_gauge_steel(from_unit, to_unit, value):
    def to_mm(unit, v):
        if unit == "gauge":
            if v not in STEEL_SHEET_GAUGE_MM:
                raise KeyError(f"Gauge {v} not in table -- add it from your reference spec.")
            return STEEL_SHEET_GAUGE_MM[v]
        if unit == "mm": return v
        if unit == "in": return v * 25.4
        raise KeyError(f"Unknown sheet_metal_gauge_steel unit: {unit}")
    def from_mm(mm, unit):
        if unit == "gauge":
            return min(STEEL_SHEET_GAUGE_MM, key=lambda g: abs(STEEL_SHEET_GAUGE_MM[g] - mm))
        if unit == "mm": return mm
        if unit == "in": return mm / 25.4
        raise KeyError(f"Unknown sheet_metal_gauge_steel unit: {unit}")
    return from_mm(to_mm(from_unit, value), to_unit)


def convert(category: str, from_unit: str, to_unit: str, value: float) -> float:
    if category == "temperature":
        return convert_temperature(from_unit, to_unit, value)
    if category == "fuel_efficiency":
        return convert_fuel_efficiency(from_unit, to_unit, value)
    if category == "density":
        return convert_density(from_unit, to_unit, value)
    if category == "wire_gauge":
        return convert_wire_gauge(from_unit, to_unit, value)
    if category == "ph":
        return convert_ph(from_unit, to_unit, value)
    if category == "hardness_steel":
        return convert_hardness_steel(from_unit, to_unit, value)
    if category == "sheet_metal_gauge_steel":
        return convert_sheet_metal_gauge_steel(from_unit, to_unit, value)
    if category in RATIO_CATEGORIES:
        table = RATIO_CATEGORIES[category]
        return value * table[from_unit] / table[to_unit]
    if category in CATEGORY_UNITS:
        unit_map = CATEGORY_UNITS[category]
        q = ureg.Quantity(value, unit_map[from_unit])
        return q.to(unit_map[to_unit]).magnitude
    raise KeyError(f"Unknown category: {category}")


def round_result(value: float) -> float:
    return round(value, 2) if abs(value) >= 100 else round(value, 4)


if __name__ == "__main__":
    checks = [
        ("length", "in", "cm", 1, 2.54),
        ("weight", "kg", "lb", 1, 2.2046),
        ("temperature", "C", "F", 0, 32),
        ("temperature", "C", "F", 100, 212),
        ("volume", "L", "gal", 1, 0.2642),
        ("volume", "gal_uk", "L", 1, 4.5461),
        ("speed", "mph", "kmh", 1, 1.6093),
        ("pressure", "atm", "psi", 1, 14.6959),
        ("energy", "kWh", "kJ", 1, 3600),
        ("power", "ton_ref", "kW", 1, 3.5169),
        ("force", "lbf", "N", 1, 4.4482),
        ("torque", "lbft", "Nm", 1, 1.3558),
        ("flow_rate", "gpm", "Lmin", 1, 3.7854),
        ("density", "lbft3", "kgm3", 1, 16.0185),
        ("density", "kgm3", "api_gravity", 999.016, 10.0),
        ("viscosity_dynamic", "poise", "cP", 1, 100),
        ("viscosity_kinematic", "St", "cSt", 1, 100),
        ("digital_storage", "GB", "MB", 1, 1000),
        ("data_transfer_rate", "Mbps", "Kbps", 1, 1000),
        ("frequency", "kHz", "Hz", 1, 1000),
        ("rotation_speed", "rpm", "rads", 1, 0.10472),
        ("angle", "deg", "rad", 90, 1.5708),
        ("voltage", "kV", "V", 1, 1000),
        ("concentration_ratio", "percent", "ppm", 1, 10000),
        ("sound_level", "Bel", "dB", 1, 10),
        ("fuel_efficiency", "mpg_us", "l_per_100km", 100, 2.3521),
        ("illuminance", "fc", "lux", 1, 10.7639),
        ("radiation_dose", "Gy", "rad", 1, 100),
        ("radiation_activity", "Ci", "Bq", 1, 3.7e10),
        ("wire_gauge", "AWG", "mm", 10, 2.588),
        ("wire_gauge", "AWG", "mm", 24, 0.5106),
        ("ph", "pH", "molL", 7, 1e-7),
        ("ph", "molL", "pH", 0.001, 3),
        ("hardness_steel", "HRC", "HB", 50, 481),
        ("electric_charge", "Ah", "C", 1, 3600),
        ("magnetic_flux_density", "T", "G", 1, 10000),
        ("magnetic_field_strength", "Oe", "Am", 1, 79.5775),
        ("molar_concentration", "molL", "molm3", 1, 1000),
        ("acceleration", "g", "ms2", 1, 9.80665),
        ("surface_tension", "Npm", "dynecm", 1, 1000),
        ("cutting_speed", "sfm", "mmin", 1, 0.3048),
        ("specific_energy_density", "Whkg", "MJkg", 1, 0.0036),
        ("air_changes_per_hour", "ach", "acm", 60, 1),
        ("thermal_conductivity", "WmK", "BTUhrftF", 1, 0.5778),
        ("heat_transfer_coefficient", "Wm2K", "BTUhrft2F", 1, 0.1761),
    ]
    for category, f, t, val, expected in checks:
        try:
            result = round(convert(category, f, t, val), 6)
            tolerance = max(0.01, abs(expected) * 0.001)
            status = "OK" if abs(result - expected) <= tolerance else "MISMATCH"
        except Exception as e:
            result, status = f"ERROR: {e}", "FAIL"
        print(f"[{status}] {val} {f} ({category}) -> {t} = {result} (expected ~{expected})")
        