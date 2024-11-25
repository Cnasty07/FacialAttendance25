import os
import controllers
import components
import database
import ui
from controllers import facial_controller , databaseController

def test_database():
    # class_table = databaseController.ClassTable().read(1)
    
    student_table = databaseController.StudentTable().read(1)

    # print(class_table)
    print(student_table)


def test_facial():
    facial_controller.FacialController(1).match_processed_image()


def main():
    test_database()
    # test_facial()

if __name__ == '__main__':
    main() 
