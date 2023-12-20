from setuptools import setup, find_packages

setup(
    name="labeler",
    version="0.11.0",
    packages=find_packages(exclude=["docs", "tests"]),
    package_dir={"": "src"},
    package_data={"labeler": ["*.json"]},
    install_requires=["pandas", "pandarallel", "requests", "scikit-learn"],
    extras_require={}
)