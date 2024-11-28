from setuptools import setup
  
with open("README.md", 'r') as f:
    info = f.read()

setup( 
    name='atom-finder-coccinelle', 
    version='0.1.0', 
    description='An utility to find atoms of confusion via coccinelle', 
    author='The Atoms of Confusion Project', 
    packages=['src', 'tests'],
    include_package_data=True,
    install_requires=['pandas', 'click', 'pytest'],
    entry_points={
        'console_scripts': [
            "aoc-coccinelle = src.main:cli",
        ],
    },

) 
