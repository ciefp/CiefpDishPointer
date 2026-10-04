# -*- coding: utf-8 -*-
# CiefpDishPointer - plugin.py
# Verzija: 1.1
# Autor: Ciefp
# Kompatibilno: Python 2 i Python 3

from Plugins.Plugin import PluginDescriptor

def main(session, **kwargs):
    from .main import CiefpDishPointer
    session.open(CiefpDishPointer)

def Plugins(**kwargs):
    return [
        PluginDescriptor(
            name="CiefpDishPointer",
            description="Dish Pointer - Help with antenna adjustment v1.2",
            where=PluginDescriptor.WHERE_PLUGINMENU,
            icon="plugin.png",
            fnc=main
        )
    ]