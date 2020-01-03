from setuptools import setup, find_packages

with open('README.rst', encoding='UTF-8') as f:
    readme = f.read()

setup(
    name='hr',
    version='0.1.0',
    description='Manage users on a server based on an “inventory” JSON file',
    long_description=readme,
    author='nal3x',
    author_email='',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[''],
#    entry_points={
#        'console_scripts': [
#            'pgbackup=pgbackup.cli:main',
#            ]
#        }
)
