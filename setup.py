import setuptools

import io
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with io.open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="yflive",
    version="0.1.5-dev0",
    description="live Yahoo! Finance data streamer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Max Beinlich",
    author_email="maxbeinlich@gmail.com",
    license="Apache",
    url='https://github.com/mbnlc/yflive.git',
    download_url='https://github.com/mbnlc/yflive/releases',
    project_urls={
        "Source": "https://github.com/mbnlc/yflive",
        "Bug Tracker": "https://github.com/mbnlc/yflive/issues",
    },
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 5 - Production/Stable",

        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",

        "Operating System :: OS Independent",

        "License :: OSI Approved :: Apache Software License",

        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=["websocket-client", "protobuf"],
    packages=setuptools.find_packages(exclude="tests"),
    include_package_data=True,
    python_requires=">=3.6"
)