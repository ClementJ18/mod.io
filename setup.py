from distutils.core import setup

setup(
    name="modio",
    version="0.3.0",
    description="mod.io python wrapper",
    author="Clement Julia",
    author_email="clement.julia13@gmail.com",
    url="https://github.com/ClementJ18/mod.io",
    packages=["modio"],
    install_requires=["aiohttp==3.8.1", "requests==2.28.1"],
)
