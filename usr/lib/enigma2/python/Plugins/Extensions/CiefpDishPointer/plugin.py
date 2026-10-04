# -*- coding: utf-8 -*-
# CiefpDishPointer - plugin.py
# Verzija: 1.1
# Autor: Ciefp
# Kompatibilno: Python 2 i Python 3

from Plugins.Plugin import PluginDescriptor
from . import __version__

def main(session, **kwargs):
    from .main import CiefpDishPointer
    session.open(CiefpDishPointer)

def Plugins(**kwargs):
    return [
        PluginDescriptor(
            name="CiefpDishPointer",
            description="Dish Pointer - antenna setup helper v%s" % __version__,
            where=PluginDescriptor.WHERE_PLUGINMENU,
            icon="plugin.png",
            fnc=main
        )
    ]