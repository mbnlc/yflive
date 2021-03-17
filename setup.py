import setuptools

import io
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with io.open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="yflive",
    version="0.1.0",
    description="live Yahoo! Finance data streamer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Max Beinlich",
    author_email="maxbeinlich@gmail.com",
    license="Unlicense",
    url='https://github.com/maxBeinlich/yflive.git',
    download_url='https://github.com/maxBeinlich/yflive/releases',
    project_urls={
        "Source": "https://github.com/maxBeinlich/yflive",
        "Bug Tracker": "https://github.com/maxBeinlich/yflive/issues",
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: The Unlicense",
        "Operating System :: OS Independent",
        "Topic :: Internet",
        "Topic :: Finance",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ],
    install_requires=["websocket-client"],
    packages=setuptools.find_packages(exclude="tests"),
    include_package_data=True,
    python_requires=">=3.6"
)