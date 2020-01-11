# Readme

This is still very much in progress. Don't use it :-)

* Documentation: https://filetools.readthedocs.io
* Source: https://github.com/wingechr/filetools
* Package: https://pypi.org/project/filetools

# Definitions

* provide functions to retrieve files from `remote_resource` to local `path`
    * http(s) download
    * sql query
    * copy from network
    * ...
* identify `file_type` of file at `path`
    * /text
    * /text/csv
    * /text/csv/my_special_flavor
    * ...
* `file_type` is node in a `file_type_hierarchy`
    *  /text/csv > /text > /
* find available/best functions to get `metadata` for file with `file_type`
  and optionally, whitelisted/blacklisted `attributes`
* use functions to get `metadata` from file at `path`
* provide function for `file_type` that (sometimes) can
    * open (`__enter__`) file resource
    * list available `streams` / `tables` by name give their `schema` 
    * provide an iterator over each `stream` that returns `objects` with 
      `attributes`
    * think of a stream as a table with objects as rows
    * There should be a way to determine which streams MUST be there, which CAN be 
      there, and which should be ignored
* sometimes, this is only possible for a `collection` or `package` of files
    * shapefiles
    * csv + csvt
* provide function for `file_type` that (sometimes) can take a set of streams 
  and save them to a (`collection` of ) file(s).  
* `attributes` in `streams` may have conversion functions to and from string or 
  from source to python data types, as well as validators
* it should be possible to quickly plugin new classes / instances to do those 
  jobs
* There should be a global configuration to customize functionality
* Al lot of this is intended to be parallel to datapackages
* maybe we can use jsonschema to define the structures? 

# Use case

* most of all: reuse code to take a file that follows a specific schema, 
  * convert it to the expected streams that are equivalent to tables in a 
    database or resources in a datapackage
* build datapipelines from one type of file to another, which we then can
  plug into a build tool like `scons`
  


# Todo

* How should we treat container files like zip?

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
sphinx-build -a -E -b html docs/source docs/build
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

