# -*- coding: utf-8 -*-
# CiefpDishPointer - screens/satfinder.py
# Verzija: 1.0
# Autor: Ciefp
# Kompatibilno: Python 2 i Python 3

from Screens.Screen import Screen
from Components.Label import Label
from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Components.ScrollLabel import ScrollLabel
from ..core.config import _, config
from ..core.calc import calculate_all


class SatFinderScreen(Screen):
    skin = """
        <screen name="SatFinderScreen" position="center,center" size="1400,900" 
                title="Sat Finder" backgroundColor="#001020" flags="wfNoBorder">

            <eLabel position="0,0" size="1400,60" backgroundColor="#004000" zPosition="1"/>
            <widget name="title" position="0,0" size="1400,60" 
                    font="Regular;34" foregroundColor="#ffffff" 
                    halign="center" valign="center" transparent="1" zPosition="2"/>

            <eLabel position="20,80" size="660,780" 
                    backgroundColor="#001830" zPosition="1"/>

            <widget name="sat_list" position="30,90" size="640,760" 
                    itemHeight="45"
                    font="Regular;26" foregroundColor="#ffffff" 
                    transparent="1" zPosition="2"/>

            <eLabel position="700,80" size="680,780" 
                    backgroundColor="#001830" zPosition="1"/>

            <widget name="info_header" position="720,100" size="640,50" 
                    font="Regular;30" foregroundColor="#ffff00" 
                    halign="left" valign="center" transparent="1" zPosition="2"/>

            <widget name="info_text" position="720,170" size="640,600" 
                    font="Regular;28" foregroundColor="#ffffff" 
                    halign="left" valign="top" transparent="1" zPosition="2"/>

            <widget name="hint" position="720,800" size="640,50" 
                    font="Regular;22" foregroundColor="#aaaaaa" 
                    halign="center" valign="center" transparent="1" zPosition="2"/>
        </screen>
    """

    def __init__(self, session, satellites):
        Screen.__init__(self, session)
        self.session = session
        self.satellites = satellites
        self.selected_sat = None

        # ============================================================
        # WIDGETI
        # ============================================================
        self["title"] = Label("Single Satellite")
        self["sat_list"] = MenuList([])
        self["info_header"] = Label(_("dish_setup"))
        self["info_text"] = Label("")
        self["hint"] = Label("OK = izaberi | EXIT = nazad")

        # ============================================================
        # POPUNI LISTU
        # ============================================================
        self._build_list()

        # ============================================================
        # AKCIJE
        # ============================================================
        self["actions"] = ActionMap(
            ["OkCancelActions", "DirectionActions"],
            {
                "cancel": self.keyCancel,
                "ok": self.keyOk,
                "up": self.keyUp,
                "down": self.keyDown,
                "left": self.keyUp,
                "right": self.keyDown,
            },
            -1
        )

        # Selektuj trenutni satelit iz config-a
        self.onLayoutFinish.append(self._select_current)
        self.onLayoutFinish.append(self._update_info)

    # ============================================================
    # LISTA
    # ============================================================

    def _build_list(self):
        """Popunjava listu satelita."""
        items = []
        for sat in self.satellites:
            items.append("%s  (%.1f)" % (sat.name, sat.position_float))
        self["sat_list"].setList(items)

    def _select_current(self):
        """Selektuje trenutni satelit iz config-a."""
        pos = config.plugins.CiefpDishPointer.selected_sat.value
        for i, sat in enumerate(self.satellites):
            if sat.position == pos:
                self["sat_list"].moveToIndex(i)
                break

    def _get_current_satellite(self):
        """Vraca trenutno selektovani satelit."""
        idx = self["sat_list"].getSelectedIndex()
        if 0 <= idx < len(self.satellites):
            return self.satellites[idx]
        return None

    # ============================================================
    # INFO PANEL
    # ============================================================

    def _update_info(self):
        """Azurira desni panel sa izracunatim vrednostima."""
        sat = self._get_current_satellite()
        if not sat:
            self["info_text"].setText("")
            return

        try:
            lat = float(config.plugins.CiefpDishPointer.latitude.value)
            lon = float(config.plugins.CiefpDishPointer.longitude.value)
        except:
            lat = 0.0
            lon = 0.0

        data = calculate_all(lat, lon, sat.position_float)

        skew_str = "%.1f° %s" % (
            abs(data["skew"]),
            _("right") if data["skew"] >= 0 else _("left")
        )

        text = (
            "%s: %s\n\n"
            "%s: %.1f°\n"
            "%s: %.1f°\n"
            "%s: %.1f°\n"
            "%s: %s\n\n"
            "%s: %.1f°"
        ) % (
            _("nearest_sat"), sat.name,
            _("azimuth_true"), data["azimuth_true"],
            _("azimuth_mag"), data["azimuth_mag"],
            _("dish_elevation"), data["elevation"],
            _("lnb_skew"), skew_str,
            _("declination"), data["declination"],
        )

        self["info_header"].setText(sat.name)
        self["info_text"].setText(text)

    # ============================================================
    # KEY ACTIONS
    # ============================================================

    def keyUp(self):
        """Pomeri selekciju gore."""
        self["sat_list"].up()
        self._update_info()

    def keyDown(self):
        """Pomeri selekciju dole."""
        self["sat_list"].down()
        self._update_info()

    def keyOk(self):
        """OK - izaberi satelit i zatvori ekran."""
        sat = self._get_current_satellite()
        if sat:
            self.close(sat)

    def keyCancel(self):
        """EXIT - zatvori bez izbora."""
        self.close(None)