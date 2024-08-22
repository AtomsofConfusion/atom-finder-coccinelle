from setuptools import setup
  
setup( 
    name='atom-finder-coccinelle', 
    version='0.0.1', 
    description='An utility to find atoms of confusion via coccinelle', 
    author='Austin Huang', 
    author_email='im@austinhuang.me', 
    packages=['.'], 
    include_package_data=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'atom-finder-coccinelle = main:cli',
        ],
    },
) 
