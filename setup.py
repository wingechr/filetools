# coding: utf-8
import setuptools

__title__ = "filetools"
__version__ = "0.0.8"
__author__ = "Christian Winger"
__contact__ = "c@wingechr.de"
__license__ = "MIT License"
__language__ = "en"
__description__ = "file processing tools"


if __name__ == "__main__":

    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

    setuptools.setup(
        name=__title__,
        version=__version__,
        author=__author__,
        author_email=__contact__,
        description=__description__,
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://pypi.org/project/filetools",
        project_urls={
            "Documentation": "https://filetools.readthedocs.io",
            "Source": "https://github.com/wingechr/filetools",
        },
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: " + __license__,
            "Operating System :: OS Independent",
        ],
        python_requires=">=3.6",
        package_data={"": ["data/**"]},
    )
