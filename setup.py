import glob
import os
import sys
from setuptools import find_packages, setup


additional_files = []
for filename in glob.iglob('./py4macro/**', recursive=True):
    additional_files.append(filename.replace('./py4macro/', ''))


setup(
    name='py4macro',
    version='0.1.0',
    author='Tetsu Haruyama',
    author_email='haruyama@econ.kobe-u.ac.jp',
    packages=find_packages(),
    package_dir={'py4macro': './py4macro'},
    include_package_data=True,
    package_data={'py4macro': additional_files},
    install_requires=['pandas','statsmodels'],
    url='https://github.com/spring-haru/py4macro',
    license='LICENSE',
    description='Python package containing Penn World Table, IMF World Economic Outlook and Maddison Project datasets.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords=['data', 'Penn World Table', 'IMF World Economic Outlook', 'Maddison Project', 'Hodrick-Prescott filter']
)
