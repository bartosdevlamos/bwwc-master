from setuptools import setup, find_packages

setup(
    name='baabs_wide_web_crawler',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'openpyxl',
    ],
    entry_points={
        'console_scripts': [
            'bwwc-master=main:main',
        ],
    },
)