import os
import datetime
from dataclasses import dataclass , field
import bson

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

@dataclass(init=True, repr=True)
class Class:
    name: str
    course_code: int
    roster: list[bson.ObjectId]
    start_time: datetime.time | None = field(default=None)
    end_time: datetime.time | None = field(default=None)


def main():
    class_instance = Class(
        name="Introduction to Programming",
        course_code=102,
        roster=[],
        # start_time=datetime.datetime(2025,8,25,9,0).time(),
        # class_end_time=datetime.datetime(2025,12,12,10,30).time()
    )
    print(class_instance.__repr__())

    # Testing adding Class
    client = MongoClient(host=os.getenv("MONGO_URI"), server_api=ServerApi("1"),connect=True)
    client_db = client["EmbeddedAppData"]
    class_collection = client_db["Classes"]
    for classes in class_collection.find().sort("course_code", 1):
        print(classes)
    

if __name__ == "__main__":
    main()