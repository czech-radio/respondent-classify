from setuptools import setup, find_packages

setup(
    name="labeler-server",
    version="0.10.0",
    py_module=["server"],
    # packages=find_packages(exclude=["docs", "tests"]),
    install_requires=["flask[dotenv]>=3.0.0"],
    extras_require={
        "dev": ["black", "isort", "pytest"]
    },
    entry_points={
        "console_scripts": [
            "labeler-server = server:main",
        ]
    }
    
)