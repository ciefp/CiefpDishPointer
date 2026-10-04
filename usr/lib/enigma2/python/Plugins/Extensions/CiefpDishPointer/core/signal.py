# -*- coding: utf-8 -*-
# CiefpDishPointer - core/signal.py
# Verzija: 1.1
# Autor: Ciefp
# Kompatibilno: Python 2 i Python 3

from enigma import iServiceInformation


# ============================================================
# GLAVNA FUNKCIJA - SIGNAL IZ FRONTENDA
# ============================================================

def get_signal_data(session):
    """
    Cita signal podatke iz trenutnog tunera preko frontendInfo().
    
    Returns:
        dict sa kljucevima:
        - snr: SNR u procentima (0-100)
        - snr_db: SNR u dB
        - agc: AGC u procentima (0-100)
        - ber: Bit Error Rate
        - lock: bool
    """
    result = {
        "snr": 0,
        "snr_db": 0.0,
        "agc": 0,
        "ber": 0,
        "lock": False,
    }

    try:
        service = session.nav.getCurrentService()
        if not service:
            return result

        frontendInfo = service.frontendInfo()
        if not frontendInfo:
            return result

        fd = frontendInfo.getAll(True)
        if not fd:
            return result

        # SNR - kvalitet signala (0-65535 -> 0-100%)
        quality = fd.get("tuner_signal_quality", 0)
        result["snr"] = min(100, quality // 655)

        # SNR u dB
        snr_db = fd.get("tuner_signal_quality_db", 0) / 100.0
        if snr_db <= 0.0 and result["snr"] > 0:
            # Aproksimacija ako tuner ne daje dB
            snr_db = (result["snr"] / 100.0) * 20.0
        result["snr_db"] = snr_db

        # AGC - snaga signala (0-65535 -> 0-100%)
        power = fd.get("tuner_signal_power", 0)
        result["agc"] = min(100, power // 655)

        # BER
        result["ber"] = fd.get("tuner_bit_error_rate", 0)

        # Lock
        result["lock"] = result["snr"] > 0

        return result

    except Exception as e:
        print("[CiefpDishPointer] Greska u get_signal_data: %s" % e)
        return result


# ============================================================
# TRENUTNI SERVIS
# ============================================================

def get_current_service_info(session):
    """
    Vraca informacije o trenutnom servisu.
    """
    result = {
        "channel": "",
        "provider": "",
        "frequency": 0,
        "symbol_rate": 0,
        "polarization": "",
        "fec": "",
    }

    try:
        service = session.nav.getCurrentService()
        if not service:
            return result

        info = service.info()
        if not info:
            return result

        result["channel"] = info.getName() or ""
        result["provider"] = info.getInfoString(iServiceInformation.sProvider) or ""

        frontendInfo = service.frontendInfo()
        if frontendInfo:
            fd = frontendInfo.getAll(True)
            if fd:
                result["frequency"] = fd.get("frequency", 0) // 1000
                result["symbol_rate"] = fd.get("symbol_rate", 0) // 1000

        return result

    except Exception as e:
        print("[CiefpDishPointer] Greska u get_current_service_info: %s" % e)
        return result


# ============================================================
# TRENUTNI SATELIT
# ============================================================

def get_current_satellite(session):
    """
    Vraca trenutni satelit iz frontendInfo.
    """
    result = {
        "position": 0,
        "position_float": 0.0,
        "name": "",
    }

    try:
        service = session.nav.getCurrentService()
        if not service:
            return result

        frontendInfo = service.frontendInfo()
        if not frontendInfo:
            return result

        fd = frontendInfo.getAll(True)
        if not fd:
            return result

        orbital = fd.get("orbital_position", 0)
        if orbital > 1800:
            orbital = orbital - 3600

        result["position"] = orbital
        result["position_float"] = orbital / 10.0

        # Ime satelita iz satellites.xml
        try:
            from .satellites import load_satellites
            for sat in load_satellites():
                if sat.position == orbital:
                    result["name"] = sat.name
                    break
        except:
            pass

        return result

    except Exception as e:
        print("[CiefpDishPointer] Greska u get_current_satellite: %s" % e)
        return result