import datetime

from pymongo.mongo_client import MongoClient
from pymongoose import set_schemas, set_schemas_from_list
from pymongoose.mongo_types import MongoException, MongoError

from src.models.remoteModels import StudentUser, Classes
from src.controllers.mongooseClient import RemoteDBC

# TODO: Finish using this controller for remote DB operations

class remoteController:
    def __init__(self) -> None:
        self.rClient = RemoteDBC()

    def get_student(self,student_email: str):
        student = self.rClient.db.Student.find_one({"email": student_email})
        return student

    def get_class(self, class_name: str):
        classes = self.rClient.db.Classes.find_one({"name": class_name})
        return classes

    def get_all_classes(self) -> list[Classes]:
        classes = self.rClient.db.Classes.find({})
        all_classes = [cls for cls in classes]
        return all_classes


def main() -> None:
   # rdbc = RemoteDBC() # Starts connection
    # new_student = StudentUser(
    #     name="John Doe",
    #     email="john.doe@example.com",
    #     # face_data=[np.random.rand(128) for _ in range(5)],
    # )
    # print(new_student)

    # id = new_student.save()
    # print("Inserted Student ID:", id)
    
    # # Finding and deleting the inserted test data
    # load_student = rdbc.db.Student.find_one({"name": "John Doe"})
    # print("Loaded Student:", load_student, type(load_student))
    # rdbc.db.Student.delete_one({"_id": load_student['_id']})  # Clean up inserted test data
    # classes = Classes(
    #     name="Biology 101",
    #     course_code=104,
    #     start_time=datetime.datetime.now(),
    #     end_time=datetime.datetime.now() + datetime.timedelta(hours=1)
    # )
    # class_id = classes.save()
    # print("Inserted Class ID:", class_id)

    # load_class = rdbc.db.Classes.find_one({"name": "Biology 101"})
    # print("Loaded Class:", load_class, type(load_class))

    # rdbc.db.Classes.delete_one({"_id": load_class['_id']})  # Clean up inserted test data
    pass

if __name__ == "__main__":
    main()
