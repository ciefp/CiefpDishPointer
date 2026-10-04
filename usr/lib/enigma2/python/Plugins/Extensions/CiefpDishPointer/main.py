# -*- coding: utf-8 -*-
# CiefpDishPointer - main.py
# Verzija: 1.1
# Autor: Ciefp
# Kompatibilno: Python 2 i Python 3

from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.Label import Label
from Components.ActionMap import ActionMap
from Components.ProgressBar import ProgressBar
from Components.Pixmap import Pixmap
from enigma import eTimer

from .core.config import _, config
from .core.location import LocationThread
from .core.satellites import load_satellites, find_satellites_xml
from .core.calc import (
    calculate_all,
    calculate_true_south_data,
    find_nearest_satellite,
    find_multi_lnb_zero,
)
from .core.signal import (
    get_signal_data,
    get_current_service_info,
    get_current_satellite,
)


PLUGIN_PATH = "/usr/lib/enigma2/python/Plugins/Extensions/CiefpDishPointer"


# ============================================================
# GLAVNI EKRAN
# ============================================================

class CiefpDishPointer(Screen):

    skin = """
        <screen name="CiefpDishPointer" position="0,0" size="1920,1080" 
                title="CiefpDishPointer" backgroundColor="#001020" flags="wfNoBorder">
            
            <!-- HEADER -->
            <eLabel position="0,0" size="1920,60" backgroundColor="#004000" zPosition="1"/>
            <widget name="title" position="0,0" size="1920,60" 
                    font="Regular;34" foregroundColor="#ffffff" 
                    halign="center" valign="center" transparent="1" zPosition="2"/>
            
            <!-- LEVA STRANA - PODACI -->
            <widget name="location_header" position="40,90" size="900,40" 
                    font="Regular;30" foregroundColor="#ffff00" transparent="1"/>
            <widget name="location_text" position="40,140" size="900,300" 
                    font="Regular;26" foregroundColor="#ffffff" transparent="1"/>
            
            <widget name="sat_header" position="40,360" size="900,40" 
                    font="Regular;30" foregroundColor="#ffff00" transparent="1"/>
            <widget name="sat_text" position="40,410" size="900,200" 
                    font="Regular;26" foregroundColor="#ffffff" transparent="1"/>
            
            <widget name="dish_header" position="40,630" size="900,40" 
                    font="Regular;30" foregroundColor="#ffff00" transparent="1"/>
            <widget name="dish_text" position="40,680" size="900,200" 
                    font="Regular;26" foregroundColor="#ffffff" transparent="1"/>
            
            <!-- DESNA STRANA - PANEL -->
            <eLabel position="1400,90" size="520,900" 
                    backgroundColor="#001830" zPosition="1"/>
            
            <widget name="clock" position="1500,100" size="380,120" 
                    font="Regular;40" foregroundColor="#ffffff" 
                    halign="center" valign="center" transparent="1" zPosition="2"/>
            
            <widget name="dish_icon" position="950,90" size="400,800" 
                    alphatest="on" zPosition="2"/>
            
            <widget name="plugin_icon" position="1500,230" size="300,180" 
                    alphatest="on" zPosition="2"/>
            
            <widget name="btn_exit" position="1430,440" size="420,55" 
                    font="Regular;26" foregroundColor="#ffffff" 
                    backgroundColor="#cc0000" halign="center" valign="center" zPosition="2"/>
            <widget name="btn_satfinder" position="1430,510" size="420,55" 
                    font="Regular;26" foregroundColor="#ffffff" 
                    backgroundColor="#008000" halign="center" valign="center" zPosition="2"/>
            <widget name="btn_multi" position="1430,580" size="420,55" 
                    font="Regular;26" foregroundColor="#000000" 
                    backgroundColor="#ffcc00" halign="center" valign="center" zPosition="2"/>
            <widget name="btn_help" position="1430,650" size="420,55" 
                    font="Regular;26" foregroundColor="#ffffff" 
                    backgroundColor="#0066cc" halign="center" valign="center" zPosition="2"/>
            <widget name="btn_lang" position="1430,720" size="420,55" 
                    font="Regular;26" foregroundColor="#ffffff" 
                    backgroundColor="#ff6600" halign="center" valign="center" zPosition="2"/>
            <widget name="btn_location" position="1430,790" size="420,55" 
                    font="Regular;26" foregroundColor="#ffffff" 
                    backgroundColor="#006666" halign="center" valign="center" zPosition="2"/>
            
            <!-- DONJI DEO - SIGNAL -->
            <eLabel position="0,910" size="1920,170" 
                    backgroundColor="#000000" zPosition="1"/>
            
            <widget name="current_service" position="20,915" size="1900,30" 
                    font="Regular;22" foregroundColor="#00ff00" 
                    halign="left" valign="center" transparent="1" zPosition="2"/>
            
            <!-- SNR red -->
            <widget name="snr_label" position="20,948" size="120,50" 
                    font="Bold;36" foregroundColor="#ffff00" 
                    halign="left" valign="center" transparent="1" zPosition="2"/>
            <widget name="snr_bar" position="150,955" size="1200,40" 
                    pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CiefpDishPointer/icon_snr.png"
                    borderWidth="2" borderColor="#000000" zPosition="2"/>
            <widget name="snr_percent" position="1380,948" size="180,50" 
                    font="Bold;36" foregroundColor="#ffffff" 
                    halign="center" valign="center" transparent="1" zPosition="2"/>
            <widget name="snr_db" position="1580,948" size="320,50" 
                    font="Bold;36" foregroundColor="#00ff00" 
                    halign="center" valign="center" transparent="1" zPosition="2"/>
            
            <!-- AGC red -->
            <widget name="agc_label" position="20,998" size="120,50" 
                    font="Bold;36" foregroundColor="#ffff00" 
                    halign="left" valign="center" transparent="1" zPosition="2"/>
            <widget name="agc_bar" position="150,1005" size="1200,40" 
                    pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CiefpDishPointer/icon_agc.png"
                    borderWidth="2" borderColor="#000000" zPosition="2"/>
            <widget name="agc_percent" position="1380,998" size="180,50" 
                    font="Bold;36" foregroundColor="#ffffff" 
                    halign="center" valign="center" transparent="1" zPosition="2"/>
        </screen>
    """

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session

        # ============================================================
        # PODACI
        # ============================================================
        self.satellites = load_satellites()
        self.selected_system = config.plugins.CiefpDishPointer.system_type.value
        self.selected_sat = None
        self.location_thread = None

        # ============================================================
        # WIDGETI
        # ============================================================
        self["title"] = Label(_("title"))
        self["location_header"] = Label(_("location_info"))
        self["location_text"] = Label("")
        self["sat_header"] = Label(_("satellite_data"))
        self["sat_text"] = Label("")
        self["dish_header"] = Label(_("dish_setup"))
        self["dish_text"] = Label("")
        self["clock"] = Label("")
        self["plugin_icon"] = Pixmap()
        self["dish_icon"] = Pixmap()

        self["btn_exit"] = Label(_("exit"))
        self["btn_satfinder"] = Label(_("satfinder"))
        self["btn_multi"] = Label(_("multi_lnb_btn"))
        self["btn_help"] = Label(_("help_images"))
        self["btn_lang"] = Label(_("language"))
        self["btn_location"] = Label(_("location_edit"))

        self["current_service"] = Label("")
        self["snr_label"] = Label(_("snr"))
        self["snr_bar"] = ProgressBar()
        self["snr_percent"] = Label("0%")
        self["snr_db"] = Label("DB:0.00")

        self["agc_label"] = Label(_("agc"))
        self["agc_bar"] = ProgressBar()
        self["agc_percent"] = Label("0%")

        # ============================================================
        # AKCIJE
        # ============================================================
        self["actions"] = ActionMap(
            ["OkCancelActions", "ColorActions", "SetupActions", "DirectionActions"],
            {
                "cancel": self.keyCancel,
                "ok": self.keyOk,
                "red": self.keyCancel,
                "green": self.keySatFinder,
                "yellow": self.keyMultiLNB,
                "blue": self.keyHelp,
                "menu": self.keySettings,        # MENU - Settings (jezik itd)
                "info": self.keyLocationEdit,    # INFO/HELP - Location Edit
                "up": self.keyUp,
                "down": self.keyDown,
                "left": self.keyLeft,
                "right": self.keyRight,
            },
            -1
        )

        # ============================================================
        # TIMERI
        # ============================================================
        self.clock_timer = eTimer()
        self.clock_timer.callback.append(self.update_clock)
        self.clock_timer.start(1000)

        self.signal_timer = eTimer()
        self.signal_timer.callback.append(self.update_signal)
        self.signal_timer.start(
            config.plugins.CiefpDishPointer.signal_refresh.value * 1000
        )

        # ============================================================
        # INICIJALNO POPUNJAVANJE
        # ============================================================
        self.update_clock()
        self.refresh_location()
        self.refresh_satellite()
        self.refresh_dish()

        # ============================================================
        # AUTOMATSKA GEOLOKACIJA
        # ============================================================
        if config.plugins.CiefpDishPointer.auto_location.value:
            self.location_thread = LocationThread(self.on_location_ready)
            self.location_thread.start()

        # ============================================================
        # IKONE - na kraju, kada je ekran spreman
        # ============================================================
        self.onLayoutFinish.append(self._load_icons)

    # ============================================================
    # IKONE
    # ============================================================
    def _load_icons(self):
        """Ucitava ikone iz plugin foldera."""
        import os
        from Tools.LoadPixmap import LoadPixmap

        icons = [
            ("plugin_icon", "icon.png"),
            ("dish_icon", "dish.png"),
        ]

        for widget_name, filename in icons:
            path = "%s/%s" % (PLUGIN_PATH, filename)
            if not os.path.exists(path):
                print("[CiefpDishPointer] Ikona ne postoji: %s" % path)
                continue
            try:
                pix = LoadPixmap(path)
                if pix:
                    self[widget_name].instance.setPixmap(pix)
                    print("[CiefpDishPointer] Ucitana ikona: %s" % path)
                else:
                    print("[CiefpDishPointer] LoadPixmap vratio None: %s" % path)
            except Exception as e:
                print("[CiefpDishPointer] Greska pri ucitavanju %s: %s" % (path, e))

    # ============================================================
    # OSVEZAVANJE PRIKAZA
    # ============================================================

    def refresh_location(self):
        """Azurira prikaz lokacije."""
        cfg = config.plugins.CiefpDishPointer
        try:
            lat = float(cfg.latitude.value)
            lon = float(cfg.longitude.value)
        except:
            lat = 0.0
            lon = 0.0

        text = (
            "%s: %s\n"
            "%s: %s\n"
            "%s: %s\n"
            "%s: %.4f\n"
            "%s: %.4f"
        ) % (
            _("continent"), cfg.continent.value,
            _("country"), cfg.country.value,
            _("city"), cfg.city.value,
            _("latitude"), lat,
            _("longitude"), lon,
        )
        self["location_text"].setText(text)

    def refresh_satellite(self):
        """Azurira prikaz izbora sistema."""
        cfg = config.plugins.CiefpDishPointer
        current = cfg.system_type.value

        options = [
            ("all", _("all_satellites")),
            ("motorised", _("motorised")),
            ("multi", _("multi_lnb")),
            ("single", _("single_sat")),
        ]

        lines = []
        for key, label in options:
            mark = "(x)" if key == current else "( )"
            lines.append("%s %s" % (mark, label))

        self["sat_text"].setText("\n".join(lines))

    def refresh_dish(self):
        """Azurira prikaz Dish Setup Data."""
        cfg = config.plugins.CiefpDishPointer
        try:
            lat = float(cfg.latitude.value)
            lon = float(cfg.longitude.value)
        except:
            lat = 0.0
            lon = 0.0

        system = cfg.system_type.value

        if system == "motorised":
            data = calculate_true_south_data(lat, lon)
            text = (
                "%s: %s\n"
                "%s: %.1f°\n"
                "%s: %.1f°\n"
                "%s: %.1f°\n"
                "%s: ---"
            ) % (
                _("true_south"), "",
                _("azimuth_true"), data["azimuth_true"],
                _("azimuth_mag"), data["azimuth_mag"],
                _("declination"), data["declination"],
                _("lnb_skew"),
            )

        elif system == "single":
            sat = self._get_selected_satellite()
            if sat:
                data = calculate_all(lat, lon, sat.position_float)
                text = (
                    "%s: %s\n"
                    "%s: %.1f°\n"
                    "%s: %.1f°\n"
                    "%s: %.1f°\n"
                    "%s: %s"
                ) % (
                    _("nearest_sat"), sat.name,
                    _("azimuth_true"), data["azimuth_true"],
                    _("azimuth_mag"), data["azimuth_mag"],
                    _("dish_elevation"), data["elevation"],
                    _("lnb_skew"), self._format_skew(data["skew"]),
                )
            else:
                text = self._empty_dish_text()

        elif system == "all":
            nearest = find_nearest_satellite(lat, lon, self.satellites)
            if nearest:
                data = calculate_all(lat, lon, nearest.position_float)
                text = (
                    "%s: %s\n"
                    "%s: %.1f°\n"
                    "%s: %.1f°\n"
                    "%s: %.1f°\n"
                    "%s: %s"
                ) % (
                    _("nearest_sat"), nearest.name,
                    _("azimuth_true"), data["azimuth_true"],
                    _("azimuth_mag"), data["azimuth_mag"],
                    _("dish_elevation"), data["elevation"],
                    _("lnb_skew"), self._format_skew(data["skew"]),
                )
            else:
                text = self._empty_dish_text()

        elif system == "multi":
            sat = self._get_selected_satellite()
            if sat:
                data = calculate_all(lat, lon, sat.position_float)
                text = (
                    "%s: %s\n"
                    "%s: %.1f°\n"
                    "%s: %.1f°\n"
                    "%s: %.1f°\n"
                    "%s: %s"
                ) % (
                    _("nearest_sat"), sat.name,
                    _("azimuth_true"), data["azimuth_true"],
                    _("azimuth_mag"), data["azimuth_mag"],
                    _("dish_elevation"), data["elevation"],
                    _("lnb_skew"), self._format_skew(data["skew"]),
                )
            else:
                text = self._empty_dish_text()

        else:
            text = self._empty_dish_text()

        self["dish_text"].setText(text)

    def _empty_dish_text(self):
        return (
            "%s: ---\n"
            "%s: ---\n"
            "%s: ---\n"
            "%s: ---\n"
            "%s: ---"
        ) % (
            _("nearest_sat"),
            _("azimuth_true"),
            _("azimuth_mag"),
            _("dish_elevation"),
            _("lnb_skew"),
        )

    def _format_skew(self, skew):
        if skew >= 0:
            return "%.1f° %s" % (skew, _("right"))
        else:
            return "%.1f° %s" % (abs(skew), _("left"))

    def _get_selected_satellite(self):
        pos = config.plugins.CiefpDishPointer.selected_sat.value
        for sat in self.satellites:
            if sat.position == pos:
                return sat
        if self.satellites:
            try:
                lat = float(config.plugins.CiefpDishPointer.latitude.value or 0)
                lon = float(config.plugins.CiefpDishPointer.longitude.value or 0)
            except:
                lat = 0.0
                lon = 0.0
            return find_nearest_satellite(lat, lon, self.satellites)
        return None

    # ============================================================
    # TIMER CALLBACKS
    # ============================================================

    def update_clock(self):
        import time
        self["clock"].setText(time.strftime("%H:%M\n%d.%m.%Y"))

    def update_signal(self):
        data = get_signal_data(self.session)

        snr = data.get("snr", 0)
        snr_db = data.get("snr_db", 0.0)
        self["snr_bar"].setValue(snr)
        self["snr_percent"].setText("%d%%" % snr)
        self["snr_db"].setText("DB:%.2f" % snr_db)

        agc = data.get("agc", 0)
        self["agc_bar"].setValue(agc)
        self["agc_percent"].setText("%d%%" % agc)

        info = get_current_service_info(self.session)
        sat = get_current_satellite(self.session)
        if info.get("channel"):
            sat_str = ""
            if sat.get("position_float"):
                sat_str = "(%.1f) " % sat["position_float"]
            self["current_service"].setText(
                "%s%s  |  %s" % (
                    sat_str,
                    info.get("channel", ""),
                    info.get("provider", ""),
                )
            )
        else:
            self["current_service"].setText("")

    # ============================================================
    # GEOLOKACIJA
    # ============================================================

    def on_location_ready(self, result):
        if result.get("success"):
            cfg = config.plugins.CiefpDishPointer
            cfg.continent.value = result.get("continent", "Unknown")
            cfg.country.value = result.get("country", "")
            cfg.city.value = result.get("city", "")
            cfg.latitude.value = "%.4f" % result.get("latitude", 0.0)
            cfg.longitude.value = "%.4f" % result.get("longitude", 0.0)
            cfg.save()

            self.refresh_location()
            self.refresh_dish()
        else:
            print("[CiefpDishPointer] Geolokacija nije uspela: %s"
                  % result.get("error", ""))

    # ============================================================
    # PROMENA SISTEMA (strelicama levo/desno)
    # ============================================================

    def keyUp(self):
        pass

    def keyDown(self):
        pass

    def keyLeft(self):
        self._change_system(-1)

    def keyRight(self):
        self._change_system(1)

    def _change_system(self, direction):
        systems = ["all", "motorised", "multi", "single"]
        cfg = config.plugins.CiefpDishPointer
        try:
            idx = systems.index(cfg.system_type.value)
        except ValueError:
            idx = 0

        idx = (idx + direction) % len(systems)
        cfg.system_type.value = systems[idx]
        cfg.system_type.save()

        self.refresh_satellite()
        self.refresh_dish()

    # ============================================================
    # KEY ACTIONS
    # ============================================================
    def keyCancel(self):
        """EXIT - zatvara plugin."""
        if self.location_thread:
            self.location_thread.stop()
        self.close()

    def keyOk(self):
        """OK - nista za sada."""
        pass

    def keySatFinder(self):
        """GREEN - otvara Single Satellite (Sat Finder)."""
        from .screens.satfinder import SatFinderScreen
        self.session.openWithCallback(
            self.on_satfinder_closed,
            SatFinderScreen,
            self.satellites
        )

    def on_satfinder_closed(self, result=None):
        if result:
            config.plugins.CiefpDishPointer.selected_sat.value = result.position
            config.plugins.CiefpDishPointer.system_type.value = "single"
            config.plugins.CiefpDishPointer.system_type.save()
            config.plugins.CiefpDishPointer.selected_sat.save()
        self.refresh_satellite()
        self.refresh_dish()

    def keyMultiLNB(self):
        """YELLOW - otvara Multi LNB."""
        from .screens.multilan import MultiLNBScreen
        try:
            lat = float(config.plugins.CiefpDishPointer.latitude.value)
            lon = float(config.plugins.CiefpDishPointer.longitude.value)
        except:
            lat = 0.0
            lon = 0.0
        self.session.openWithCallback(
            self.on_multilan_closed,
            MultiLNBScreen,
            self.satellites,
            lat,
            lon
        )

    def on_multilan_closed(self, result=None):
        if result:
            config.plugins.CiefpDishPointer.selected_sat.value = result.position
            config.plugins.CiefpDishPointer.system_type.value = "multi"
            config.plugins.CiefpDishPointer.system_type.save()
            config.plugins.CiefpDishPointer.selected_sat.save()
        self.refresh_satellite()
        self.refresh_dish()

    def keyHelp(self):
        """BLUE - otvara slike pomoci."""
        from .screens.help_images import HelpImagesScreen
        self.session.open(HelpImagesScreen)

    def keySettings(self):
        """MENU - otvara Settings ekran."""
        from .screens.settings import SettingsScreen
        self.session.openWithCallback(
            self.on_settings_closed,
            SettingsScreen
        )

    def on_settings_closed(self, result=None):
        """Callback posle zatvaranja Settings."""
        # Osvezi sve labele
        self["title"].setText(_("title"))
        self["location_header"].setText(_("location_info"))
        self["sat_header"].setText(_("satellite_data"))
        self["dish_header"].setText(_("dish_setup"))
        self["btn_exit"].setText(_("exit"))
        self["btn_satfinder"].setText(_("satfinder"))
        self["btn_multi"].setText(_("multi_lnb_btn"))
        self["btn_help"].setText(_("help_images"))
        self["btn_lang"].setText(_("language"))
        self["btn_location"].setText(_("location_edit"))
        self["snr_label"].setText(_("snr"))
        self["agc_label"].setText(_("agc"))

        self.refresh_location()
        self.refresh_satellite()
        self.refresh_dish()

    def keyLocationEdit(self):
        """INFO/HELP - otvara Location Edit."""
        from .screens.location_edit import LocationEditScreen
        self.session.openWithCallback(
            self.on_location_edit_closed,
            LocationEditScreen
        )

    def on_location_edit_closed(self, result=None):
        """Callback posle zatvaranja Location Edit."""
        if result:
            self.refresh_location()
            self.refresh_dish()