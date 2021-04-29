from setuptools import find_packages
from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='python-mobilitydb',
    packages=find_packages(),
    version='0.1.2',
    license='MIT',
    description='A database adapter to access MobilityDB from Python',
    author='MobilityDB Project',
    platforms=["linux"],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/MobilityDB/MobilityDB-python',
    download_url='',
    install_requires=[
        'asyncpg',
        'psycopg2-binary',
        'Spans',
        'postgis',
        'pytest',
        'python-dateutil',
        'parsec',
        'pytest-asyncio'
    ],
    keywords=['MobilityDB', 'Python'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Database :: Front-Ends',
        'Topic :: Software Development :: Libraries :: Python Modules',
        "Topic :: Scientific/Engineering :: GIS",
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    project_urls={
        'Source': 'https://github.com/MobilityDB/MobilityDB-python',
        'Documentation': 'https://docs.mobilitydb.com/MobilityDB-python/master/python-mobilitydb.pdf',
    },
)
