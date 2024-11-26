import os
import controllers
import components
import database
import ui
from controllers import facial_controller , databaseController

def add_database_entry(table_name, entry_data):
    if table_name == 'student':
        databaseController.StudentTable().create(entry_data)
    elif table_name == 'class':
        databaseController.ClassTable().create(entry_data)
    else:
        print("Invalid table name")

# Example usage:
# add_database_entry('student', {'name': 'John Doe', 'id': 123})
# add_database_entry('class', {'name': 'Math 101', 'id': 456})

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
