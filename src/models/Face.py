
from pydantic import BaseModel, Field, ConfigDict
import numpy as np
import bson

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

def main():
    pass

if __name__ == "__main__":
    main()