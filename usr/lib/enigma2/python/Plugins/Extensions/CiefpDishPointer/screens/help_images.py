# -*- coding: utf-8 -*-
# CiefpDishPointer - screens/help_images.py
# Verzija: 1.1
# Autor: Ciefp
# Kompatibilno: Python 2 i Python 3

import os
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.Label import Label
from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Components.Pixmap import Pixmap
from Tools.LoadPixmap import LoadPixmap

from ..core.config import _


PLUGIN_PATH = "/usr/lib/enigma2/python/Plugins/Extensions/CiefpDishPointer"
IMAGES_PATH = "%s/images" % PLUGIN_PATH


# ============================================================
# LISTA TEMA
# ============================================================
# Format: (key, topic_label_key, help_text_key, filename)

HELP_ITEMS = [
    ("elevacija", "help_topic_elevacija", "help_elevacija", "elevacija.png"),
    ("azimut", "help_topic_azimut", "help_azimut", "azimut.png"),
    ("deklinacija", "help_topic_deklinacija", "help_deklinacija", "deklinacija.png"),
    ("lnb_skew", "help_topic_lnb_skew", "help_lnb_skew", "lnb_skew.png"),
    ("true_south", "help_topic_true_south", "help_true_south", "true_south.png"),
    ("motor_setup", "help_topic_motor_setup", "help_motor_setup", "motor_setup.png"),
]


# ============================================================
# GLAVNI EKRAN - LISTA TEMA
# ============================================================

class HelpImagesScreen(Screen):
    skin = """
        <screen name="HelpImagesScreen" position="center,center" size="1400,900" 
                title="Help" backgroundColor="#001020" flags="wfNoBorder">
            
            <eLabel position="0,0" size="1400,60" backgroundColor="#004000" zPosition="1"/>
            <widget name="title" position="0,0" size="1400,60" 
                    font="Regular;34" foregroundColor="#ffffff" 
                    halign="center" valign="center" transparent="1" zPosition="2"/>
            
            <eLabel position="20,80" size="660,780" 
                    backgroundColor="#001830" zPosition="1"/>
            
            <widget name="topic_list" position="30,90" size="640,760" 
                    itemHeight="60"
                    font="Regular;30" foregroundColor="#ffffff" 
                    transparent="1" zPosition="2"/>
            
            <eLabel position="700,80" size="680,780" 
                    backgroundColor="#001830" zPosition="1"/>
            
            <widget name="info_header" position="720,100" size="640,50" 
                    font="Regular;30" foregroundColor="#ffff00" 
                    halign="left" valign="center" transparent="1" zPosition="2"/>
            
            <widget name="info_text" position="720,170" size="640,650" 
                    font="Regular;26" foregroundColor="#ffffff" 
                    halign="left" valign="top" transparent="1" zPosition="2"/>
            
            <widget name="hint" position="720,800" size="640,50" 
                    font="Regular;22" foregroundColor="#aaaaaa" 
                    halign="center" valign="center" transparent="1" zPosition="2"/>
        </screen>
    """

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session

        # ============================================================
        # WIDGETI
        # ============================================================
        self["title"] = Label(_("help_title"))
        self["topic_list"] = MenuList([])
        self["info_header"] = Label("")
        self["info_text"] = Label("")
        self["hint"] = Label("OK = prikazi sliku | EXIT = nazad")

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

        self.onLayoutFinish.append(self._update_info)

    # ============================================================
    # LISTA
    # ============================================================

    def _build_list(self):
        """Popunjava listu tema."""
        items = []
        for key, topic_key, help_key, filename in HELP_ITEMS:
            items.append(_(topic_key))
        self["topic_list"].setList(items)

    def _get_current_topic(self):
        """Vraca trenutno selektovanu temu."""
        try:
            idx = self["topic_list"].getSelectedIndex()
            if 0 <= idx < len(HELP_ITEMS):
                return HELP_ITEMS[idx]
        except:
            pass
        return None

    # ============================================================
    # INFO PANEL
    # ============================================================

    def _update_info(self):
        """Azurira desni panel sa tekstualnim objasnjenjem."""
        topic = self._get_current_topic()
        if not topic:
            self["info_header"].setText("")
            self["info_text"].setText("")
            return

        key, topic_key, help_key, filename = topic
        self["info_header"].setText(_(topic_key))
        self["info_text"].setText(_(help_key))

    # ============================================================
    # KEY ACTIONS
    # ============================================================

    def keyUp(self):
        try:
            self["topic_list"].up()
        except:
            pass
        self._update_info()

    def keyDown(self):
        try:
            self["topic_list"].down()
        except:
            pass
        self._update_info()

    def keyOk(self):
        """OK - otvara sliku za izabranu temu."""
        topic = self._get_current_topic()
        if not topic:
            return

        # 4 elementa: key, topic_key, help_key, filename
        key, topic_key, help_key, filename = topic
        image_path = "%s/%s" % (IMAGES_PATH, filename)

        if not os.path.exists(image_path):
            self.session.open(
                MessageBox,
                "Slika nije pronadjena:\n%s" % filename,
                MessageBox.TYPE_INFO,
                timeout=3
            )
            return

        self.session.open(
            HelpImageDetailScreen,
            image_path,
            _(help_key)
        )

    def keyCancel(self):
        """EXIT - zatvori ekran."""
        self.close()


# ============================================================
# EKRAN ZA PRIKAZ SLIKE
# ============================================================

class HelpImageDetailScreen(Screen):
    skin = """
        <screen name="HelpImageDetailScreen" position="center,center" size="1600,950" 
                title="Help" backgroundColor="#001020" flags="wfNoBorder">
            
            <eLabel position="0,0" size="1600,60" backgroundColor="#004000" zPosition="1"/>
            <widget name="title" position="0,0" size="1600,60" 
                    font="Regular;34" foregroundColor="#ffffff" 
                    halign="center" valign="center" transparent="1" zPosition="2"/>
            
            <!-- Slika - leva strana -->
            <eLabel position="20,80" size="950,850" 
                    backgroundColor="#001830" zPosition="1"/>
            <widget name="image" position="30,90" size="930,830" 
                    alphatest="blend" zPosition="2"/>
            
            <!-- Tekst - desna strana -->
            <eLabel position="990,80" size="590,850" 
                    backgroundColor="#001830" zPosition="1"/>
            <widget name="text" position="1010,100" size="550,810" 
                    font="Regular;26" foregroundColor="#ffffff" 
                    halign="left" valign="top" transparent="1" zPosition="2"/>
            
            <widget name="hint" position="990,900" size="590,40" 
                    font="Regular;22" foregroundColor="#aaaaaa" 
                    halign="center" valign="center" transparent="1" zPosition="2"/>
        </screen>
    """

    def __init__(self, session, image_path, text):
        Screen.__init__(self, session)
        self.session = session

        self["title"] = Label(_("help_title"))
        self["image"] = Pixmap()
        self["text"] = Label(text)
        self["hint"] = Label("EXIT = nazad")

        self.image_path = image_path

        self["actions"] = ActionMap(
            ["OkCancelActions", "DirectionActions"],
            {
                "cancel": self.close,
                "ok": self.close,
                "left": self.close,
                "right": self.close,
            },
            -1
        )

        self.onLayoutFinish.append(self._load_image)

    def _load_image(self):
        """Ucitava sliku."""
        try:
            pix = LoadPixmap(self.image_path)
            if pix:
                self["image"].instance.setPixmap(pix)
            else:
                self["text"].setText("Slika nije mogla da se ucita:\n%s" % self.image_path)
        except Exception as e:
            self["text"].setText("Greska: %s" % e)