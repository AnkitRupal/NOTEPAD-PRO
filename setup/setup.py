from distutils.command.build import build
from http.server import executable
import tkinter
from unicodedata import name

from click import option
from pandas import options
import cx_Freeze
import sys
import os
base = None
if sys.platform == 'win32':
    base='Win32GUI'

os.environ['TCL_LIBRARY']=r"C:\Users\Ankit Rupal\AppData\Local\Programs\Python\Python37\tcl\tcl8.6"
os.environ['TK_LIBRARY']=r"C:\Users\Ankit Rupal\AppData\Local\Programs\Python\Python37\tcl\tk8.6"

executables = [cx_Freeze.Executable(
    "notepad_pro.py", base=base, icon="notepad_pro.ico")]

cx_Freeze.setup(
    name= "Notepad Pro",
    options={"build_exe": {"packages": ["tkinter", "os"], "include_files": ["notepad_pro.ico", 'tcl86t.dll','tk86t.dll','icons']}},
    version="0.01",
    description = "Tkinter Application",
    executables=executables
)