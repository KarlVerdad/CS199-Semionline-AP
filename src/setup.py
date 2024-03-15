from setuptools import setup

setup(
   name='oapmla',
   version='1.0',
   description='Online Assignment Problem with ML Advice',
   author='KASILAG-Rey',
   author_email='crkasilag@up.edu.ph',
   packages=['oapmla'],  #same as name
   install_requires=['networkx', 'numpy'], #external packages as dependencies
)