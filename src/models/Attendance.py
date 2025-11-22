import datetime
import bson

from pydantic import BaseModel, Field, ConfigDict , BeforeValidator
from pydantic.types import StrictBool
from typing import Annotated , Optional

PyObjectId = Annotated[str, BeforeValidator(str)]

# TODO: Implement this when everything else is done.
    # Not in use yet.

class AttendanceModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    student_id: bson.ObjectId
    class_id: bson.ObjectId
    attendance_date: datetime.time = Field(description="Date and time of the attendance record")
    attendance_status: StrictBool = Field(description="True if present, False if absent")

    model_config = ConfigDict({
        "arbitrary_types_allowed": True,
        "extra": "forbid",
        "validate_assignment": True,
    })


def main():
    pass


if __name__ == "__main__":
    main()