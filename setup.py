from setuptools import setup

setup(
    name='CoVID-19_GreyHounds',
    packages=['application'],
    include_package_data=True,
    install_requires=[
        'flask',
        'requests',
        'beautifulsoup4',
        'openpyxl',
    ],
)

