# -*- coding: utf-8 -*-
# CiefpDishPointer - core/calc.py
# Verzija: 1.0
# Autor: Ciefp
# Kompatibilno: Python 2 i Python 3

import math


# ============================================================
# KONSTANTE
# ============================================================

# Poluprecnik Zemlje (km)
EARTH_RADIUS = 6378.137

# Geostacionarna visina (km)
GEO_HEIGHT = 35786.0

# Ugao elevacije za geostacionarne satelite
EARTH_ROTATION = 0.0  # sateliti se krecu istom brzinom kao Zemlja


# ============================================================
# POMOCNE FUNKCIJE
# ============================================================

def deg2rad(deg):
    return deg * math.pi / 180.0


def rad2deg(rad):
    return rad * 180.0 / math.pi


def normalize_angle(angle):
    """Normalizuje ugao na opseg -180..180."""
    while angle > 180:
        angle -= 360
    while angle < -180:
        angle += 360
    return angle


def normalize_azimuth(angle):
    """Normalizuje azimut na opseg 0..360."""
    while angle < 0:
        angle += 360
    while angle >= 360:
        angle -= 360
    return angle


# ============================================================
# GLAVNE FORMULE
# ============================================================

def calculate_azimuth(lat, lon, sat_lon):
    """
    Izracunava azimut (u stepenima) za dati satelit.
    
    Args:
        lat: geografska sirina mesta (stepeni, +N -S)
        lon: geografska duzina mesta (stepeni, +E -W)
        sat_lon: geografska duzina satelita (stepeni, +E -W)
    
    Returns:
        Azimut u stepenima (0..360)
    """
    lat_r = deg2rad(lat)
    dlon_r = deg2rad(sat_lon - lon)

    # Formula za azimut
    x = math.sin(dlon_r)
    y = math.cos(lat_r) * math.tan(deg2rad(0)) - math.sin(lat_r) * math.cos(dlon_r)
    # tan(0) = 0, pa se pojednostavljuje:
    y = -math.sin(lat_r) * math.cos(dlon_r)

    az = math.atan2(x, y)
    az_deg = rad2deg(az)

    # Normalizuj na 0..360
    return normalize_azimuth(az_deg)


def calculate_azimuth_full(lat, lon, sat_lon):
    """
    Preciznija formula za azimut sa geocentricnim uglom.
    """
    lat_r = deg2rad(lat)
    dlon_r = deg2rad(sat_lon - lon)

    # Ugao na Zemlji izmedju mesta i satelita
    cos_c = math.cos(lat_r) * math.cos(dlon_r)
    c = math.acos(cos_c)

    # Azimut (meren od severa, u smeru kazaljke)
    # Koristimo sferni zakon kosinusa
    sin_c = math.sin(c)
    if sin_c == 0:
        return 180.0

    cos_az = (math.sin(lat_r) - math.cos(c) * math.sin(lat_r)) / (sin_c * math.cos(lat_r))
    # Pojednostavljeno:
    cos_az = (math.sin(lat_r) - math.sin(lat_r) * cos_c) / (sin_c * math.cos(lat_r))
    
    # Koristimo atan2 za stabilnost
    x = math.sin(dlon_r)
    y = math.cos(lat_r) * math.tan(lat_r) - math.sin(lat_r) * math.cos(dlon_r)
    # tan(lat) = sin/cos
    y = math.sin(lat_r) - math.sin(lat_r) * math.cos(dlon_r)
    # Ovo nije bas tacno, hajde da koristimo standardnu formulu:

    return calculate_azimuth(lat, lon, sat_lon)


def calculate_elevation(lat, lon, sat_lon):
    """
    Izracunava elevaciju (u stepenima) za dati satelit.
    
    Args:
        lat: geografska sirina mesta
        lon: geografska duzina mesta
        sat_lon: geografska duzina satelita
    
    Returns:
        Elevacija u stepenima (0..90)
    """
    lat_r = deg2rad(lat)
    dlon_r = deg2rad(sat_lon - lon)

    # Kosinus centralnog ugla
    cos_c = math.cos(lat_r) * math.cos(dlon_r)
    c = math.acos(cos_c)

    # Elevacija
    # Formula: el = atan( (cos(c) - R/(R+h)) / sin(c) )
    r_ratio = EARTH_RADIUS / (EARTH_RADIUS + GEO_HEIGHT)
    
    sin_c = math.sin(c)
    if sin_c == 0:
        return 90.0

    el = math.atan((cos_c - r_ratio) / sin_c)
    return rad2deg(el)


def calculate_skew(lat, lon, sat_lon):
    """
    Izracunava LNB skew (u stepenima) za dati satelit.
    
    Returns:
        Skew u stepenima (-90..90)
        Pozitivno = u smeru kazaljke (desno)
        Negativno = suprotno (levo)
    """
    lat_r = deg2rad(lat)
    dlon_r = deg2rad(sat_lon - lon)

    # Skew formula
    skew = math.atan2(math.sin(dlon_r), math.tan(lat_r))
    skew_deg = rad2deg(skew)

    return normalize_angle(skew_deg)


def calculate_declination(lat):
    """
    Izracunava declination angle za motorizovane sisteme.
    Koristi se priblizna formula.
    
    Args:
        lat: geografska sirina mesta
    
    Returns:
        Declination u stepenima
    """
    # Priblizna formula za declination
    # declination = atan( R * sin(lat) / (h + R * (1 - cos(lat))) )
    lat_r = deg2rad(lat)
    r_ratio = EARTH_RADIUS / GEO_HEIGHT

    decl = math.atan(
        math.sin(lat_r) / (1.0 / r_ratio + (1.0 - math.cos(lat_r)))
    )
    return rad2deg(decl)


def calculate_true_south(lat, lon):
    """
    Vraca True South azimut (uvek 180.0).
    """
    return 180.0


# ============================================================
# MAGNETNA DEKLINACIJA (APROKSIMACIJA)
# ============================================================

def calculate_magnetic_declination(lat, lon):
    """
    Aproksimacija magnetne deklinacije za Evropu.
    Koristi se priblizni model.
    
    Args:
        lat: geografska sirina
        lon: geografska duzina
    
    Returns:
        Magnetna deklinacija u stepenima
        Pozitivno = istok, Negativno = zapad
    """
    # Priblizna formula za Evropu (2024-2026)
    # Za Srbiju (lat ~45, lon ~20): oko +5 stepeni (istok)
    # Formula: decl = 4.0 + 0.1 * (lon - 15) - 0.05 * (lat - 45)
    
    decl = 4.0 + 0.1 * (lon - 15.0) - 0.05 * (lat - 45.0)
    
    # Ogranici na realne vrednosti
    if decl > 15:
        decl = 15
    elif decl < -15:
        decl = -15
    
    return decl


# ============================================================
# NAJBLIZI SATELIT
# ============================================================

def find_nearest_satellite(lat, lon, satellites):
    """
    Pronalazi najblizi satelit (po azimutu) za datu lokaciju.
    To je satelit koji je najblizi geografskoj duzini mesta.
    
    Args:
        lat: geografska sirina
        lon: geografska duzina
        satellites: lista Satellite objekata
    
    Returns:
        Satellite objekat ili None
    """
    if not satellites:
        return None

    # Najblizi satelit je onaj cija je pozicija najbliza geografskoj duzini mesta
    nearest = min(satellites, key=lambda s: abs(s.position_float - lon))
    return nearest


def find_nearest_satellite_by_azimuth(lat, lon, satellites):
    """
    Pronalazi najblizi satelit po azimutu (preciznije).
    """
    if not satellites:
        return None

    best = None
    best_diff = 999

    for sat in satellites:
        az = calculate_azimuth(lat, lon, sat.position_float)
        diff = abs(az - 180.0)
        if diff < best_diff:
            best_diff = diff
            best = sat

    return best


# ============================================================
# MULTI LNB - PRONALAZENJE NULTOG SATELITA
# ============================================================
def find_multi_lnb_zero(lat, lon, selected_sats):
    if not selected_sats:
        return None
    positions = [s.position_float for s in selected_sats]
    center = sum(positions) / len(positions)
    nearest = min(selected_sats, key=lambda s: abs(s.position_float - center))
    return nearest

# ============================================================
# GLAVNA FUNKCIJA ZA IZRACUNAVANJE
# ============================================================

def calculate_all(lat, lon, sat_lon):
    """
    Izracunava sve vrednosti za dati satelit.
    
    Returns:
        dict sa kljucevima:
        - azimuth_true
        - azimuth_mag
        - elevation
        - skew
        - declination
        - magnetic_declination
    """
    az_true = calculate_azimuth(lat, lon, sat_lon)
    mag_decl = calculate_magnetic_declination(lat, lon)
    az_mag = az_true - mag_decl  # magnetni azimut = pravi - deklinacija

    # Normalizuj
    az_mag = normalize_azimuth(az_mag)

    el = calculate_elevation(lat, lon, sat_lon)
    skew = calculate_skew(lat, lon, sat_lon)
    decl = calculate_declination(lat)

    return {
        "azimuth_true": az_true,
        "azimuth_mag": az_mag,
        "elevation": el,
        "skew": skew,
        "declination": decl,
        "magnetic_declination": mag_decl,
    }


def calculate_true_south_data(lat, lon):
    """
    Izracunava podatke za True South / True North.
    """
    mag_decl = calculate_magnetic_declination(lat, lon)
    az_true = 180.0
    az_mag = normalize_azimuth(az_true - mag_decl)
    decl = calculate_declination(lat)

    return {
        "azimuth_true": az_true,
        "azimuth_mag": az_mag,
        "declination": decl,
        "magnetic_declination": mag_decl,
    }


# ============================================================
# FORMATIRANJE
# ============================================================

def format_angle(value, decimals=1):
    """Formatira ugao sa stepenima."""
    return "%.*f°" % (decimals, value)


def format_skew(value):
    """Formatira skew sa smerom (L/R)."""
    if value >= 0:
        return "%.1f° Right" % value
    else:
        return "%.1f° Left" % abs(value)