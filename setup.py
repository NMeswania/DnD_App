###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import glob

from pathlib import Path
from setuptools import setup, find_packages

with open('README.md') as f:
  readme = f.read()

with open('LISENCE') as f:
  license = f.read()

data_dir_str = "dnd_app/data"
data_dir = Path(data_dir_str)

root_dirs = []
for d in data_dir.iterdir():
  dir_category = d.name

  if dir_category == "character":
    for d_ in (data_dir / "character").iterdir():
      character_dir = f"{dir_category}/{d_.name}" 
      root_dirs.append(character_dir)
  
  else:
    root_dirs.append(dir_category)

data_files = []
for root_dir in root_dirs:
  data_file = (f"{data_dir_str}/{root_dir}", [file for file in glob.glob(f"./dnd_app/data/{root_dir}/*.json", recursive=True)])
  data_files.append(data_file)

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
      packages=find_packages(exclude=('tests', 'docs')),
      package_data={
        "": ["*.kv", "*.yaml", "*.json"]
      },
      data_files=data_files
)
