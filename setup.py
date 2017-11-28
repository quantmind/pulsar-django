#!/usr/bin/env python
import os

from setuptools import setup, find_packages

import pulse


def read(name):
    filename = os.path.join(os.path.dirname(__file__), name)
    with open(filename) as fp:
        return fp.read()


def requirements(name):
    install_requires = []
    dependency_links = []

    for line in read(name).split('\n'):
        if line.startswith('-e '):
            link = line[3:].strip()
            if link == '.':
                continue
            dependency_links.append(link)
            line = link.split('=')[1]
        line = line.strip()
        if line:
            install_requires.append(line)

    return install_requires, dependency_links


meta = dict(
    version=pulse.__version__,
    description=pulse.__doc__,
    name='pulsar-django',
    author='Luca Sbardella',
    author_email="luca@quantmind.com",
    maintainer_email="luca@quantmind.com",
    url="https://github.com/quantmind/pulsar-django",
    license="BSD",
    long_description=read('README.rst'),
    packages=find_packages(include=['pulse', 'pulse.*']),
    include_package_data=True,
    zip_safe=False,
    setup_requires=['pulsar', 'wheel'],
    install_requires=requirements('requirements/hard.txt')[0],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities'
    ]
)


if __name__ == '__main__':
    try:
        from pulsar import cmds
        meta['cmdclass'] = dict(pypi=cmds.PyPi)
    except ImportError:
        pass
    setup(**meta)
