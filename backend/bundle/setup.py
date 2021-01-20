import os

import setuptools


def read_file(filename):
    base_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_path, filename)) as file:
        return file.read()


setuptools.setup(
    name="bundle",
    version="0.2.5",
    packages=setuptools.find_packages(exclude=['tests*']),
    author="Heyuan Zeng",
    author_email="zengl@reed.edu",
    description="Utilities for local server",
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/FlickerSoul/Graphery",
    project_urls={
        "Bug Tracker": "https://github.com/FlickerSoul/Graphery/issues",
        "Documentation": "http://docs.graphery.reedcompbio.org",
        "Source Code": "https://github.com/FlickerSoul/Graphery",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
