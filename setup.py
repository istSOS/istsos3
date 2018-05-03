import setuptools
from distutils.core import setup

requirements = open('requirements.txt').read().split('\n')

setup(
    name='istsos',
    description='istSOS3 Core Library',
    url='https://github.com/istSOS/istsos3',
    project_urls={
        'Documentation': 'http://istsos.org/en/v3.0.0-Beta',
        'Source': 'https://github.com/istSOS/istsos3',
        'Tracker': 'https://github.com/istSOS/istsos3/issues',
    },
    author='The istSOS Team',
    author_email='geoservice@supsi.ch',
    version='3.0.0b1',
    packages=setuptools.find_packages(),
    install_requires=[x for x in requirements if x],
    package_data={
        'assets': ['istsos/assets'],
    },
    python_requires='>=3, <4',
    license='GNU General Public License v3 (GPLv3)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='istsos ogc sos sensor observation service',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3 :: Only'
    ]
)
