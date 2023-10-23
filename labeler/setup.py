from setuptools import setup, find_packages

print(find_packages(exclude=["docs", "tests"]))
setup(
    name="labeler",
    version="0.10.0",
    packages=find_packages(exclude=["docs", "tests"]),
    install_requires=["pandas", "pandarallel", "requests", "scikit-learn"],
    extras_require={
        "dev": ["matplotlib", "pytest"]
    }#,
    #entry_points={
    #    "console_scripts": [
    #        "labeler-server = server:main",
    #    ]
    #}

)