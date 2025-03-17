from setuptools import setup, find_packages
from mkdata.cli import __version__ as version

long_description = open("README.md").read()
long_description = long_description[long_description.index('#'):]   # the logo does not render on the PyPI website

setup(
    name="mkdata",
    version=version,
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "mkdata=mkdata.cli:main",
        ],
    },
    author="RayZh",
    author_email="rayzhangshanghai@hotmail.com",
    description="Simple but powerful batch data generator based on Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RayZh-hs/mkdata",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)