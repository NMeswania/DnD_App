###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from setuptools import setup, find_packages

with open('README.md') as f:
  readme = f.read()

with open('LISENCE') as f:
  license = f.read()

setup(name='dnd_app',
      version='0.0.0',
      entry_points={
          'console_scripts': ['dnd_app = dnd_app.main:main',],
      },
      description='D&D app to manage character sheets',
      long_description=readme,
      author='Neal Meswania',
      url='https://github.com/NMeswania/DnD_App',
      license=license,
      packages=find_packages(exclude=('tests', 'docs')))
