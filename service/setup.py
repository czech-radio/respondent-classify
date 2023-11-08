from setuptools import setup, find_packages

setup(
    name="service",
    version="0.11.0",
    package_dir={"": "src"},
    packages=find_packages(exclude=["docs", "tests"]),
    install_requires=["flask"],
    extras_require={},
)
