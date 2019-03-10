from setuptools import setup, find_packages


setup(
    name='renju_DK',
    version='1.1.3',
    description='Renju RL game with computer oppenent',
    url='https://github.com/eldmitro/renjurl',
    author='Dmitriy Kuznetsov',
    author_email='k.d.s.98@mail.ru',
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(exclude=['projection', 'docs']),
    python_requires='>=3.6, <4',
    install_requires=['numpy'],
    entry_points={  # Optional
        'console_scripts': [
            'renju_DK=renjuRL_DK.renju_game.main:main',
        ],
    },

)
