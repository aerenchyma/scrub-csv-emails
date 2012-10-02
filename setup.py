try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'A script to scrub a list of emails and names (CSV)'
    'author': 'Brian Dant',
    'url': 'git@github.com:briandant/scrub-csv-emails.git',
    'download_url': 'git@github.com:briandant/scrub-csv-emails.git',
    'author_email': 'brian.r.dant@gmail.com',
    'version': 'pre-release',
    'install_requires': ['nose'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'scrub-csv-emails'
}

setup(**config)
