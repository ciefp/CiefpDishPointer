# -*- coding: utf-8 -*-
# CiefpDishPointer - core/location.py
# Verzija: 1.0
# Autor: Ciefp
# Kompatibilno: Python 2 i Python 3

import sys
import json
from threading import Thread

# Python 2/3 kompatibilnost
PY3 = sys.version_info[0] == 3

if PY3:
    from urllib.request import urlopen, Request
    from urllib.error import URLError
else:
    from urllib2 import urlopen, Request, URLError


# ============================================================
# KONFIGURACIJA
# ============================================================

# ip-api.com - besplatan, ne zahteva API key, limit 45 req/min
IP_API_URL = "http://ip-api.com/json/?fields=status,country,countryCode,regionName,city,lat,lon,timezone,query"

# Timeout u sekundama
HTTP_TIMEOUT = 8


# ============================================================
# GLAVNA FUNKCIJA
# ============================================================

def get_location_from_ip():
    """
    Dobavlja lokaciju preko IP adrese.
    
    Returns:
        dict sa kljucevima:
        - success: bool
        - continent: str
        - country: str
        - country_code: str
        - region: str
        - city: str
        - latitude: float
        - longitude: float
        - timezone: str
        - ip: str
        - error: str (ako nije uspelo)
    """
    result = {
        "success": False,
        "continent": "",
        "country": "",
        "country_code": "",
        "region": "",
        "city": "",
        "latitude": 0.0,
        "longitude": 0.0,
        "timezone": "",
        "ip": "",
        "error": "",
    }

    try:
        req = Request(IP_API_URL)
        req.add_header("User-Agent", "CiefpDishPointer/1.0")

        if PY3:
            response = urlopen(req, timeout=HTTP_TIMEOUT)
            raw = response.read().decode("utf-8")
        else:
            response = urlopen(req, timeout=HTTP_TIMEOUT)
            raw = response.read()

        data = json.loads(raw)

        if data.get("status") != "success":
            result["error"] = "IP API vratio status: %s" % data.get("status", "unknown")
            return result

        # Popuni rezultat
        result["success"] = True
        result["country"] = data.get("country", "")
        result["country_code"] = data.get("countryCode", "")
        result["region"] = data.get("regionName", "")
        result["city"] = data.get("city", "")
        result["latitude"] = float(data.get("lat", 0.0))
        result["longitude"] = float(data.get("lon", 0.0))
        result["timezone"] = data.get("timezone", "")
        result["ip"] = data.get("query", "")

        # Kontinent na osnovu country_code
        result["continent"] = country_to_continent(result["country_code"])

        return result

    except URLError as e:
        result["error"] = "URL greska: %s" % str(e)
        return result
    except Exception as e:
        result["error"] = "Greska: %s" % str(e)
        return result


# ============================================================
# KONTINENT NA OSNOVU COUNTRY CODE
# ============================================================

CONTINENT_MAP = {
    # Evropa
    "AL": "Europe", "AD": "Europe", "AT": "Europe", "BY": "Europe",
    "BE": "Europe", "BA": "Europe", "BG": "Europe", "HR": "Europe",
    "CY": "Europe", "CZ": "Europe", "DK": "Europe", "EE": "Europe",
    "FI": "Europe", "FR": "Europe", "DE": "Europe", "GR": "Europe",
    "HU": "Europe", "IS": "Europe", "IE": "Europe", "IT": "Europe",
    "XK": "Europe", "LV": "Europe", "LI": "Europe", "LT": "Europe",
    "LU": "Europe", "MK": "Europe", "MT": "Europe", "MD": "Europe",
    "MC": "Europe", "ME": "Europe", "NL": "Europe", "NO": "Europe",
    "PL": "Europe", "PT": "Europe", "RO": "Europe", "RU": "Europe",
    "SM": "Europe", "RS": "Europe", "SK": "Europe", "SI": "Europe",
    "ES": "Europe", "SE": "Europe", "CH": "Europe", "UA": "Europe",
    "GB": "Europe", "VA": "Europe",

    # Severna Amerika
    "US": "North America", "CA": "North America", "MX": "North America",

    # Juzna Amerika
    "BR": "South America", "AR": "South America", "CL": "South America",
    "CO": "South America", "PE": "South America", "VE": "South America",

    # Azija
    "CN": "Asia", "JP": "Asia", "IN": "Asia", "KR": "Asia",
    "TR": "Asia", "IL": "Asia", "SA": "Asia", "AE": "Asia",
    "TH": "Asia", "VN": "Asia", "PH": "Asia", "ID": "Asia",
    "MY": "Asia", "SG": "Asia", "PK": "Asia", "BD": "Asia",

    # Afrika
    "ZA": "Africa", "EG": "Africa", "NG": "Africa", "KE": "Africa",
    "MA": "Africa", "TN": "Africa", "DZ": "Africa", "LY": "Africa",

    # Australija
    "AU": "Australia", "NZ": "Australia",
}


def country_to_continent(country_code):
    """Vraca kontinent na osnovu country code."""
    return CONTINENT_MAP.get(country_code.upper(), "Unknown")


# ============================================================
# THREAD ZA GEOLOKACIJU
# ============================================================

class LocationThread(Thread):
    """
    Thread koji dobavlja lokaciju preko IP adrese.
    Ne blokira glavni UI thread.
    """

    def __init__(self, callback):
        """
        Args:
            callback: funkcija koja se poziva kada se dobiju podaci.
                      Potpis: callback(result_dict)
        """
        Thread.__init__(self)
        self.callback = callback
        self.daemon = True
        self._stopped = False

    def run(self):
        try:
            result = get_location_from_ip()
            if not self._stopped:
                self.callback(result)
        except Exception as e:
            if not self._stopped:
                self.callback({
                    "success": False,
                    "error": str(e),
                })

    def stop(self):
        """Zaustavlja thread."""
        self._stopped = True


# ============================================================
# POMOCNE FUNKCIJE
# ============================================================

def is_valid_latitude(lat):
    """Proverava da li je geografska sirina validna."""
    try:
        lat = float(lat)
        return -90.0 <= lat <= 90.0
    except:
        return False


def is_valid_longitude(lon):
    """Proverava da li je geografska duzina validna."""
    try:
        lon = float(lon)
        return -180.0 <= lon <= 180.0
    except:
        return False


def format_coordinates(lat, lon):
    """Formatira koordinate za prikaz."""
    lat_str = "%.4f°%s" % (abs(lat), "N" if lat >= 0 else "S")
    lon_str = "%.4f°%s" % (abs(lon), "E" if lon >= 0 else "W")
    return lat_str, lon_str