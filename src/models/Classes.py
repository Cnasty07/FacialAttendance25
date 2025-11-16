import os
import datetime
import bson

from pydantic import Field , BaseModel, ConfigDict
from pydantic.dataclasses import dataclass
from pydantic.types import  StrictInt, StrictStr, AwareDatetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# @dataclass(init=True, repr=True)
class Classes(BaseModel):
    name: StrictStr = Field(description="Name of the class/course", min_length=1)
    course_code: StrictInt = Field(description="Numeric course code", ge=1)
    roster: list[bson.ObjectId]
    start_time: datetime.time
    end_time: datetime.time

    model_config = ConfigDict({
        "arbitrary_types_allowed": True,
        "extra": "forbid",
        "validate_assignment": True,
    })


def main():
    class_instance = Classes(
        name="Introduction to Programming",
        course_code=102,
        roster=[],
        start_time=datetime.time(9, 0),
        end_time=datetime.time(10, 30)
    )
    print(class_instance.__repr__())

if __name__ == "__main__":
    main()