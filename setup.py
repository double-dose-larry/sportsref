from setuptools import setup

setup(
   name='py_bref',
   version='0.1.2',
   description='Get baseball data from baseball-reference.com with a pleasant interface',
   author='double_dose_larry',
   author_email='larrydouble33@gmail.com',
   packages=['py_bref'],  #same as name
   install_requires=['fuzzywuzzy', 'pandas'], #external packages as dependencies
)