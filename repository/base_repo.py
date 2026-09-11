from config.mongodb_config import connect_mongodb

class BaseRepository:

    collection_name = None

    def __init__(self):

        self.db = connect_mongodb()

        if not self.collection_name:
            raise ValueError(
                "collection_name is not defined"
            )

        self.collection = self.db[self.collection_name]