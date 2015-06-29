# py2app setup file

from cx_Freeze import setup, Executable

included_files = ['animals/']

setup(name='Animal Master',
      version='0.1',
      description='Game where a user can manage pets.',
      executables=[Executable('main.py', base=None)],
      options={'build_exe': {'include_files': included_files,
                             'packages': ['os']},
               'bdist_mac': {'iconfile': 'icon.icns',
                            'bundle_name': 'Animal Master'}
               }
      )
