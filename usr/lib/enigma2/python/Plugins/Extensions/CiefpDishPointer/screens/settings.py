# -*- coding: utf-8 -*-
# CiefpDishPointer - screens/settings.py
# Verzija: 1.0

from Screens.Screen import Screen
from Screens.Setup import Setup
from Components.ActionMap import ActionMap
from Components.config import config, getConfigListEntry
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.Button import Button


class SettingsScreen(ConfigListScreen, Screen):
    skin = """
        <screen name="SettingsScreen" position="center,center" size="1000,700" 
                title="Settings" backgroundColor="#001020">
            <widget name="config" position="20,20" size="960,600" 
                    scrollbarMode="showOnDemand" transparent="1"/>
            <widget name="key_red" position="20,640" size="300,40" 
                    backgroundColor="red" font="Regular;24" 
                    foregroundColor="#ffffff" halign="center" valign="center"/>
            <widget name="key_green" position="340,640" size="300,40" 
                    backgroundColor="green" font="Regular;24" 
                    foregroundColor="#ffffff" halign="center" valign="center"/>
        </screen>
    """

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session

        cfg = config.plugins.CiefpDishPointer

        list = [
            getConfigListEntry("Language", cfg.language),
            getConfigListEntry("Auto Location", cfg.auto_location),
            getConfigListEntry("Signal Refresh (s)", cfg.signal_refresh),
            getConfigListEntry("City", cfg.city),
            getConfigListEntry("Country", cfg.country),
            getConfigListEntry("Latitude", cfg.latitude),
            getConfigListEntry("Longitude", cfg.longitude),
        ]

        ConfigListScreen.__init__(self, list)

        self["key_red"] = Button("Cancel")
        self["key_green"] = Button("Save")

        self["actions"] = ActionMap(
            ["SetupActions", "ColorActions"],
            {
                "cancel": self.keyCancel,
                "red": self.keyCancel,
                "green": self.keySave,
                "ok": self.keySave,
            },
            -1
        )

    def keySave(self):
        for x in self["config"].list:
            x[1].save()
        self.close(True)

    def keyCancel(self):
        for x in self["config"].list:
            x[1].cancel()
        self.close(False)