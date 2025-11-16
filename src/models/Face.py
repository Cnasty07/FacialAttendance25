
from pydantic import BaseModel, Field, ConfigDict
import numpy as np
import bson

# INFO: Primarily to be used when capturing and storing face into User model for Student Users.
class Face(BaseModel):
    student_id: bson.ObjectId
    class_id: bson.ObjectId
    face_encoding: list[np.ndarray]

    model_config = ConfigDict({
        "arbitrary_types_allowed": True,
        "extra": "forbid",
        "validate_assignment": True,
    })



def main():
    face_instance = Face(
        student_id=bson.ObjectId(),
        class_id=bson.ObjectId(),
        face_encoding=[np.ndarray(shape=(128,), dtype=float)]
    )
    print(face_instance)

if __name__ == "__main__":
    main()