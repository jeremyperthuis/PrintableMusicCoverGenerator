from cx_Freeze import setup, Executable
import os
#
os.environ['TCL_LIBRARY'] = "C:\\Users\\jpu\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\jpu\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tk8.6"
# build_exe_options = {"include_files": ["tcl86t.dll", "tk86t.dll"]}
base = "Console"

setup(
    name = "simple",
    version = "0.1",
    description = "Ce programme vous dit hello",
    executables = [Executable("Functions.py")]
)