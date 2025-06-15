from setuptools import setup, find_packages

setup(
    name="deployit",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "typer",
        "rich",
        "docker",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "deployit=deployit.cli:run",
        ],
    },
    python_requires=">=3.8",
) 