from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import *


class TestUrls(SimpleTestCase):

    def test_table_create_resolve(self):
        url = reverse('table-create')
        self.assertEquals(resolve(url).func, tables_create_table)

    def test_table_delete_resolve(self):
        url = reverse('table-delete', args=['48'])
        self.assertEquals(resolve(url).func, tables_delete_table)

    def test_table_add_col_resolve(self):
        url = reverse('table-add-col', args=['48'])
        self.assertEquals(resolve(url).func, tables_add_col)

    def test_table_edit_col_resolve(self):
        url = reverse('table-edit-col', args=['48', '1'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, tables_edit_col)

    def test_table_del_col_resolve(self):
        url = reverse('table-del-col', args=['48', '1'])
        self.assertEquals(resolve(url).func, tables_delete_col)

    def test_table_add_row_resolve(self):
        url = reverse('table-add-row', args=['48'])
        self.assertEquals(resolve(url).func, tables_add_row)

    def test_table_del_row_resolve(self):
        url = reverse('table-del-row', args=['48', '1'])
        self.assertEquals(resolve(url).func, tables_del_row)

    def test_database_save_resolve(self):
        url = reverse('database-save')
        self.assertEquals(resolve(url).func, export_to_csv)

    def test_table_database_set_resolve(self):
        url = reverse('database-set')
        self.assertEquals(resolve(url).func, database_set)

    def test_database_clear_resolve(self):
        url = reverse('database-clear')
        self.assertEquals(resolve(url).func, database_clear)



