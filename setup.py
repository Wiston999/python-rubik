from setuptools import setup, find_packages
from os import path
from codecs import open

__author__ = 'Victor Cabezas'

here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

install_reqs = [
    'future==0.16.0',
]

setup(
    name='rubik_solver',
    author='Victor Cabezas',
    author_email='wiston666@gmail.com',
    version='0.2.0',
    description='Rubik solver algorithms',
    long_description=long_description,
    url='https://github.com/Wiston999/python-rubik',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=install_reqs,
    entry_points={
        'console_scripts': [
            'rubik_solver=rubik_solver.utils:main'
        ]
    },
    include_package_data=True,
)
