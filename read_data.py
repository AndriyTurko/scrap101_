import os
import json
import redis
import sqlite3


class BaseConnector:
    def __init__(self, store_name, file_name):
        self.store_name = store_name
        self.file_name = file_name

    def json_exist_in_storage(self, json_type='avail'):
        raise NotImplementedError('Not implemented yet')

    def read_json_from_storage(self, json_type='avail'):
        raise NotImplementedError('Not implemented yet')

    def write_json_into_storage(self, json_content, json_type='avail'):
        raise NotImplementedError('Not implemented yet')


class FileConnector(BaseConnector):
    def get_file_path(self, json_type='avail'):
        if json_type == 'avail':
            return 'temp_files/{}/{}/avail_{}.json'.format(self.store_name, self.file_name, self.file_name)
        else:
            return 'temp_files/{}/{}/full_{}.json'.format(self.store_name, self.file_name, self.file_name)

    def json_exist_in_storage(self, json_type='avail'):
        file_path = self.get_file_path(json_type)
        if os.path.exists(file_path):
            return True
        else:
            return False

    def read_json_from_storage(self, json_type='avail'):
        file_path = self.get_file_path(json_type)
        with open(file_path, "r") as file1:
            return json.loads(file1.read())

    def write_json_into_storage(self, json_content, json_type='avail'):
        file_path = self.get_file_path(json_type)
        with open(file_path, "w") as file1:
            json.dump(json_content, file1)


def redis_decorator(func):
    def new_function(self, *args, json_type='avail'):
        self.redis_connection = redis.Redis()
        self.redis_key = self.get_redis_key(json_type)
        print(44444)
        result = func(self, *args, json_type)
        print(5555)
        self.redis_connection.close()
        return result
    return new_function


class RedisConnector(BaseConnector):
    def get_redis_key(self, json_type):
        return '{}_{}_{}'.format(self.store_name, self.file_name, json_type)

    @redis_decorator
    def json_exist_in_storage(self, *args, json_type='avail'):
        print(111111, self.redis_key)
        return self.redis_connection.exists(self.redis_key)

    @redis_decorator
    def read_json_from_storage(self, *args, json_type='avail'):
        redis_content = self.redis_connection.get(self.redis_key)
        result = json.loads(redis_content)
        return result

    @redis_decorator
    def write_json_into_storage(self, json_content, json_type='avail'):
        self.redis_connection.set(self.redis_key, json.dumps(json_content))


class SQLiteConnector(BaseConnector):
    def json_exist_in_storage(self, json_type='avail'):
        connection_obj = sqlite3.connect(json_type + '.db')
        cursor_obj = connection_obj.cursor()
        exist = cursor_obj.execute("DROP TABLE IF EXISTS " + json_type)
        connection_obj.close()
        return exist

    def read_json_from_storage(self, json_type='avail'):
        # connection_obj = sqlite3.connect(json_type + '.db')
        # if connection_obj.execute("SELECT * FROM json_type"):
        #     cursor = connection_obj.execute("SELECT * FROM json_type")
        #     rows = cursor.fetchall()
        # connection_obj.close()
        return 'rows'

    def write_json_into_storage(self, json_content, json_type='avail'):
        connection_obj = sqlite3.connect(json_type + '.db')
        cursor_obj = connection_obj.cursor()
        table = """ CREATE TABLE json_type (
                			json_content
                		); """
        end = cursor_obj.execute(table)
        print("Table is Ready")
        connection_obj.close()
        return end
#
# Connecting to sqlite
# connection object
# connection_obj = sqlite3.connect('geek.db')
#
# # cursor object
# cursor_obj = connection_obj.cursor()
#
# # Drop the GEEK table if already exists.
#     cursor_obj.execute("DROP TABLE IF EXISTS GEEK")
#
# # Creating table
# table = """ CREATE TABLE GEEK (
# 			Email VARCHAR(255) NOT NULL,
# 			First_Name CHAR(25) NOT NULL,
# 			Last_Name CHAR(25),
# 			Score INT
# 		); """
# cursor_obj.execute(table)
# print("Table is Ready")
# connection_obj.close()
