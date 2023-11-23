import glob
from setuptools import find_packages, setup


additional_files = []
for filename in glob.iglob('./py4macro/**', recursive=True):
    additional_files.append(filename.replace('./py4macro/', ''))


setup(
    name='py4macro',
    version='0.8.7',
    author='Tetsu Haruyama',
    author_email='haruyama@econ.kobe-u.ac.jp',
    packages=find_packages(exclude=("data_generation",)),
    package_dir={'py4macro': './py4macro'},
    include_package_data=True,
    package_data={'py4macro': additional_files},
    install_requires=['pandas'],
    url='https://github.com/Py4Macro/py4macro',
    license='MIT',
    description='A module for py4macro.github.io',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords=['data', 'Penn World Table', 'IMF World Economic Outlook', 'Maddison Project', 'Hodrick-Prescott filter', 'Japan']
)
