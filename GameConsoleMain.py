# -*- coding: utf-8 -*-
import os
from sys import platform



try:
    import toga
except:
    print("You'd better install the libraries of BeeWare\nNow, we're helping you with this.")
    from src.oddevenmatrix.oemsup.bugReporter import version
    version.installLibraries(version)


if platform == 'win32':
    os.system("python ./src/oddevenmatrix/GameConsoleMain.py")
elif platform == 'linux':
    os.system("python3 ./src/oddevenmatrix/GameConsoleMain.py")
