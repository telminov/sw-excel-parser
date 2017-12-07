# python setup.py sdist register bdist_egg upload
from setuptools import setup
from sw_excel_parser import __version__

setup(
    name='sw-excel-parser',
    version=__version__,
    packages=['sw_excel_parser', ],
    install_requires=[
        'xlrd>=1.1.0',
        'python-dateutil>=2.6.1',
    ],
    tests_require=[
        'coverage',
        'coveralls',
        'nose',
    ],
    test_suite='nose.collector',
    url='https://github.com/telminov/sw-excel-parser',
    license='MIT',
    author='Telminov Sergey',
    author_email='sergey@telminov.ru',
    description='Soft Way Microsoft Excel documents parsing package'
)
