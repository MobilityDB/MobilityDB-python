from setuptools import setup, find_packages
from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='MobilityDB',
    packages=find_packages(),
    version='0.1',
    license='MIT',
    description='MobilityDB Driver',
    author='MobilityDB Team',
    author_email='mobilitydb@ulb.ac.be',
    long_description=long_description,
    url='https://github.com/ULB-CoDE-WIT/MobilityDB-Python',
    download_url='',
    install_requires=[  # I get to this in a second
        'psycopg2-binary',
        'postgis',
        'bdateutil'
    ],
    keywords=['MobilityDB', 'Python'],  # Keywords that define your package best
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
