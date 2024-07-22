from setuptools import setup, find_packages
from typing import List

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()     
   

setup(
    name='VR Therapy',
    version='0.0.1',
    author='cyril',
    author_email='cyriljosecky@gmail.com',
    install_requires=["scikit-learn","pandas","numpy"],
    packages=find_packages()
)