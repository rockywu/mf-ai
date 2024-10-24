from pymilvus import MilvusClient

class MilvusDatabase:
    def __init__(
        self,  
        uri='http://home.wujialei.com:19530',
        user="root",
        password="Rockywu0427",
        db_name="mf_db"
        ):
        self.client = MilvusClient(
            uri=uri,
            user=user,
            password=password,
            db_name=db_name
        )

    def load_collection(self, collection_name, replica_number=1):
        self.client.load_collection(collection_name=collection_name, replica_number=replica_number)
        load_state = self.client.get_load_state(collection_name=collection_name)
        print('Load state for {}: {}'.format(collection_name, load_state))

    def search(self, collection_name, data,limit=10, filter=None, anns_field=None, output_fields=None, search_params=None):
        return self.client.search(
            collection_name=collection_name,
            data=data,
            filter=filter,
            anns_field=anns_field,
            output_fields=output_fields,
            limit=limit,
            search_params=search_params
        )

    def close(self):
        self.client.close()