import os
import codecs
from setuptools import setup

def read(fname):
    return codecs.open(
        os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()

README = read('README.rst')

setup(
    name = "django-fuzzydt",
    version = "0.1a1",
    url = 'https://github.com/idangazit/django-fuzzydt',
    license = 'BSD',
    description = '"Fuzzy" datetime parsing app for django including form fields/widgets',
    long_description = README,
    author = 'Idan Gazit',
    author_email = 'idan@pixane.com',
    packages = ['fuzzydt'],
    package_data = {
        'fuzzydt': ['static/fuzzydt/*/*'],
    },
    install_requires=['parsedatetime'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    zip_safe = False,
)
