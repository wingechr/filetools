from collections import OrderedDict


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
