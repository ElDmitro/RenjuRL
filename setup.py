"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='renjuAI_DK',
    version='1.0.2',
    description='Renju RL game with computer oppenent',
    url='https://github.com/eldmitro/renjurl',
    author='Dmitriy Kuznetsov',
    author_email='k.d.s.98@mail.ru',
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(exclude=['projection']),
    python_requires='>=3.7, <4',
    install_requires=['numpy'],
    entry_points={  # Optional
        'console_scripts': [
            'renjuRL_DK=renju_game.main:main',
        ],
    },

)
