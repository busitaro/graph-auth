from setuptools import setup
from setuptools import find_packages


DESCRIPTION = "authentication tool for Microsoft365 Graph api"
NAME = "graph_auth"
AUTHOR = "busitaro10"
AUTHOR_EMAIL = "busitaro10@gmail.com"
URL = "https://github.com/busitaro/graph-auth"
DOWNLOAD_URL = "https://github.com/busitaro/graph-auth"
VERSION = 0.12

INSTALL_REQUIRES = [
    "requests>=2.31.0",
]

setup(
    name=NAME,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    url=URL,
    version=VERSION,
    download_url=DOWNLOAD_URL,
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
)
