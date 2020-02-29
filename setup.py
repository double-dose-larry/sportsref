from setuptools import setup, find_packages

setup(
   name='sportsref',
   version='0.1.8',
   description='Get sports data from sports-reference.com websites with a pleasant interface',
   author='double_dose_larry',
   author_email='larrydouble33@gmail.com',
   packages=find_packages(),  #same as name
   install_requires=['fuzzywuzzy', 'pandas', 'bs4'], #external packages as dependencies
)