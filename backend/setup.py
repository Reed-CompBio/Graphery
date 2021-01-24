import setuptools


def read_file(filename):
    with open(filename) as file:
        return file.read()


long_description = 'This is a the backend of Graphery. It includes a Django server ' \
                   'and a user server. '

setuptools.setup(
    name="Graphery Servers",
    version="0.25.3",
    packages=setuptools.find_packages(exclude=['tests*']),
    install_requires=read_file('requirements.txt'),
    author="Heyuan Zeng",
    author_email="zengl@reed.edu",
    description="Backend of Graphery",
    long_description=long_description,
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
