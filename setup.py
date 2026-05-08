from setuptools import find_packages, setup

setup(
    name="python-mastery-repo",
    version="0.1.0",
    description="Enterprise-grade Python mastery repository with tutorials, examples, and production-ready modules.",
    packages=find_packages(exclude=["tests*", "*.tests*", "*.test*", "__pycache__"]),
    python_requires=">=3.9",
    install_requires=[
        "fastapi>=0.101.0",
        "uvicorn[standard]>=0.23.0",
        "pydantic>=2.9.0",
        "pandas>=2.2.0",
        "numpy>=2.0.0",
        "scipy>=1.11.0",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
        "structlog>=24.0.0",
        "pyspark>=3.5.0",
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
