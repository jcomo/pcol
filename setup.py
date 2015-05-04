from setuptools import setup, find_packages

setup(
    name = 'pcol',
    version = '0.1.1',
    description = "A straightforward color rendering library for Python",
    url = 'https://github.com/jcomo/pcol',
    author = 'Jonathan Como',
    author_email = 'jonathan.como@gmail.com',
    py_modules = ['pcol'],
    packages = find_packages(exclude=['docs', 'tests']),
    install_requires = [],
    classifiers = [
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],
    keywords = 'console terminal color tree'
)
