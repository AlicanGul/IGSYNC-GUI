# a. gul, temmuz 2020
#-----------------------------------------
# IGSYNC-GUI icin build script.
# cx_freeze ile calistirilabilir dosya
# yapmak icin kullanilir.
#-----------------------------------------
# mevcut klasorde komut satirinda:
# python build.py build_exe
# (cxfreeze yuklu olmali)


prg_adi = "IGSYNC-GUI"
prg_main = "igsync.py"

import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["os", "tkinter", "string", "configparser", "dirsync"],
        "include_files": ["ayar.ini"]}

base = "Win32GUI"
setup(name = prg_adi,
    version = "0.1",
    description = prg_adi,
    options = {"build_exe": build_exe_options},
    executables = [Executable(prg_main, base=base)] )
