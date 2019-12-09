# filetools

This is still very much in progress. Don't use it :-)

* Documentation: https://filetools.readthedocs.io
* Source: https://github.com/wingechr/filetools
* Package: https://pypi.org/project/filetools

# development

# code quality
python3 -m black  # actually reformat code
python3 -m pycodestyle .  # check (previously pep8)
python3 -m pylint filetools

# testing
python3 -m unittest

# build docs locally
sphinx-build -b html docs/source docs/build

# bump version
bumpversion --allow-dirty patch

# git
git add .
git status
git commit
git push  # use github webhooks to build documentation on readthedocs

# build (remove old versions first)
python3 setup.py rotate -m ".*" -k 0 sdist

# distribute
python3 -m twine upload dist/*
