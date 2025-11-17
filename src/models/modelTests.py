import os
from src.models.User import StudentUser

def StudentUserModelLoad():
    new_student = StudentUser(
        name="John Doe",
        email="john.doe@example.com",
        enrolled_classes=[],
        face_data=[]
    )
    return new_student


def main():
    student = StudentUserModelLoad()
    print(student)
    
if __name__ == "__main__":
    main()
