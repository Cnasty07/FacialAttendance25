from src.models.User import StudentUserSchema
from src.models.Classes import ClassesSchema

from src.controllers.mongooseClient import mongoose_init

# TODO: Finish using this controller for remote DB operations

class remoteController:
    def __init__(self) -> None:
        self.rClient = mongoose_init()  # Initialize remote DB connection
        # self.rClient = self.mongoClient() # Initialize remote DB connection
        self.Student = self.rClient.db.Student
        self.Classes = self.rClient.db.Classes

    def get_student(self, student_email: str) -> StudentUserSchema | None:
        """_summary_
            Fetch a student from the database by email.
        Args:
            student_email (str): _description_
        Returns:
            StudentUserSchema | None: _description_
        """
        try:
            student = self.Student.find_one({"email": student_email})
            # TODO: Fix parsing
            # student = StudentUserSchema.parse(student)
            # print("Fetched Student:", student)
        except Exception as e:
            print("Error fetching student:", e)
            return None

        return student

    def get_all_students(self) -> list[StudentUserSchema]:
        """_summary_
            Fetch all students from the database.
        Returns:
            list[StudentUserSchema]: _description_
        """
        try:
            students = self.Student.find({})
        except Exception as e:
            print("Error fetching students:", e)
            return []
        all_students = [stu for stu in students]
        return all_students

    def get_class(self, class_name: str) -> ClassesSchema | None:
        try:
            classes = self.Classes.find_one({"name": class_name})
        except Exception as e:
            print("Error fetching class:", e)
            return None

        return classes

    def get_all_classes(self) -> list[ClassesSchema]:
        try:
            classes = self.Classes.find({})
        except Exception as e:
            print("Error fetching classes:", e)
            return []
        all_classes = [cls for cls in classes]
        return all_classes


def main() -> None:
    pass


if __name__ == "__main__":
    main()
