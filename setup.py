from setuptools import setup, find_packages

VERSION = '0.1'
DESCRIPTION = 'Finding pairwise rectangles intersections'

setup(
    name="rectinter",
    version=VERSION,
    author="Stanislaw Grodzki",
    author_email="<sg406651@students.mimuw.edu.pl>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['sortedcontainers', 'numba'],
    keywords=['python', 'rectangle', 'intersection'],
    test_suite='tests',
    tests_require=['pytest'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
