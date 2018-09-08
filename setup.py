from distutils.core import setup

setup(
    name='logmmse',
    version='1.0',
    description='A python implementation of the LogMMSE speech enhancement/noise reduction alogrithm',
    license='MIT',
    url='https://github.com/wilsonchingg/logmmse',
    packages=['logmmse'],
    author=['Rajiv Poddar, Wilson Ching (Fork Author)'],
    author_email=['wilsonchingg96@gmail.com'],
    install_requires=[
        'numpy',
        'scipy',
    ],
)
