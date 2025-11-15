import datetime
from dataclasses import dataclass, field
import bson



@dataclass(init=True, repr=True)
class Attendance:
    attendance_id: bson.ObjectId
    student_id: bson.ObjectId
    class_id: bson.ObjectId
    attendance_date: datetime.datetime
    attendance_status: bool


def main():
    attendance_instance = Attendance(
        attendance_id=bson.ObjectId(),
        student_id=bson.ObjectId(),
        class_id=bson.ObjectId(),
        attendance_date=datetime.datetime.now(),
        attendance_status=True
    )
    print(attendance_instance.__repr__())

if __name__ == "__main__":
    main()