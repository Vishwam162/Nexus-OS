#!/bin/sh
# NEXUS OS - Dynamic Boot Graphic Launcher

if [ -z "$DISPLAY" ] && [ "$XDG_VTNR" -eq 1 ]; then
    echo "🛸 Launching Nexus Graphics Subsystem..."
    # This turns on the display system and opens your login gate immediately
    exec startx /usr/bin/python3 /usr/share/nexus/nexus_login.py
fi