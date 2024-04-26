#
# Mario Torre - 03/27/2024 
#
from setuptools import setup, find_packages 

setup(
    name='hcc2sdk',
    version='0.1.0',
    packages=find_packages(),
    license='SENSIA',
    description='SDK API for HCC2',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https/bitbucket.com/sensiaglobal/hcc2-sdk-python-api.git',
    author='Mario Torre',
    author_email='mario.torre@sensiaglobal.com',
)
