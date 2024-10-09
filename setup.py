from setuptools import setup, find_packages
  
with open("README.md", 'r') as f:
    info = f.read()

def s1():
    pass

def s2():
    pass

setup( 
    name='atom-finder-coccinelle', 
    version='0.1.2', 
    description='An utility to find atoms of confusion via coccinelle', 
    author='', 
    author_email='', 
    packages=['src', 'test'],
    include_package_data=True,
    install_requires=['pandas'],
    entry_points={
        'console_scripts': [
            "atom-finder-coccinelle = src.main:cli",
            "atom-finder-coccinelle-tests = tests.run_tests:main",
        ],
    },
    # add scripts for global path

) 
