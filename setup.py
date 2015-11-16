# coding: utf-8
__author__ = 'Héctor Vela'

from setuptools import setup, find_packages

setup(
    name="django-plupload",
    version="0.5",
    description="""
django-plupload is a barebones multi file upload app for django.
Uses plupload""",
    long_description=open('README.md').read(),
    author="Héctor Vela",
    author_email="vellonce@gmail.com",
    url="",
    license="GPLv2",
    packages=find_packages(),
    include_package_data=True,
    install_requires=['django'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "License :: OSI Approved :: BSD License",
        'Topic :: Software Development :: Libraries :: Python Modules ',
        ],
    zip_safe=False,
)
