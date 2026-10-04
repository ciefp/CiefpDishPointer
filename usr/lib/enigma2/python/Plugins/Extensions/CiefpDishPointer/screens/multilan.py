# -*- coding: utf-8 -*-
# CiefpDishPointer - screens/multilan.py
# Verzija: 1.1
# Autor: Ciefp
# Kompatibilno: Python 2 i Python 3

from Screens.Screen import Screen
from Components.Label import Label
from Components.ActionMap import ActionMap
from Components.MenuList import MenuList

from ..core.config import _, config
from ..core.calc import calculate_all, find_multi_lnb_zero


class MultiLNBScreen(Screen):
    skin = """
        <screen name="MultiLNBScreen" position="center,center" size="1400,900" 
                title="Multi LNB Setup" backgroundColor="#001020" flags="wfNoBorder">
            
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
            
            <widget name="info_text" position="720,170" size="640,500" 
                    font="Regular;26" foregroundColor="#ffffff" 
                    halign="left" valign="top" transparent="1" zPosition="2"/>
            
            <widget name="hint" position="720,700" size="640,150" 
                    font="Regular;22" foregroundColor="#aaaaaa" 
                    halign="center" valign="top" transparent="1" zPosition="2"/>
        </screen>
    """

    def __init__(self, session, satellites, lat, lon):
        Screen.__init__(self, session)
        self.session = session
        self.satellites = satellites
        self.lat = lat
        self.lon = lon

        # Set izabranih satelita (pozicije)
        self.selected = set()
        # Preporuceni nulti satelit
        self.zero_sat = None

        # ============================================================
        # WIDGETI
        # ============================================================
        self["title"] = Label(_("mlnb_title"))
        self["sat_list"] = MenuList([])
        self["info_header"] = Label("")
        self["info_text"] = Label("")
        self["hint"] = Label(_("mlnb_hint"))

        # ============================================================
        # POPUNI LISTU
        # ============================================================
        self._build_list()

        # ============================================================
        # AKCIJE
        # ============================================================
        self["actions"] = ActionMap(
            ["OkCancelActions", "ColorActions", "DirectionActions"],
            {
                "cancel": self.keyCancel,
                "ok": self.keyToggle,
                "green": self.keySave,
                "up": self.keyUp,
                "down": self.keyDown,
                "left": self.keyUp,
                "right": self.keyDown,
            },
            -1
        )

        self.onLayoutFinish.append(self._update_info)

    # ============================================================
    # LISTA
    # ============================================================

    def _build_list(self):
        """Popunjava listu satelita sa checkbox-ovima."""
        items = []
        for sat in self.satellites:
            mark = "[X]" if sat.position in self.selected else "[ ]"
            items.append("%s %s  (%.1f)" % (
                mark, sat.name, sat.position_float
            ))
        self["sat_list"].setList(items)

    def _get_current_satellite(self):
        """Vraca trenutno selektovani satelit."""
        try:
            idx = self["sat_list"].getSelectedIndex()
            if 0 <= idx < len(self.satellites):
                return self.satellites[idx]
        except:
            pass
        return None

    # ============================================================
    # INFO PANEL
    # ============================================================
    def _update_info(self):
        """Azurira desni panel sa preporucenim nultim satelitom."""
        # Izabrani sateliti kao objekti
        selected_sats = [
            s for s in self.satellites if s.position in self.selected
        ]

        if not selected_sats:
            self["info_header"].setText(_("mlnb_no_selection"))
            self["info_text"].setText(_("mlnb_no_selection_hint"))
            self.zero_sat = None
            return

        # Preporuceni nulti satelit
        zero = find_multi_lnb_zero(self.lat, self.lon, selected_sats)
        self.zero_sat = zero

        if zero is None:
            self["info_header"].setText(_("mlnb_error"))
            self["info_text"].setText(_("mlnb_error_calc"))
            return

        # Izracunaj vrednosti za nulti satelit
        try:
            data = calculate_all(self.lat, self.lon, zero.position_float)
        except Exception as e:
            self["info_header"].setText(_("mlnb_error"))
            self["info_text"].setText(_("mlnb_error_calc_detail") % e)
            return

        skew_str = "%.1f deg %s" % (
            abs(data["skew"]),
            _("right") if data["skew"] >= 0 else _("left")
        )

        # Lista izabranih satelita (sortirana po poziciji)
        sorted_sats = sorted(selected_sats, key=lambda s: s.position_float)
        sat_labels = []
        for s in sorted_sats:
            pos = s.position_float
            if pos < 0:
                sat_labels.append("%.1fW" % abs(pos))
            else:
                sat_labels.append("%.1fE" % pos)
        sat_list_str = ", ".join(sat_labels)

        # Srednja pozicija
        try:
            avg_pos = sum(s.position_float for s in selected_sats) / len(selected_sats)
        except:
            avg_pos = 0.0

        text = (
            "%s\n\n"
            "%s: %.1f deg\n"
            "%s: %.1f deg\n"
            "%s: %.1f deg\n"
            "%s: %s\n\n"
            "%s\n"
            "%s\n\n"
            "%s"
        ) % (
            zero.name,
            _("azimuth_true"), data["azimuth_true"],
            _("azimuth_mag"), data["azimuth_mag"],
            _("dish_elevation"), data["elevation"],
            _("lnb_skew"), skew_str,
            _("mlnb_selected_count") % len(selected_sats),
            sat_list_str,
            _("mlnb_average_position") % avg_pos,
        )

        self["info_header"].setText(_("mlnb_recommended"))
        self["info_text"].setText(text)
    # ============================================================
    # KEY ACTIONS
    # ============================================================

    def keyToggle(self):
        """OK - oznaci/odznaci trenutni satelit."""
        sat = self._get_current_satellite()
        if not sat:
            return

        if sat.position in self.selected:
            self.selected.discard(sat.position)
        else:
            self.selected.add(sat.position)

        # Osvezi listu (checkbox)
        try:
            idx = self["sat_list"].getSelectedIndex()
        except:
            idx = 0
        self._build_list()
        try:
            self["sat_list"].moveToIndex(idx)
        except:
            pass

        # Osvezi info
        self._update_info()

    def keyUp(self):
        try:
            self["sat_list"].up()
        except:
            pass
        self._update_info()

    def keyDown(self):
        try:
            self["sat_list"].down()
        except:
            pass
        self._update_info()

    def keySave(self):
        """GREEN - potvrdi izbor i vrati nulti satelit."""
        if not self.selected:
            return

        if self.zero_sat:
            self.close(self.zero_sat)

    def keyCancel(self):
        """EXIT - zatvori bez izbora."""
        self.close(None)