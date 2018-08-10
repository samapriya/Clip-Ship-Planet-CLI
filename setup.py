import sys
import os
import sys
import setuptools
from setuptools import find_packages
from setuptools.command.test import test as TestCommand
from distutils.version import StrictVersion
from setuptools import __version__ as setuptools_version

if StrictVersion(setuptools_version) < StrictVersion('38.3.0'):
    raise SystemExit(
        'Your `setuptools` version is old. '
        'Please upgrade setuptools by running `pip install -U setuptools` '
        'and try again.'
    )
def readme():
    with open('README.md') as f:
        return f.read()
setuptools.setup(
    name='pclip',
    version='0.2.7',
    packages={'pclip': ['aoi.json']},
    package_data={'pclip': ['aoi.json']},
    url='https://github.com/samapriya/Clip-Ship-Planet-CLI',
    install_requires=['planet>=1.1.0','psutil>=5.2.2','urllib3>=1.22','requests>=2.18.4','retrying>=1.3.3','pyshp>=1.2.12','progressbar2>=3.34.3',          'pypiwin32; platform_system == "Windows"','pywin32; platform_system == "Windows"'],
    license='Apache 2.0',
    long_description=open('README.rst').read(),
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: GIS',
    ),
    author='Samapriya Roy',
    author_email='samapriya.roy@gmail.com',
    description='Planet Clip-Ship Tools CLI',
    entry_points={
        'console_scripts': [
            'pclip=pclip.pclip:main',
        ],
    },
)
