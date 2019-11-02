from setuptools import setup, find_packages

setup(name='file_name_extraction',
      version='1.0',
      description='Python Distribution Utilities',
      author='Victor Sowa',
      author_email='victor.johan.sowa@gmail.com',
      install_requires=['pandas>=0.25.3'],
      python_requires='>=3.6',
      packages=find_packages())
