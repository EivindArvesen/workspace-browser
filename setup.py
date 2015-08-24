#!/usr/bin/env python

import io

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

requirements = read('requirements.txt')

setup(
    name='Raskolnikov',
    version='0.1',
    # version=sandman.__version__,
    description='An experimental web browser',
    author='Eivind Arvesen',
    author_email='eivind.arvesen@gmail.com',
    url='https://github.com/eivind88/raskolnikov',
    install_requires= requirements,
    # install_requires= ['nose'],
    packages=['raskolnikov'],
    test_suite = 'nose.collector',
    # scripts = ['go_foo.py'], # installs as script, must include shebang
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Desktop Environment',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: The BSD 3-Clause License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Communications :: Email',
        'Topic :: Office/Business',
    ],
)
