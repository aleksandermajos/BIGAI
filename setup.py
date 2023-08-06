from setuptools import find_packages, setup

setup(
   name='BIGAI',
   version='0.0.7',
   author='Aleksander Majos',
   author_email='aleksander.majos@gmail.com',
   packages=find_packages(),
   include_package_data=True,
   zip_safe=False,
   download_url='https://github.com/aleksandermajos/BIGAI',
   license='LICENSE.txt',
   description='An AI Library as a Baseline to create AI Projects',
   #long_description=open('README.md').read(),
   install_requires=[],
)