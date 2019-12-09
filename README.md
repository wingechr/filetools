# filetools

This is still very much in progress. Don't use it :-)

* Documentation: https://filetools.readthedocs.io
* Source: https://github.com/wingechr/filetools
* Package: https://pypi.org/project/filetools


# Development

### code quality
```bash
python3 -m black .  # actually reformat code
python3 -m pycodestyle .  # check (previously pep8)
python3 -m pylint filetools
```

### testing
```bash
nosetests --with-doctest
```

### build docs locally
```bash
pandoc -f markdown_github -i README.md -o docs/source/readme.rst
sphinx-build -b html docs/source docs/build
```

### bump version
```bash
bumpversion --allow-dirty patch
```

### git
```bash
git add .
git status
git commit
git push  # use github webhooks to build documentation on readthedocs
```

### build (remove old versions first)
```bash
python3 setup.py rotate -m ".*" -k 0 sdist
```

### distribute
```bash
python3 -m twine upload dist/*
```
