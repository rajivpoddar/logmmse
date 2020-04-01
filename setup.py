from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='logmmse',
    version='1.4',
    description='A python implementation of the LogMMSE speech enhancement/noise reduction alogrithm',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url='https://github.com/wilsonchingg/logmmse',
    packages=['logmmse'],
    author='Rajiv Poddar, Wilson Ching (Fork Author)',
    author_email='wilsonchingg96@gmail.com',
    install_requires=[
        'numpy',
        'scipy',
    ],
)
