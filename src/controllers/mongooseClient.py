import os

from pymongo.mongo_client import MongoClient
from pymongoose import set_schemas, set_schemas_from_list
from pymongoose.mongo_types import MongoException, MongoError

from src.models.remoteModels import StudentUser, Classes

# Using pymongoose to connect to remote MongoDB and set schemas
class RemoteDBC:
    def __init__(self) -> None:
        self.client = MongoClient(os.getenv("MONGO_URI"))
        self.db = self.client.EmbeddedAppData
        try:
            schemas = {
                "Student": StudentUser(empty=True).schema,
                "Classes": Classes(empty=True).schema,
            }

            # Schemas to dictionary or list
            set_schemas(self.db, schemas)
            set_schemas_from_list(self.db, [StudentUser(empty=True), Classes(empty=True)])

        except MongoException as e:
            print("Error setting schemas:", e)


