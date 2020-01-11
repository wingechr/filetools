import unittest
from filetools.tools import NestedTables2 as NestedTables


class TestNestedTables(unittest.TestCase):
    def create_nt(self):
        nt = NestedTables()
        # do not use setUp because parse_value has side effects
        nt.add_table("t1", ["/t1"])
        return nt

    def test_primitive(self):
        nt = NestedTables()
        data = "primitive"
        res = nt.parse(data)
        #self.assertEqual(data, res)

    def test_list(self):
        nt = NestedTables()
        data = [1, 2, 3]
        res = nt.parse(data)
        #self.assertEqual(res, None)

    def test_dict(self):
        nt = self.create_nt()
        data = {'t1': [{'id': 'test_id'}]}
        res = nt.parse(data)
        #self.assertEqual(nt.get_table('/t1')["table_data"]['test_id']['id'], 'test_id')
