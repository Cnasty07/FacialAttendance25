import datetime
import bson

from pydantic import BaseModel, Field, ConfigDict
from pydantic.types import StrictBool

class Attendance(BaseModel):
    attendance_id: bson.ObjectId
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
    attendance_instance = Attendance(
        attendance_id=bson.ObjectId(),
        student_id=bson.ObjectId(),
        class_id=bson.ObjectId(),
        attendance_date=datetime.datetime.now().time(),
        attendance_status=True
    )
    print(attendance_instance)

    

if __name__ == "__main__":
    main()