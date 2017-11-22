from distutils.core import setup

setup(
    name='sw-excel-parser',
    version='0.0.1',
    packages=['sw_excel_parser'],
    install_requires=[
        'xlrd>=1.1.0',
        'python-dateutil>=2.6.1'
    ],
    test_suite='runtests.runtests',
    url='https://github.com/telminov/sw-excel-parser',
    license='MIT',
    author='Telminov Sergey',
    author_email='sergey@telminov.ru',
    description='Soft Way Microsoft Excel documents parsing package'
)