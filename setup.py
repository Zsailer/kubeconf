import io
import os
from setuptools import setup, find_packages

# Use README for long description
here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


setup(
    name='kubeconf',
    version='0.0.1',
    author='Zach Sailer',
    author_email='zachsailer@gmail.com',
    description='Lightweight Python module for creating, manipulating, and editing kubeconfig files',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Zsailer/kubeconf',
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)