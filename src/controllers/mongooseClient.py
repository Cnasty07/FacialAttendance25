import os

from pymongo.mongo_client import MongoClient
from pymongoose import set_schemas, set_schemas_from_list
from pymongoose.mongo_types import MongoException, MongoError

from src.models.User import StudentUserSchema
from src.models.Classes import ClassesSchema
# Using pymongoose to connect to remote MongoDB and set schemas

# TODO: Rename to better reflect remote DB usage
class RemoteDBC:
    def __init__(self) -> None:
        self.client = MongoClient(os.getenv("MONGO_URI"),tls=True,tlsAllowInvalidCertificates=True) # Temporary fix while working on capture 
        self.db = self.client.EmbeddedAppData
        try:
            schemas = {
                "Student": StudentUserSchema(empty=True).schema,
                "Classes": ClassesSchema(empty=True).schema,
            }

            # Schemas to dictionary or list
            set_schemas(self.db, schemas)
            set_schemas_from_list(self.db, [StudentUserSchema(empty=True), ClassesSchema(empty=True)])

        except MongoException as e:
            print("Error setting schemas:", e)


