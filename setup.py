from setuptools import setup

setup(
    name = 'Melange Contrib Libraries',
    version = '0.1',
    package_dir = {'cream.contrib.melange': 'melange'},
    packages = ['cream.contrib.melange'],
    include_package_data = True,
    package_data={'cream.contrib.melange': ['interface.glade']}
    )
