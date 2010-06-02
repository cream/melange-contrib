from distutils.core import setup

setup(
    name = 'Melange Contrib Libraries',
    version = '0.1',
    package_dir = {'cream.contrib.melange': 'melange'},
    packages = ['cream.contrib.melange'],
    package_data={'cream.contrib.melange': ['interface.glade']}
    )
