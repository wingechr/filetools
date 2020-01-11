class Table:
    def __init__(self, name, id_column=None, ref_id_column=None):
        self.name = name
        self.auto_id_column = '_id'
        self.id_column = id_column or self.auto_id_column
        self.ref_id_column = ref_id_column or ('%s_id' % self.name)
        self.n_records = 0
        self.data = {}
        self.columns = set()

    def create_record(self, data):
        """
        Returns:
            record_id
        """
        self.n_records += 1
        if self.id_column == self.auto_id_column:
            key = self.n_records
        else:
            key = data[self.id_column]
        self.data[key] = {}
        return key

    def update_record(self, record_id, record, allow_value_update=False):
        rec = self.data[record_id]
        for k, v in record.items():
            if k in rec and not allow_value_update:
                raise Exception('Not allowed to overwrite existing value for %s.' % k)
            self.columns.add(k)
            rec[k] = v


class Database:
    def __init__(self, table_path_map=None, auto_create=True, allow_value_update=True, allow_single_value=True, list_of_list='batch', link_1_1_relation='down'):
        self.auto_create = auto_create
        self.tables = {}
        self.table_path_map = table_path_map or {}
        self.allow_value_update = allow_value_update
        self.allow_single_value = allow_single_value
        self.list_of_list = list_of_list
        self.link_1_1_relation = link_1_1_relation
        assert self.list_of_list in (False, 'batch')
        assert self.link_1_1_relation in ('up', 'down', 'both')

    def create_table(self, table_path, name=None, id_column=None, alias_paths=None):
        assert table_path not in self.tables
        name = name or self.get_table_name_from_path(table_path)
        self.tables[table_path] = Table(name=name, id_column=id_column)
        for p in (alias_paths or []):
            self.table_path_map[p] = table_path

    def get_table(self, table_path):
        """
        Returns:
            Table
        """
        if table_path in self.table_path_map:
            table_path = self.table_path_map[table_path]
        if table_path not in self.tables and self.auto_create:
            self.create_table(table_path=table_path)
        return self.tables[table_path]


    def get_table_name_from_path(self, table_path):
        return table_path.replace('/', '_')


    def get_list_items_type(self, items):
        items_type = None
        for it in items:
            t = self.get_item_type(it)
            if items_type is None:
                items_type = t
            elif items_type != t:
                raise Exception('All items in list must be of same type.')
        return items_type


    def get_item_type(self, obj):
        if isinstance(obj, dict):
            return 'dict'
        elif isinstance(obj, (list, tuple)):
            return 'list'
        else:
            return 'value'


    def join_path(self, path, item):
        return path + '/' + item


    def parse_dict(self, obj, table_path='', ref=None):
        """Place record in the database.

        Args:
            obj(dict): possibly nestewd record data

        Returns:
            record id

        """
        record = {}  # flat dict
        for k, v in (ref or {}).items():
            record[k] = v

        if table_path:  # not in root
            table = self.get_table(table_path=table_path)
            record_id = table.create_record(data=obj)
            ref = {table.ref_id_column: record_id}
        else:  # no ref on root
            ref = None
            table = None
            record_id = None

        for k, v in obj.items():
            ref_table_path = self.join_path(table_path, k)
            v_type = self.get_item_type(v)
            if v_type == 'dict':
                # parse object in separate list. optionally, we could also link directly to the item,
                # since it's exactly one
                if self.link_1_1_relation == 'down':
                    v = self.parse_dict(obj=v, table_path=ref_table_path, ref=None)
                elif self.link_1_1_relation == 'up':
                    self.parse_dict(obj=v, table_path=ref_table_path, ref=ref)
                    v = None
                else:  # both
                    v = self.parse_dict(obj=v, table_path=ref_table_path, ref=ref)
            elif v_type == 'list':
                # do not add a field, instead: parse list as new table and add thid record's id to link it
                self.parse_list(obj=v, table_path=ref_table_path, ref=ref)
                v = None
            else:
                pass
            if v is not None:
                record[k] = v

        # not in root
        if table_path:
            table.update_record(record_id=record_id, record=record, allow_value_update=self.allow_value_update)
            return record_id

    def parse_list(self, obj, table_path='', ref=None):
        list_items_type = self.get_list_items_type(obj)
        for v in obj:
            if list_items_type == 'dict':
                ref_record_id = self.parse_dict(obj=v,table_path=table_path, ref=ref)
            elif list_items_type == 'list':
                # list of lists: not well defined. we could interpret it as
                # just multiple batches of data
                if self.list_of_list == 'batch':
                    for ls in obj:
                        self.parse_list(obj=ls, table_path=table_path, ref=ref)
                else:
                    raise Exception('List of lists not allowed.')
            else:
                # list of values: the assumption is that this is a m-n relation
                # `ref` refers to the first table,
                # the values are keys of the second table (`table_path`)
                table = self.get_table(table_path)
                record = {
                    table.ref_id_column: v
                }
                for k, v in (ref or {}).items():
                    record[k] = v
                mn_table_path = self.join_path(table_path, '#')
                table_mn = self.get_table(mn_table_path)
                record_id = table_mn.create_record(data=record)
                table_mn.update_record(record_id=record_id, record=record, allow_value_update=self.allow_value_update)

    def parse(self, obj):
        obj_type = self.get_item_type(obj)
        if obj_type == 'list':
            self.parse_list(obj=obj)
        elif obj_type == 'dict':
            self.parse_dict(obj=obj)
        else:
            if not self.self.allow_single_value:
                raise Exception('Single value not allowed.')
            table = self.get_table(table_path='')
            record = {table.id_column: obj}
            record_id = table.create_record(record)
            table.update_record(record=record, record_id=record_id, allow_value_update=self.allow_value_update)


db = Database(auto_create=False)
db.create_table(table_path='/t1', id_column='tid')
db.create_table(table_path='')
db.create_table(table_path='/#')
# db.parse({"t1": [{"tid": 9}, {"tid": 8}]})
db.parse([{}])
print(db.get_data())