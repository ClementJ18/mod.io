from setuptools import setup, find_packages
import re

version = ""
with open("modio/__init__.py") as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError("version is not set")

readme = ""
with open("README.md") as f:
    readme = f.read()

setup(
    name="mod.io",
    version=version,
    description="mod.io python wrapper",
    author="Clement Julia",
    author_email="clement.julia13@gmail.com",
    url="https://github.com/ClementJ18/mod.io",
    long_description_content_type="text/markdown",
    long_description=readme,
    packages=find_packages(include=["modio", "modio.*"]),
    install_requires=["aiohttp==3.8.1", "requests==2.28.1", "typing-extensions==4.3.0"],
)
