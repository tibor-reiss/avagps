import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="avagps",
    version="1.0.0",
    author="Tibor Reiss",
    author_email="tibor.reiss@gmail.com",
    description="Avast homework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tibor-reiss/avagps",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'flask',
        'gunicorn',
        'pytest-mock',
        'pytest-cov',
        'python-dotenv',
        'requests',
        'timeout-decorator',
    ],
    python_requires='>=3.8',
)
