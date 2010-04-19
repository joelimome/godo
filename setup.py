
import os
from setuptools import setup, find_packages

from godo import __version__

README = os.path.join(os.path.dirname(__file__), "README.rst")
DESCRIPTION = open(README).read()

TROVE = """
Development Status :: 4 - Beta
Environment :: Console
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Programming Language :: Python
Topic :: Software Development :: Build Tools
""".strip().splitlines()

ENTRIES="""
[console_scripts]
godo=godo.main:run
"""

setup(
    name="godo",
    version=__version__,
    license="MIT",
    url="http://github.com/davisp/godo.git",

    description="Run some python code in order.",
    long_description=DESCRIPTION,
    
    author="Paul J. Davis",
    author_email="paul.joseph.davis@gmail.com",

    classifiers=TROVE,

    packages=find_packages(exclude=['tests']),
    
    entry_points=ENTRIES
)

