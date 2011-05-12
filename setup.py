import setuptools 
import datetime

version = datetime.datetime.utcnow().strftime("0.0.dev-%Y-%m-%dT%H%MZ")
pypi_download_url = "http://pypi.python.org/pypi/kia/" + version

setuptools.setup(
    name = "kia",
    version = version,
    
    url = "https://github.com/jeremybanks/kia/",
    download_url = pypi_download_url,
    
    description = "Very neato.",
    
    packages = ["kia"],
    
    entry_points = {
        "console_scripts": [
            "kia = kia.__main__:main"
        ],
    },
    
    install_requires = ["M2Crypto>=0.21.0,<0.22.0",
                        "Twisted>=11.0.0,<12.0.0"],
    
    package_dir = {"": "src/"},
    
    long_description = open("readme.rst").read(),
    
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "License :: Public Domain",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "Framework :: Twisted",
        "Operating System :: OS Independent",
        "Topic :: Internet :: Proxy Servers",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: Name Service (DNS)"
    ],
    
    author = "Jeremy Banks",
    author_email = "jeremy@jeremybanks.ca"
)
