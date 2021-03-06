from setuptools import setup, find_packages


setup(
    name='renju_DK',
    version='2.1.1',
    description='Renju RL game with computer oppenent',
    url='https://github.com/eldmitro/renjurl',
    author='Dmitriy Kuznetsov',
    author_email='k.d.s.98@mail.ru',
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(exclude=['projection', 'docs']),
    python_requires='>=3.5, <4',
    install_requires=['numpy', 'tensorflow', 'keras'],
    entry_points={  # Optional
        'console_scripts': [
            'renju_DK=renjuRL_DK.renju_game.main:main',
        ],
    },

)
