from setuptools import setup, find_packages

VERSION = '0.1.1'
DESCRIPTION = ''
with open('README.md') as readme:
    LONG_DESCRIPTION = readme.read()

# Setting up
setup(
    name='monota',
    version=VERSION,
    author='Kilthunox',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
    ],
    keywords=['python', 'websockets', 'server'],
    classifiers=[
        'Programming Language :: Python :: 3',
    ]
)



