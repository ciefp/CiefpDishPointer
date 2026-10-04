# -*- coding: utf-8 -*-
# CiefpDishPointer - screens/location_edit.py
# Verzija: 1.0
# Autor: Ciefp
# Kompatibilno: Python 2 i Python 3

from Screens.Screen import Screen
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Screens.MessageBox import MessageBox
from Components.Label import Label
from Components.ActionMap import ActionMap
from Components.config import config

from ..core.config import _, LANGUAGES, get_language
from ..core.location import is_valid_latitude, is_valid_longitude


class LocationEditScreen(Screen):
    skin = """
        <screen name="LocationEditScreen" position="center,center" size="1000,700" 
                title="Location Edit" backgroundColor="#001020" flags="wfNoBorder">
            
            <eLabel position="0,0" size="1000,60" backgroundColor="#004000" zPosition="1"/>
            <widget name="title" position="0,0" size="1000,60" 
                    font="Regular;34" foregroundColor="#ffffff" 
                    halign="center" valign="center" transparent="1" zPosition="2"/>
            
            <eLabel position="20,80" size="960,500" 
                    backgroundColor="#001830" zPosition="1"/>
            
            <!-- Continent -->
            <widget name="label_continent" position="40,100" size="300,50" 
                    font="Regular;28" foregroundColor="#ffff00" 
                    halign="left" valign="center" transparent="1" zPosition="2"/>
            <widget name="value_continent" position="360,100" size="600,50" 
                    font="Regular;28" foregroundColor="#ffffff" 
                    halign="left" valign="center" transparent="1" zPosition="2"/>
            
            <!-- Country -->
            <widget name="label_country" position="40,170" size="300,50" 
                    font="Regular;28" foregroundColor="#ffff00" 
                    halign="left" valign="center" transparent="1" zPosition="2"/>
            <widget name="value_country" position="360,170" size="600,50" 
                    font="Regular;28" foregroundColor="#ffffff" 
                    halign="left" valign="center" transparent="1" zPosition="2"/>
            
            <!-- City -->
            <widget name="label_city" position="40,240" size="300,50" 
                    font="Regular;28" foregroundColor="#ffff00" 
                    halign="left" valign="center" transparent="1" zPosition="2"/>
            <widget name="value_city" position="360,240" size="600,50" 
                    font="Regular;28" foregroundColor="#ffffff" 
                    halign="left" valign="center" transparent="1" zPosition="2"/>
            
            <!-- Latitude -->
            <widget name="label_lat" position="40,310" size="300,50" 
                    font="Regular;28" foregroundColor="#ffff00" 
                    halign="left" valign="center" transparent="1" zPosition="2"/>
            <widget name="value_lat" position="360,310" size="600,50" 
                    font="Regular;28" foregroundColor="#ffffff" 
                    halign="left" valign="center" transparent="1" zPosition="2"/>
            
            <!-- Longitude -->
            <widget name="label_lon" position="40,380" size="300,50" 
                    font="Regular;28" foregroundColor="#ffff00" 
                    halign="left" valign="center" transparent="1" zPosition="2"/>
            <widget name="value_lon" position="360,380" size="600,50" 
                    font="Regular;28" foregroundColor="#ffffff" 
                    halign="left" valign="center" transparent="1" zPosition="2"/>
            
            <!-- Hint -->
            <widget name="hint" position="40,430" size="920,140" 
                    font="Regular;22" foregroundColor="#aaaaaa" 
                    halign="left" valign="top" transparent="1" zPosition="2"/>
            
            <!-- Dugmici -->
            <widget name="key_red" position="40,600" size="300,60" 
                    backgroundColor="#cc0000" font="Regular;26" 
                    foregroundColor="#ffffff" halign="center" valign="center" zPosition="2"/>
            <widget name="key_green" position="360,600" size="300,60" 
                    backgroundColor="#008000" font="Regular;26" 
                    foregroundColor="#ffffff" halign="center" valign="center" zPosition="2"/>
        </screen>
    """

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session

        # ============================================================
        # WIDGETI
        # ============================================================
        self["title"] = Label("Location Edit")
        self["label_continent"] = Label(_("continent"))
        self["value_continent"] = Label("")
        self["label_country"] = Label(_("country"))
        self["value_country"] = Label("")
        self["label_city"] = Label(_("city"))
        self["value_city"] = Label("")
        self["label_lat"] = Label(_("latitude"))
        self["value_lat"] = Label("")
        self["label_lon"] = Label(_("longitude"))
        self["value_lon"] = Label("")
        self["hint"] = Label(
            "Strelicama gore/dole birate polje.\n"
            "OK otvara tastaturu za unos.\n"
            "GREEN snima, RED otkazuje."
        )
        self["key_red"] = Label(_("cancel"))
        self["key_green"] = Label(_("save"))

        # ============================================================
        # TRENUTNA SELEKCIJA (0=city, 1=lat, 2=lon)
        # ============================================================
        self.selected_field = 0

        # ============================================================
        # POPUNI VREDNOSTI
        # ============================================================
        self._load_values()

        # ============================================================
        # AKCIJE
        # ============================================================
        self["actions"] = ActionMap(
            ["OkCancelActions", "ColorActions", "DirectionActions"],
            {
                "cancel": self.keyCancel,
                "red": self.keyCancel,
                "green": self.keySave,
                "ok": self.keyOk,
                "up": self.keyUp,
                "down": self.keyDown,
                "left": self.keyUp,
                "right": self.keyDown,
            },
            -1
        )

        self.onLayoutFinish.append(self._highlight_current)

    # ============================================================
    # POPUNJAVANJE VREDNOSTI
    # ============================================================

    def _load_values(self):
        """Popunjava vrednosti iz config-a."""
        cfg = config.plugins.CiefpDishPointer
        self["value_continent"].setText(cfg.continent.value or "-")
        self["value_country"].setText(cfg.country.value or "-")
        self["value_city"].setText(cfg.city.value or "-")
        self["value_lat"].setText(cfg.latitude.value or "0")
        self["value_lon"].setText(cfg.longitude.value or "0")

    def _highlight_current(self):
        """Istice trenutno izabrano polje."""
        cfg = config.plugins.CiefpDishPointer

        # Ucitaj vrednosti
        cont = cfg.continent.value or "-"
        country = cfg.country.value or "-"
        city = cfg.city.value or "-"
        lat = cfg.latitude.value or "0"
        lon = cfg.longitude.value or "0"

        # Marker za trenutno polje
        m0 = "> " if self.selected_field == 0 else "  "
        m1 = "> " if self.selected_field == 1 else "  "
        m2 = "> " if self.selected_field == 2 else "  "

        self["value_continent"].setText(cont)
        self["value_country"].setText(country)
        self["value_city"].setText("%s%s" % (m0, city))
        self["value_lat"].setText("%s%s" % (m1, lat))
        self["value_lon"].setText("%s%s" % (m2, lon))

    # ============================================================
    # KEY ACTIONS
    # ============================================================

    def keyUp(self):
        self.selected_field = (self.selected_field - 1) % 3
        self._highlight_current()

    def keyDown(self):
        self.selected_field = (self.selected_field + 1) % 3
        self._highlight_current()

    def keyOk(self):
        """OK - otvara tastaturu za izabrano polje."""
        cfg = config.plugins.CiefpDishPointer

        if self.selected_field == 0:
            # City - tekstualna tastatura
            self.session.openWithCallback(
                self._on_city_entered,
                VirtualKeyBoard,
                title=_("city"),
                text=cfg.city.value or ""
            )
        elif self.selected_field == 1:
            # Latitude - numericka
            self.session.openWithCallback(
                self._on_lat_entered,
                VirtualKeyBoard,
                title=_("latitude"),
                text=cfg.latitude.value or "0"
            )
        elif self.selected_field == 2:
            # Longitude - numericka
            self.session.openWithCallback(
                self._on_lon_entered,
                VirtualKeyBoard,
                title=_("longitude"),
                text=cfg.longitude.value or "0"
            )

    def _on_city_entered(self, result):
        if result:
            config.plugins.CiefpDishPointer.city.value = result
            self["value_city"].setText(result)

    def _on_lat_entered(self, result):
        if result:
            if is_valid_latitude(result):
                config.plugins.CiefpDishPointer.latitude.value = result
                self["value_lat"].setText(result)
            else:
                self.session.open(
                    MessageBox,
                    _("invalid_input"),
                    MessageBox.TYPE_ERROR,
                    timeout=3
                )

    def _on_lon_entered(self, result):
        if result:
            if is_valid_longitude(result):
                config.plugins.CiefpDishPointer.longitude.value = result
                self["value_lon"].setText(result)
            else:
                self.session.open(
                    MessageBox,
                    _("invalid_input"),
                    MessageBox.TYPE_ERROR,
                    timeout=3
                )

    def keySave(self):
        """GREEN - snima i zatvara."""
        cfg = config.plugins.CiefpDishPointer
        cfg.city.save()
        cfg.latitude.save()
        cfg.longitude.save()
        self.close(True)

    def keyCancel(self):
        """RED - otkazuje i zatvara."""
        cfg = config.plugins.CiefpDishPointer
        cfg.city.cancel()
        cfg.latitude.cancel()
        cfg.longitude.cancel()
        self.close(False)