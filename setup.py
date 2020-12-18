import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hostess-deybhayden",
    version="0.0.1",
    author="Ben Hayden",
    author_email="hayden767@gmail.com",
    description="A small script to pull AWS cost and usage information per billed client.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deybhayden/hostess",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=["rich", "boto3"],
    scripts=["bin/hostess"],
)
