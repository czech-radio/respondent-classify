from setuptools import setup, find_packages

setup(
    name="service",
    version="0.12.0",
    packages=find_packages(include=["service"]),
    install_requires=["flask", "python-dotenv"],
    extras_require={}
)
