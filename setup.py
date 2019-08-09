from setuptools import setup, find_packages

setup(name='texlog',
      version='0.3.0',
      description='Log the wordcount of tex files',
      url='https://github.com/deparkes/texcount',
      author='deparkes',
      author_email='deparkes@deparkes.co.uk',
      license='GPL',
      packages=find_packages(exclude=['tests', 'dist']),
      tests_require=['pytest', 'pytest-cov'],
      zip_safe=True)
