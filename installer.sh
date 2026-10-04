#!/bin/bash
##setup command=wget -q "--no-check-certificate" https://raw.githubusercontent.com/ciefp/CiefpDishPointer/main/installer.sh -O - | /bin/sh

######### Only This 2 lines to edit with new version ######
version='1.1'
changelog='\nInitial release\nAutomatic geolocation via IP\n4 modes: All / Motorised / Multi LNB / Single\nCalculations: azimuth, elevation, LNB skew, declination\nSingle Satellite screen\nMulti LNB setup with checkbox list\nHelp Images with visual explanations\nReal-time signal (SNR/AGC/DB)\nSerbian and English language'
##############################################################

# Check if we should skip restart (for batch installations)
SKIP_REBOOT="${SKIP_REBOOT:-0}"

TMPPATH=/tmp/CiefpDishPointer

if [ ! -d /usr/lib64 ]; then
    PLUGINPATH=/usr/lib/enigma2/python/Plugins/Extensions/CiefpDishPointer
else
    PLUGINPATH=/usr/lib64/enigma2/python/Plugins/Extensions/CiefpDishPointer
fi

# Check depends packages
if [ -f /var/lib/dpkg/status ]; then
   STATUS=/var/lib/dpkg/status
   OSTYPE=DreamOs
else
   STATUS=/var/lib/opkg/status
   OSTYPE=Dream
fi

echo ""
if python --version 2>&1 | grep -q '^Python 3\.'; then
    echo "You have Python3 image"
    PYTHON=PY3
else
    echo "You have Python2 image"
    PYTHON=PY2
fi
echo ""

## Remove tmp directory
[ -d $TMPPATH ] && rm -rf $TMPPATH > /dev/null 2>&1

## Remove old plugin directory
[ -d $PLUGINPATH ] && rm -rf $PLUGINPATH

# Download and install plugin
mkdir -p $TMPPATH
cd $TMPPATH
set -e

if [ -f /var/lib/dpkg/status ]; then
   echo "# Your image is OE2.5/2.6 #"
   echo ""
else
   echo "# Your image is OE2.0 #"
   echo ""
fi

# Download latest release
wget --no-check-certificate https://github.com/ciefp/CiefpDishPointer/archive/refs/heads/main.tar.gz
tar -xzf main.tar.gz

# Copy files to correct location
if [ -d "CiefpDishPointer-main/usr" ]; then
    cp -r 'CiefpDishPointer-main/usr' '/'
else
    # Fallback: flat structure
    echo "Using flat structure..."
    mkdir -p $PLUGINPATH
    cp -r CiefpDishPointer-main/* $PLUGINPATH/
fi

set +e
cd
sleep 2

### Check if plugin installed correctly
if [ ! -d $PLUGINPATH ]; then
    echo "Something wrong .. Plugin not installed"
    exit 1
fi

# Provera glavnih fajlova
if [ ! -f "$PLUGINPATH/plugin.py" ]; then
    echo "ERROR: plugin.py not found!"
    exit 1
fi

if [ ! -f "$PLUGINPATH/main.py" ]; then
    echo "ERROR: main.py not found!"
    exit 1
fi

if [ ! -d "$PLUGINPATH/core" ]; then
    echo "ERROR: core folder not found!"
    exit 1
fi

if [ ! -d "$PLUGINPATH/screens" ]; then
    echo "ERROR: screens folder not found!"
    exit 1
fi

if [ ! -d "$PLUGINPATH/images" ]; then
    echo "WARNING: images folder not found (help images may not work)"
fi

rm -rf $TMPPATH > /dev/null 2>&1
sync
echo ""
echo ""
echo "#########################################################"
echo "#      CiefpDishPointer v$version INSTALLED             #"
echo "#                  developed by ciefp                   #"
echo "#                  .::CiefpSettings::.                  #"
echo "#               https://github.com/ciefp                #"
echo "#########################################################"

# Only restart if SKIP_REBOOT is not set to 1
if [ "$SKIP_REBOOT" = "0" ]; then
    echo "#           your Device will RESTART Now                #"
    echo "#########################################################"
    sleep 5
    killall -9 enigma2
else
    echo "#        Restart skipped (batch installation)           #"
    echo "#########################################################"
fi

exit 0