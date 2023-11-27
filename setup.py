import sys
import setuptools
from pturlparser._version import __version__

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 10)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    print(f"Unsupported Python version! This version of pturlparser requires at least Python {REQUIRED_PYTHON} but you are trying to install it on Python {CURRENT_PYTHON}. To resolve this, consider upgrading to a supported Python version.")
    sys.exit(1)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pturlparser",
    description="Tool for extracting URLs from HTML and JavaScript",
    url="https://www.penterep.com/",
    author="Penterep",
    author_email="info@penterep.com",
    version=__version__,
    license="GPLv3+",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Environment :: Console",
        "Topic :: Security", 
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"
    ],
    python_requires='>=3.10.0',
    install_requires=[
        "ptlibs>=0.0.6",
        "requests>=2.27.1",
        "validators>=0.18.2",
        "impacket>=0.9.24"
        "DOPLNIT... bude tu to stejne co v requirements"
        "TO CO TU JE SE POTOM SMAZE A PRED ODEVZDANIM"
        "PROJEKTU SE TU DAJI KNIHOVNY CO JSOU OPRAVDU"
        "POTREBA. ZATIM TO ALE NECHME TAK JAK TO JE"
    ],
    entry_points = {
        'console_scripts': [
            'pturlparser = pturlparser.pturlparser:main'
        ]
    },
    include_package_data = True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls = {
        "Source": "https://github.com/W41do/pturlparser",
    }
)