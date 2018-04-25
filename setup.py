import cx_Freeze
import os

os.environ['TCL_LIBRARY'] = r'C:\Users\USER\Anaconda3\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\USER\Anaconda3\tcl\tk8.6'

executables = [cx_Freeze.Executable("snakeVSBlocks.py")]

cx_Freeze.setup(
    name="A bit Racey",
    options={"build_exe": {"packages":["pygame"]}},
    executables = executables

    )