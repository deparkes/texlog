from __future__ import absolute_import
from __future__ import print_function

from setuptools import setup
from setuptools import find_packages

setup(name='texlog',
      version='0.3.0',
      description='Log the wordcount of tex files',
      url='https://github.com/deparkes/texcount',
      author='deparkes',
      author_email='deparkes@deparkes.co.uk',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},  # Specifies that the 'root' directory for the build is 'src'
      zip_safe=True)
