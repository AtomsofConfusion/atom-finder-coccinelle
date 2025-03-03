from setuptools import setup

with open("README.md", "r") as f:
    info = f.read()

setup(
    name="atom-finder-coccinelle",
    version="0.1.0",
    description="An utility to find atoms of confusion via coccinelle",
    author="The Atoms of Confusion Project",
    packages=["src"],
    include_package_data=True,
    install_requires=["click", "pytest"],
    extras_require={
        "selenium": [
            "selenium>=4.0.0",
            "webdriver-manager>=3.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "aoc-cocci = src.tools.aoc_cocci:atom_finder",
        ],
    },
)
