"""
Setup script for EVE Online API Utility Library
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        return f.read()

# Read requirements
def read_requirements():
    with open('requirements.txt') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='eveonline-api-util',
    version='1.0.0',
    author='Dr.Incognito',
    author_email='your-email@example.com',
    description='A comprehensive Python library for EVE Online ESI API integration',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/DrIncognito/EveOnline_API_Util',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Games/Entertainment',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.8',
    install_requires=read_requirements(),
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-mock>=3.7.0',
            'pytest-cov>=4.0.0',
            'responses>=0.20.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
            'mypy>=0.950',
        ],
    },
    entry_points={
        'console_scripts': [
            'eve-api-util=eveonline_api_util.cli:main',
        ],
    },
    keywords=['eve online', 'esi', 'api', 'oauth2', 'gaming'],
    project_urls={
        'Bug Reports': 'https://github.com/DrIncognito/EveOnline_API_Util/issues',
        'Source': 'https://github.com/DrIncognito/EveOnline_API_Util',
        'Documentation': 'https://github.com/DrIncognito/EveOnline_API_Util#readme',
    },
)
