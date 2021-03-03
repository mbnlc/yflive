import setuptools

import io
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with io.open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="yflive",
    version="0.0.1",
    description="live yahoo!finance data streamer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Unlicense",
    url='https://github.com/maxBeinlich/yflive.git',
    project_urls={
        "Bug Tracker": "https://github.com/maxBeinlich/yflive/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: The Unlicense",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6"
)