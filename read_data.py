import os
import json
import redis


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


class RedisConnector(BaseConnector):
    def get_redis_key(self, json_type):
        return '{}_{}_{}'.format(self.store_name, self.file_name, json_type)

    def json_exist_in_storage(self, json_type='avail'):
        redis_connection = redis.Redis()
        redis_key = self.get_redis_key(json_type)
        print(111111, redis_key)
        key_exist = redis_connection.exists(redis_key)
        redis_connection.close()
        return key_exist

    def read_json_from_storage(self, json_type='avail'):
        redis_connection = redis.Redis()
        redis_key = self.get_redis_key(json_type)
        redis_content = redis_connection.get(redis_key)
        redis_connection.close()
        return json.loads(redis_content)

    def write_json_into_storage(self, json_content, json_type='avail'):
        redis_connection = redis.Redis()
        redis_key = self.get_redis_key(json_type)
        redis_connection.set(redis_key, json.dumps(json_content))
        redis_connection.close()
