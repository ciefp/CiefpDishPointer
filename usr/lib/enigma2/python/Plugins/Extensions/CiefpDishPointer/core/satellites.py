# -*- coding: utf-8 -*-
# CiefpDishPointer - core/satellites.py
# Verzija: 1.0
# Autor: Ciefp
# Kompatibilno: Python 2 i Python 3

import os
import re

try:
    from xml.etree import ElementTree as ET
except ImportError:
    import elementtree.ElementTree as ET


# ============================================================
# PUTANJE DO satellites.xml
# ============================================================

SATELLITES_XML_PATHS = [
    "/etc/enigma2/satellites.xml",
    "/etc/tuxbox/satellites.xml",
    "/usr/share/enigma2/satellites.xml",
    "/etc/satellites.xml",
]


def find_satellites_xml():
    """Pronalazi satellites.xml na poznatim lokacijama."""
    for path in SATELLITES_XML_PATHS:
        if os.path.isfile(path):
            return path
    return None


# ============================================================
# PARSIRANJE
# ============================================================

class Satellite(object):
    """Predstavlja jedan satelit."""

    def __init__(self, name, position, flags=0):
        self.name = name                # npr. "Astra 19.2E"
        self.position = position        # u desetinkama stepena, npr. 192
        self.flags = flags

    @property
    def position_float(self):
        """Pozicija u stepenima, npr. 19.2"""
        return self.position / 10.0

    @property
    def position_str(self):
        """Pozicija kao string, npr. '19.2E'"""
        p = self.position_float
        if p < 0:
            return "%.1fW" % abs(p)
        else:
            return "%.1fE" % p

    def __str__(self):
        return "%s (%.1f)" % (self.name, self.position_float)

    def __repr__(self):
        return "Satellite(%s, %d)" % (self.name, self.position)


def load_satellites():
    """
    Učitava sve satelite iz satellites.xml.
    Vraća listu Satellite objekata.
    """
    path = find_satellites_xml()
    if not path:
        return []

    satellites = []

    try:
        tree = ET.parse(path)
        root = tree.getroot()

        # Format 1: <satellites><sat name="..." position="192" /></satellites>
        for sat in root.findall("sat"):
            name = sat.get("name", "")
            pos = sat.get("position", "0")
            flags = int(sat.get("flags", "0"))
            try:
                pos_int = int(pos)
            except:
                continue
            if name:
                satellites.append(Satellite(name, pos_int, flags))

        # Format 2: <satellites><sat><transponder .../></sat></satellites>
        if not satellites:
            for sat in root.findall("sat"):
                name = sat.get("name", "")
                pos = sat.get("position", "0")
                flags = int(sat.get("flags", "0"))
                try:
                    pos_int = int(pos)
                except:
                    continue
                if name:
                    satellites.append(Satellite(name, pos_int, flags))

    except Exception as e:
        print("[CiefpDishPointer] Greska pri citanju satellites.xml: %s" % e)
        return []

    # Sortiraj po poziciji
    satellites.sort(key=lambda s: s.position)
    return satellites


def get_satellite_by_position(position):
    """
    Vraća Satellite objekat za datu poziciju (u desetinkama).
    Ako ne postoji, vraća None.
    """
    sats = load_satellites()
    for sat in sats:
        if sat.position == position:
            return sat
    return None


def get_satellite_by_name(name):
    """
    Vraća Satellite objekat za dato ime.
    Pretraga je case-insensitive i parcijalna.
    """
    sats = load_satellites()
    name_lower = name.lower()
    for sat in sats:
        if name_lower in sat.name.lower():
            return sat
    return None


def format_satellite_label(sat):
    """Vraća formatiran string za prikaz u listi."""
    return "%s  (%.1f)" % (sat.name, sat.position_float)