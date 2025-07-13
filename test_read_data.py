import unittest
import os
import json
import tempfile
from read_data import FileConnector, RedisConnector, SQLiteConnector
from unittest import mock
import shutil


class TestFileConnector(unittest.TestCase):
    def setUp(self):
        self.store_name = os.path.join(self.temp_dir, 'store')
        self.file_name = 'test.json'
        self.connector = FileConnector(self.store_name, self.file_name)
        self.temp_dir = tempfile.mkdtemp()
        os.makedirs(self.connector.get_file_path().rsplit('/')[0], exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_write_and_read_json(self):
        content = {"key": "value"}
        self.connector.write_json_into_storage(content)
        read = self.connector.read_json_from_storage()
        self.assertEqual(read, content)

    def test_json_exist_true(self):
        self.connector.write_json_into_storage({"x": 1})
        self.assertTrue(self.connector.json_exist_in_storage())

    def test_json_exist_false(self):
        file_path = self.connector.get_file_path()
        if os.path.exists(file_path):
            os.remove(file_path)
        self.assertFalse(self.connector.json_exist_in_storage())


class TestRedisConnector(unittest.TestCase):
    def setUp(self):
        self.store_name = 'store'
        self.file_name = 'file'
        self.connector = RedisConnector(self.store_name, self.file_name)

    def test_write_and_read_json(self, ):
        self.connector.write_json_into_storage({"key": "value"})
        result = self.connector.read_json_from_storage()
        self.assertEqual(result, {"key": "value"})
