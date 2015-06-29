# cx-Freeze setup file

from cx_Freeze import setup, Executable

base = None
executables = [
    Executable('main.py', base=base)
]

setup(name='Animal Master',
      version='0.1',
      description='Game where a user can manage pets.',
      executables=executables
      )
