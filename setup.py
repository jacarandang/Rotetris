import sys
from os import path
from cx_Freeze import setup, Executable
import re
# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os", "pygame", "random", "time", "threading", "pickle"], "excludes": ["tkinter"], "include_files": ["config.cfg", "resource"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Rotetris",
        version = "0.1",
        description = "CS 140 Rotetris",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])