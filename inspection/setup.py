from setuptools import setup, find_packages
import os

setup(
    name="inspection",
    version=os.environ["VERSION"],
    description='Vision packages for robotic inspection task',
    author='Leonardo Edgar',
    author_email='leonardo_edgar98@outlook.com',
    package_dir={'': 'src'},
    packages=find_packages(where='src')
)
