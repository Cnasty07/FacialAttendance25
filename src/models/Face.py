
from pydantic import BaseModel, Field, ConfigDict
import numpy as np
import bson

from pymongoose.mongo_types import Types, Schema

# INFO: Primarily to be used when capturing and storing face into User model for Student Users.
    # Each Face instance represents a single face encoding associated with a student and a class.

class FaceModel(BaseModel):
    student_id: bson.ObjectId = Field(description="Student's unique identifier", alias="student_id")
    class_id: bson.ObjectId = Field(description="Class's unique identifier", alias="course_code")
    face_encoding: list[float] = Field(description="Face encoding data array")

    model_config = ConfigDict({
        "arbitrary_types_allowed": True,
        "extra": "forbid",
        "validate_assignment": True,
    })



# -- FaceData Schema For PyMongoose--
class FaceDataSchema(Schema):
    schema_name = "FaceData"

    id = None
    encoding = None

    def __init__(self, **kwargs):
        self.schema = {
            "encoding": [{
                "type": Types.Number,
            }]
        }
        super().__init__(self.schema_name, self.schema, kwargs)

    def __str__(self) -> str:
        return f"FaceData(encoding_length={self.encoding}"

# -- END --


def main():
    pass

if __name__ == "__main__":
    main()