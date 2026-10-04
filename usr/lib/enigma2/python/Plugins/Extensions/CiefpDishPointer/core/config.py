# -*- coding: utf-8 -*-
# CiefpDishPointer - core/config.py
# Verzija: 1.0
# Autor: Ciefp
# Kompatibilno: Python 2 i Python 3

from enigma import getDesktop
from Components.config import (
    config,
    ConfigSubsection,
    ConfigText,
    ConfigSelection,
    ConfigYesNo,
    ConfigInteger,
)

# ============================================================
# ENIGMA2 KONFIGURACIJA
# ============================================================

config.plugins.CiefpDishPointer = ConfigSubsection()

# Jezik: EN ili SR
config.plugins.CiefpDishPointer.language = ConfigSelection(
    default="en",
    choices=[("en", "English"), ("sr", "Srpski")]
)

# Poslednja poznata lokacija
config.plugins.CiefpDishPointer.city = ConfigText(
    default="Kisac",
    fixed_size=False
)
config.plugins.CiefpDishPointer.country = ConfigText(
    default="Serbia",
    fixed_size=False
)
config.plugins.CiefpDishPointer.continent = ConfigText(
    default="Europe",
    fixed_size=False
)
config.plugins.CiefpDishPointer.latitude = ConfigText(
    default="45.29",
    fixed_size=False
)
config.plugins.CiefpDishPointer.longitude = ConfigText(
    default="19.7403",
    fixed_size=False
)

# Tip sistema: all / motorised / multi / single
config.plugins.CiefpDishPointer.system_type = ConfigSelection(
    default="motorised",
    choices=[
        ("all", "All Satellites"),
        ("motorised", "Motorised System"),
        ("multi", "Multi LNB Setup"),
        ("single", "Single Satellite"),
    ]
)

# Izabrani satelit (pozicija u desetinkama stepena, npr. 192 = 19.2E)
config.plugins.CiefpDishPointer.selected_sat = ConfigInteger(
    default=192,
    limits=(0, 3600)
)

# Automatska geolokacija pri startu
config.plugins.CiefpDishPointer.auto_location = ConfigYesNo(
    default=True
)

# Real-time osvežavanje signala (u sekundama)
config.plugins.CiefpDishPointer.signal_refresh = ConfigInteger(
    default=1,
    limits=(1, 10)
)


# ============================================================
# REČNIK JEZIKA
# ============================================================

LANGUAGES = {
    "en": {
        # Glavni naslov
        "title": "CiefpDishPointer",
        "subtitle": "Dish Pointer - Antenna Setup Helper",

        # Location
        "location_info": "Location Information",
        "continent": "Continent",
        "country": "Country",
        "city": "City",
        "latitude": "Latitude",
        "longitude": "Longitude",
        "change": "Change",

        # Satellite data
        "satellite_data": "Satellite Data",
        "all_satellites": "All Satellites",
        "motorised": "Motorised System",
        "multi_lnb": "Multi LNB Setup",
        "single_sat": "Single Satellite",
        "select_sat": "Select Satellite",

        # True South / North
        "true_south": "True South / True North",
        "azimuth_true": "Azimuth True",
        "azimuth_mag": "Azimuth Mag",
        "declination": "Declination",

        # Dish setup
        "dish_setup": "Dish Setup Data",
        "nearest_sat": "Nearest Satellite",
        "dish_elevation": "Dish Elevation",
        "lnb_skew": "LNB Skew",
        "left": "Left",
        "right": "Right",

        # Signal
        "snr": "SNR",
        "agc": "AGC",
        "lock": "Lock",
        "db": "DB",
        "locked": "LOCKED",
        "not_locked": "NOT LOCKED",
        # Multi LNB
        "mlnb_title": "Multi LNB Setup",
        "mlnb_no_selection": "No satellites selected",
        "mlnb_no_selection_hint": (
            "Select satellites you want to track\n"
            "using the OK button.\n\n"
            "Plugin will calculate which satellite\n"
            "is best for the zero (central) position."
        ),
        "mlnb_error": "Error",
        "mlnb_error_calc": "Cannot calculate zero satellite.",
        "mlnb_error_calc_detail": "Calculation error: %s",
        "mlnb_recommended": "Recommended zero satellite:",
        "mlnb_selected_count": "Selected satellites: %d",
        "mlnb_average_position": "Average position: %.1f deg",
        "mlnb_hint": (
            "OK = select/deselect satellite\n"
            "GREEN = confirm selection\n"
            "EXIT = back"
        ),

        # Buttons
        "exit": "EXIT",
        "satfinder": "SINGLE SATELLITE",
        "multi_lnb_btn": "MULTI LNB",
        "help_images": "HELP IMAGES",
        "language": "MENU:LANGUAGE",
        "location_edit": "INFO:LOCATION",
        "save": "SAVE",
        "cancel": "CANCEL",
        "ok": "OK",
        "back": "BACK",
        "close": "CLOSE",

        # Help - nazivi tema
        "help_topic_elevacija": "ELEVATION",
        "help_topic_azimut": "AZIMUTH",
        "help_topic_deklinacija": "DECLINATION",
        "help_topic_lnb_skew": "LNB SKEW",
        "help_topic_true_south": "TRUE SOUTH",
        "help_topic_motor_setup": "MOTOR SETUP",

        # Help
        "help_title": "Help - Explanation",
        "help_elevacija": (
            "ELEVATION\n\n"
            "The vertical angle of the dish.\n\n"
            "If the dish is too low, raise it.\n"
            "If too high, lower it.\n\n"
            "Check on the satellite arc:\n"
            "- Too low: dish points below the arc\n"
            "- Too high: dish points above the arc"
        ),
        "help_azimut": (
            "AZIMUTH\n\n"
            "The horizontal rotation of the dish.\n\n"
            "If the orbit is tilted west, rotate the dish east.\n"
            "If tilted east, rotate west.\n\n"
            "Use True South as reference."
        ),
        "help_deklinacija": (
            "DECLINATION\n\n"
            "The angle between the dish and the motor axis.\n\n"
            "If the orbit is too high, reduce declination.\n"
            "If too low, increase it.\n\n"
            "Typical value for Europe: 6-8 degrees."
        ),
        "help_lnb_skew": (
            "LNB SKEW\n\n"
            "Rotation of the LNB to compensate\n"
            "for the Earth's curvature.\n\n"
            "Rotate the LNB to the left or right\n"
            "according to the calculated value."
        ),
        "help_true_south": (
            "TRUE SOUTH\n\n"
            "The reference point for motorised systems.\n\n"
            "The dish must be aligned to True South (180°)\n"
            "when the motor is at 0 position.\n\n"
            "Use magnetic compass and adjust for declination."
        ),
        "help_motor_setup": (
            "MOTOR SETUP\n\n"
            "Ideal vs wrong orbit:\n"
            "- Ideal orbit: all satellites tracked\n"
            "- Wrong orbit: some satellites missing\n\n"
            "Adjust the mount according to the diagram."
        ),
        "loading": "Loading...",
        "no_internet": "No internet connection. Enter location manually.",
        "invalid_input": "Invalid input!",
        "saved": "Saved!",
    },

    "sr": {
        # Glavni naslov
        "title": "CiefpDishPointer",
        "subtitle": "Pomoc pri podesavanju antene",

        # Location
        "location_info": "Informacije o lokaciji",
        "continent": "Kontinent",
        "country": "Drzava",
        "city": "Grad",
        "latitude": "Geografska sirina",
        "longitude": "Geografska duzina",
        "change": "Promeni",

        # Satellite data
        "satellite_data": "Podaci o satelitu",
        "all_satellites": "Svi sateliti",
        "motorised": "Motorizovani sistem",
        "multi_lnb": "Multi LNB",
        "single_sat": "Pojedinacni satelit",
        "select_sat": "Izaberi satelit",

        # True South / North
        "true_south": "Pravi jug / Pravi sever",
        "azimuth_true": "Azimut pravi",
        "azimuth_mag": "Azimut magnetni",
        "declination": "Deklinacija",

        # Dish setup
        "dish_setup": "Podesavanje tanjira",
        "nearest_sat": "Najblizi satelit",
        "dish_elevation": "Elevacija tanjira",
        "lnb_skew": "LNB zakretanje",
        "left": "Levo",
        "right": "Desno",

        # Signal
        "snr": "SNR",
        "agc": "AGC",
        "lock": "Lock",
        "db": "DB",
        "locked": "ZAKLJUCAN",
        "not_locked": "NIJE ZAKLJUCAN",
        # Multi LNB
        "mlnb_title": "Multi LNB podesavanje",
        "mlnb_no_selection": "Nema izabranih satelita",
        "mlnb_no_selection_hint": (
            "Oznaci satelite koje zelis da pratis\n"
            "pomocu OK tastera.\n\n"
            "Plugin ce izracunati koji satelit\n"
            "je najbolji za nulti (centralni) polozaj."
        ),
        "mlnb_error": "Greska",
        "mlnb_error_calc": "Nije moguce izracunati nulti satelit.",
        "mlnb_error_calc_detail": "Greska pri izracunavanju: %s",
        "mlnb_recommended": "Preporuceni nulti satelit:",
        "mlnb_selected_count": "Izabrano satelita: %d",
        "mlnb_average_position": "Srednja pozicija: %.1f deg",
        "mlnb_hint": (
            "OK = oznaci/odznaci satelit\n"
            "GREEN = potvrdi izbor\n"
            "EXIT = nazad"
        ),

        # Buttons
        "exit": "IZLAZ",
        "satfinder": "POJEDINACNI SATELIT",
        "multi_lnb_btn": "MULTI LNB",
        "help_images": "SLIKE POMOCI",
        "language": "MENI:JEZIK",
        "location_edit": "INFO:LOKACIJA",
        "save": "SNIMI",
        "cancel": "OTKAZI",
        "ok": "OK",
        "back": "NAZAD",
        "close": "ZATVORI",

        # Help - nazivi tema
        "help_topic_elevacija": "ELEVACIJA",
        "help_topic_azimut": "AZIMUT",
        "help_topic_deklinacija": "DEKLINACIJA",
        "help_topic_lnb_skew": "LNB ZAKRETANJE",
        "help_topic_true_south": "PRAVI JUG",
        "help_topic_motor_setup": "PODESAVANJE MOTORA",

        # Help
        "help_title": "Pomoc - Objasnjenje",
        "help_elevacija": (
            "ELEVACIJA\n\n"
            "Vertikalni ugao tanjira.\n\n"
            "Ako je tanjir prenizak, podigni ga.\n"
            "Ako je previsok, spusti ga.\n\n"
            "Proveri na satelitskom luku:\n"
            "- Prenizak: tanjir gleda ispod luka\n"
            "- Previsok: tanjir gleda iznad luka"
        ),
        "help_azimut": (
            "AZIMUT\n\n"
            "Horizontalna rotacija tanjira.\n\n"
            "Ako je orbita nagnuta ka zapadu,\n"
            "zakreni tanjir ka istoku.\n"
            "Ako je ka istoku, zakreni ka zapadu.\n\n"
            "Koristi pravi jug kao referencu."
        ),
        "help_deklinacija": (
            "DEKLINACIJA\n\n"
            "Ugao izmedju tanjira i ose motora.\n\n"
            "Ako je orbita previsoka,\n"
            "smanji deklinaciju.\n"
            "Ako je preniska, povecaj je.\n\n"
            "Tipicna vrednost za Evropu: 6-8 stepeni."
        ),
        "help_lnb_skew": (
            "LNB ZAKRETANJE\n\n"
            "Rotacija LNB-a da kompenzuje\n"
            "zakrivljenost Zemlje.\n\n"
            "Zakreni LNB levo ili desno\n"
            "prema izracunatoj vrednosti."
        ),
        "help_true_south": (
            "PRAVI JUG\n\n"
            "Referentna tacka za motorizovane sisteme.\n\n"
            "Tanjir mora biti poravnat sa pravim jugom (180°)\n"
            "kada je motor u 0 poziciji.\n\n"
            "Koristi magnetni kompas i koriguj deklinaciju."
        ),
        "help_motor_setup": (
            "PODESAVANJE MOTORA\n\n"
            "Idealna vs pogresna orbita:\n"
            "- Idealna orbita: svi sateliti praceni\n"
            "- Pogresna orbita: neki sateliti nedostaju\n\n"
            "Podesi nosac prema dijagramu."
        ),
    },
}

# ============================================================
# POMOĆNE FUNKCIJE
# ============================================================

def get_language():
    """Vraća trenutni jezik (en ili sr)."""
    return config.plugins.CiefpDishPointer.language.value


def _(key):
    """
    Prevod kljuca u trenutni jezik.
    Ako kljuc ne postoji, vraca sam kljuc.
    """
    lang = get_language()
    return LANGUAGES.get(lang, LANGUAGES["en"]).get(key, key)


def get_help_text(key):
    """Vraća tekstualno objasnjenje za sliku."""
    return _(key)


# ============================================================
# DETEKCIJA REZOLUCIJE
# ============================================================

def is_fhd():
    """Proverava da li je rezolucija FHD (1920x1080) ili veca."""
    try:
        return getDesktop(0).size().width() >= 1920
    except:
        return False


def is_hd():
    """Proverava da li je rezolucija HD (1280x720)."""
    try:
        w = getDesktop(0).size().width()
        return 1280 <= w < 1920
    except:
        return False