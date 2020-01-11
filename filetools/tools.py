
import re
import logging
from collections import OrderedDict

FOLD_SEPARATOR = "."
FOLD_LIST_INDICATOR = "#"


class Dict:
    def __init__(self, allow_overwrite=True, get_key=None):
        """Modified dictionary
        Args:
            allow_overwrite (bool): if False: throws error if key
                already exists. Default: True
            get_key (function, optional): modify key before lookup, e.g.
                 make lowercase
        """
        self._data = OrderedDict()
        self.get_key = get_key or (lambda x: x)
        self.allow_overwrite = allow_overwrite

    def __getitem__(self, key):
        key2 = self.get_key(key)
        return self._data[key2][1]

    def __contains__(self, key):
        key2 = self.get_key(key)
        return key2 in self._data

    def __delitem__(self, key):
        key2 = self.get_key(key)
        if not self.allow_overwrite:
            raise Exception("Not allowed to remove items")
        del self._data[key2]

    def __setitem__(self, key, value):
        key2 = self.get_key(key)
        if not self.allow_overwrite and key2 in self._data:
            raise Exception("Duplicate key: %s" % key2)
        self._data[key2] = (key, value)

    def get(self, key, default=None, add_on_missing=False):
        """Get value from dictionary

        Args:
            key: key
            default: default value
            add_on_missing (boolean): if True: add item if key is missing
        Returns:
            value or default
        """
        try:
            return self[key]
        except KeyError:
            if add_on_missing:
                self[key] = default
            return default

    def update(self, obj):
        """Update self with items from dict

        Args:
            obj (dict): update data
        """
        for k, v in obj.items():
            self[k] = v

    def items(self):
        for k2, kv in self._data.items():
            yield kv

    def keys(self):
        for kv in self.items():
            yield kv[0]

    def values(self):
        for kv in self.items():
            yield kv[1]

    def __len__(self):
        return len(self._data)


def get_words(identifier: str) -> list:
    """tokenize an identifier into words

    Args:
         identifier(str): text
    Returns:
        list of words
    Examples:

        >>> get_words("helloWorld")
        ['hello', 'World']
        >>> get_words("hello_world")
        ['hello', 'world']
        >>> get_words("hello--world") # multiple split characters
        ['hello', 'world']
        >>> get_words("helloJSON")  # multiple uppercase
        ['hello', 'JSON']
    """
    # find all non upper case followed by upper case character
    text = ""
    for c1, c2 in zip(identifier, identifier[1:] + " "):
        text += c1
        if c2.isupper() and not c1.isupper():
            text += "_"
    # replace all the different split characters
    # NOTE: inverse \w matches a-z, A-Z, 0-9, and _
    text = re.sub(r"\W+", "_", text)
    text.strip("_")
    return text.split("_")


def structure_to_flat_dict(obj) -> dict:
    """Recursively fold structure into flat dict

    Reverse (sort of) of flat_dict_to_structure, but keys will
    be always strings.

    Args:
        obj: nested data structure
    Returns:
         flat dictionary
    Examples:
        >>> res = structure_to_flat_dict({1: [2, 3]})
        >>> sorted(list(res.items()))
        [('1.#0', 2), ('1.#1', 3)]


        >>> res = structure_to_flat_dict({1: [2, {3: 4}, [5, 6]]})
        >>> sorted(list(res.items()))
        [('1.#0', 2), ('1.#1.3', 4), ('1.#2.#0', 5), ('1.#2.#1', 6)]

    """
    res = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            k = str(k)
            assert FOLD_SEPARATOR not in k and FOLD_LIST_INDICATOR not in k
            if isinstance(v, (dict, list, tuple)):
                for k2, v2 in structure_to_flat_dict(v).items():
                    res["%s%s%s" % (k, FOLD_SEPARATOR, k2)] = v2
            else:
                res[k] = v
    elif isinstance(obj, (list, tuple)):
        for k, v in enumerate(obj):
            k = "%s%d" % (FOLD_LIST_INDICATOR, k)
            if isinstance(v, (dict, list, tuple)):
                for k2, v2 in structure_to_flat_dict(v).items():
                    res["%s%s%s" % (k, FOLD_SEPARATOR, k2)] = v2
            else:
                res[k] = v
    else:
        raise Exception("Not a dict or list")
    return res


def flat_dict_to_structure(flat_dict) -> object:
    """Recursively unfold flat dict into nested structure.

    Reverse (sort of) of structure_to_flat_dict, but keys will
    be always strings.

    Args:
        obj: flat dictionary
    Returns:
         nested data structure
    Examples:
        >>> flat_dict_to_structure({'1.#0': 2, '1.#1': 3})
        {'1': [2, 3]}

        >>> flat_dict_to_structure({'#0.#0': 1, '#0.#1': 2, '#0.#2.#0': 3})
        [[1, 2, [3]]]

    """
    is_list = None
    # split first part of key and group
    groups = {}
    for k, v in flat_dict.items():
        ks = k.split(FOLD_SEPARATOR)
        k1 = ks[0]  # first part
        k2 = FOLD_SEPARATOR.join(ks[1:])  # all the other parts joined
        is_list_item = k1.startswith(FOLD_LIST_INDICATOR)
        if is_list is None:
            is_list = is_list_item
        elif is_list != is_list_item:
            raise Exception("Keys must be all numerical or none of them")
        if k2:
            if k1 not in groups:
                groups[k1] = {}
            groups[k1][k2] = v
        else:  # recursion end
            groups[k1] = v
    if is_list:
        res = []
        for k in range(len(groups)):
            k = "%s%d" % (FOLD_LIST_INDICATOR, k)
            v = groups[k]
            if isinstance(v, dict):
                v = flat_dict_to_structure(v)
            res.append(v)
    else:
        res = {}
        for k, v in groups.items():
            if isinstance(v, dict):
                v = flat_dict_to_structure(v)
            res[k] = v
    return res


class Filter:
    def __init__(self, required=None, optional=None, ignored=None,
                 allow_unknown=False):
        """

        Examples:
            >>> f = Filter(ignored=['a'], allow_unknown=True)
            >>> f(['b', 'a'])
            ['b']

            >>> f = Filter(required=['a'], optional=['b', 'c'])
            >>> f(['b', 'a'])
            ['b', 'a']

            >>> f = Filter(required=['a', 'b'], allow_unknown=True)
            >>> f(['c', 'a'])
            Traceback (most recent call last):
            ...
            KeyError: 'Missing 1 required items'

            >>> f = Filter(required=['a'], optional=['b'])
            >>> f(['a', 'c'])
            Traceback (most recent call last):
            ...
            KeyError: 'Item not allowed: c'

        """
        self.required = set(required or [])
        self.optional = set(optional or [])
        self.ignored = set(ignored or [])
        self.allow_unknown = allow_unknown
        self.known = self.required | self.optional | self.ignored

    def __call__(self, items):
        res = []
        required_found = set()
        for it in items:
            if it in self.ignored:
                continue
            elif not self.allow_unknown and it not in self.known:
                raise KeyError('Item not allowed: %s' % it)
            if it in self.required:
                required_found.add(it)
            res.append(it)
        if required_found != self.required:
            n_missing = len(self.required - required_found)
            raise KeyError('Missing %d required items' % n_missing)
        return res


def structure_to_relational_tables(structure):
    """Convert a nested structure into relational tables.

    Args:
        structure: a nested python data structure

    Returns:
        list: table data
            * items are {name, schema, data}
            * values of data are lists of tuples
    """
    pass


class NestedTables:
    def __init__(self):
        self.pat2table = []
        self.logger = logging.getLogger("NestedTables")
        self.logger.setLevel(logging.DEBUG)
        for h in self.logger.handlers:
            h.setLevel(logging.DEBUG)

    def add_table(self, name, path_patterns, id_column=None, ref_id_column=None,
                  auto_id=False):
        tab = {
            "name": name,
            "table_data": {},
            "id_column": id_column or 'id',
            "ref_id_column": ref_id_column or '%s_id' % name,
            "auto_id": 0 if auto_id else None
        }
        for pat in path_patterns:
            self.pat2table.append((re.compile("^%s$" % pat), tab))

    def get_table(self, table_path):
        """
        return get_row_id function
        """
        for pat, tab in self.pat2table:
            if pat.match(table_path):
                return tab
        return None

    def parse_value(self, value, table_path='', col_name='', row_id=None):
        self.logger.debug(('parse_value',value, table_path, col_name, row_id))
        ref_table_path = table_path
        if col_name:
            ref_table_path += '/' + col_name
        self.logger.debug(('ref_table_path', ref_table_path))
        ref_table = self.get_table(ref_table_path)  # may be None
        if isinstance(value, dict):
            # this is actually a row in a different table with a 1-1 relation
            # we need to add it there and return the primary key
            # so that we can insert that as a foreign key.
            # In principle, we could also link it back
            if ref_table:
                ref_row_id = self.insert_row(row=value,
                                             table_path=ref_table_path,
                                             ref_table_path=table_path,
                                             ref_row_id=row_id)
                return ref_row_id
            else:  # not yet in table context
                for k, v in value.items():
                    self.parse_value(value=v, table_path=ref_table_path, col_name=k)

        elif isinstance(value, (list, tuple)):
            # this is a n-m-relation. We return None
            # rows must be added to another table
            if ref_table:
                ref_id_column = ref_table["ref_id_column"]
                for row in value:
                    # must make rows into a dict
                    row = {ref_id_column: row}
                    self.insert_row(row=row, table_path=ref_table_path,
                                    ref_table_path=table_path,
                                    ref_row_id=row_id)
            else:  # not in table context yet
                for row in value:
                    self.parse_value(row, table_path=ref_table_path)
            return None
        else:  # primitive  value
            return value

    def insert_row(self, row, table_path, ref_table_path='', ref_row_id=None):
        """
        Args:
            row(dict): row data
            table_path (str): url style path in the nested structure to
                identify the current table
            ref_table_path (str, optional): url style path in the nested
                structure to identify the parent table
            ref_row_id (optional): identifier of the parent row in the nested
                structure.

        Side effect:
            parsed row will be appended to table_data

        Returns:
            row_id
        """
        self.logger.debug(('insert_row', row, table_path, ref_table_path, ref_row_id))
        table = self.get_table(table_path)
        if table is None:
            raise Exception("No table for path: %s" % table_path)

        # get id, either by column or by auto incrementing max_id
        id_column = table["id_column"]
        if table["auto_id"] is None:
            print(row)
            row_id = row[id_column]
        else:
            row_id = table["auto_id"] + 1
            table["auto_id"] = row_id
        res = {}
        for col_name, value in row.items():
            col_value = self.parse_value(value=value, col_name=col_name,
                                         row_id=row_id, table_path=table_path)
            if col_value is not None:
                res[col_name] = col_value
        if ref_table_path and ref_row_id:
            # add foreign key ro ref table
            ref_table = self.get_table(ref_table_path)
            ref_id_column = ref_table["ref_id_column"]
            assert ref_id_column not in res
            res[ref_id_column] = ref_row_id
        table_data = table["table_data"]
        assert row_id not in table_data
        table_data[row_id] = res
        return row_id


class NestedTables2:
    def __init__(self):
        self.pat2table = []
        self.logger = logging.getLogger("NestedTables2")
        self.logger.setLevel(logging.DEBUG)
        for h in self.logger.handlers:
            self.logger.removeHandler(h)
        h = logging.StreamHandler()
        h.setLevel(logging.DEBUG)
        self.logger.addHandler(h)

    def add_table(self, name, path_patterns, id_column=None, ref_id_column=None,
                  auto_id=False):
        tab = {
            "name": name,
            "table_data": {},
            "id_column": id_column or 'id',
            "ref_id_column": ref_id_column or '%s_id' % name,
            "auto_id": 0 if auto_id else None
        }
        for pat in path_patterns:
            self.pat2table.append((re.compile("^%s$" % pat), tab))

    def get_table(self, table_path):
        """
        return get_row_id function
        """
        for pat, tab in self.pat2table:
            if pat.match(table_path):
                return tab
        return None

    def parse(self, value, parent_path='', key='', is_attr=False, parent_id=None):
        if not value:  # ignore None, [], {}
            return
        path = parent_path
        if key:
            path += '/' + key
        if isinstance(value, dict):
            row_id = None  # TODO: must be identified first
            res = {}
            for k, v in value.items():
                # ensure keys are strings
                if not isinstance(k, str):
                    raise Exception('Keys maust be strings')
                v = self.parse(value=v, parent_path=path, key=k, is_attr=True, parent_id=row_id)
                res[k] = v
            id_col = 'id'
            res[id_col] = row_id
        elif isinstance(value, (list, tuple)):
            # ensure all items in list have are dicts
            types = [type(el) for el in value]
            if len(set(types)) > 1:
                raise Exception('All Elements in list must have the same type')
            elif issubclass(types[0], (list, tuple)):
                raise Exception('Cannot parse list of list')
            elif not issubclass(types[0], dict):
                id_col = 'id'
                value = [{id_col: v} for v in value]
            for i, v in enumerate(value):
                self.parse(value=v, parent_path=path, key='', is_attr=False, parent_id=parent_id)
        else:
            res = value
        return res
