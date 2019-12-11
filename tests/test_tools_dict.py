import os
import unittest
from filetools.tools import Dict
from filetools.classes import FileTool

data_dir = os.path.join(os.path.dirname(__file__), "data")


def get_data_file(filename):
    path = os.path.normpath(os.path.join(data_dir, filename))
    assert os.path.isfile(path)
    return path


class TestDictLowercaseNoUpdate(unittest.TestCase):
    def test_normal(self):
        dict_normal = Dict()
        dict_normal["A"] = 1
        self.assertEqual(dict_normal.get("a"), None)
        # can put "a" in as well
        dict_normal["a"] = 2
        del dict_normal["A"]
        self.assertEqual(list(dict_normal.keys())[0], "a")
        self.assertEqual(len(dict_normal), 1)

    def test_mod(self):
        dict_mod = Dict(allow_overwrite=False, get_key=lambda x: str(x).lower())
        dict_mod["A"] = 1
        self.assertEqual(dict_mod["a"], 1)
        # cannot put "a" in again
        def add_fail():
            dict_mod["a"] = 2

        # cannot delete
        def del_fail():
            del dict_mod["A"]

        self.assertRaises(Exception, add_fail)
        self.assertRaises(Exception, del_fail)
        self.assertTrue("a" in dict_mod)

    def test_add_default(self):
        dct = Dict()
        dct.get("a", [], add_on_missing=True).append(1)
        self.assertEqual(dct["a"], [1])


class TestFileToolBytes(unittest.TestCase):
    def setUp(self):
        self.ft = FileTool()

    def test_identify_empty(self):
        tf = get_data_file("empty_file")
        meta = self.ft.inspect_file(tf)
        self.assertEqual(meta["size_bytes"], 0)


if __name__ == "__main__":
    unittest.main()
