from setuptools import setup, find_packages

setup(
    name="labeler-server",
    version="0.10.0",
    package_dir={"": "src"},
    packages=find_packages(exclude=["docs", "tests"]),
    install_requires=["flask[dotenv]>=3.0.0"],
    extras_require={},
    entry_points={
        "console_scripts": [
            "labeler-server = labeler_server.__init__:main",
        ]
    }
)