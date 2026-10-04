# -*- coding: utf-8 -*-
# CiefpDishPointer - __init__.py
# Verzija: 1.0
# Autor: Ciefp
# Kompatibilno: Python 2 i Python 3

from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
import gettext

PluginLanguageDomain = "CiefpDishPointer"
PluginLanguagePath = "Extensions/CiefpDishPointer/locale"

def localeInit():
    gettext.bindtextdomain(
        PluginLanguageDomain,
        resolveFilename(SCOPE_PLUGINS, PluginLanguagePath)
    )

def _(txt):
    t = gettext.dgettext(PluginLanguageDomain, txt)
    if t == txt:
        t = gettext.gettext(txt)
    return t

localeInit()
language.addCallback(localeInit)