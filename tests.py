import os
import controllers
import components
import database
import face_recognition
import ui
from controllers import facial_controller , databaseController

import json
import numpy as np

def add_database_entry(table_name, entry_data):
    if table_name == 'student':
        databaseController.StudentTable().create(entry_data)
    elif table_name == 'class':
        databaseController.ClassTable().create(entry_data)
    else:
        print("Invalid table name")


def test_database():
    # # class_table = databaseController.ClassTable().read(1)
    
    # student_table = databaseController.StudentTable()
    # ruben = facial_controller.FacialController().process_image('./database/tests/ruben2.jpg')
    
    # test_student = {'name': 'Ruben Reyes', 'classes': '1', 'face_encoding': ruben.tolist()}
    # print(ruben)
    # # student_table.update(11, test_student['name'], test_student['classes'], test_student['face_encoding'])
    # # student_table.create(test_student['name'],test_student['classes'],test_student['face_encoding'])
    # # print(class_table)
    # print(student_table.read())
    pass
    
    
class TestDatabase:
    def __init__(self):
        self.student_table = databaseController.StudentTable()
        self.class_table = databaseController.ClassTable()
        self.attendance_table = databaseController.AttendanceTable()
        self.face_table = databaseController.FaceTable()
    
    def test_student_table(self):
        ruben = facial_controller.FacialController().process_image('./database/tests/ruben2.jpg')
        test_student = {'name': 'Ruben Reyes', 'classes': '1', 'face_encoding': ruben.tolist()}
        self.student_table.create(test_student['name'],test_student['classes'],test_student['face_encoding'])
        print(self.student_table.read())
    
    def test_class_table(self):
        test_class = {'name': 'Math 101'}
        self.class_table.create(test_class['name'])
        print(self.class_table.read())
    
    def test_attendance_table(self):
        test_attendance = {'student_id': '1', 'class_id': '1', 'date': '2021-09-09'}
        self.attendance_table.create(test_attendance['student_id'], test_attendance['class_id'], test_attendance['date'])
        print(self.attendance_table.read())
    
    def test_face_table(self):
        # test_face = {'student_id': '1', 'face_encoding': facial_controller.FacialController().process_image('./database/tests/ruben2.jpg').tolist()}
        # self.face_table.create(test_face['student_id'], test_face['face_encoding'])
        # print(self.face_table.read())
        pass
    


def test_facial():
    # gets image and process to encoding
    # capture_test = facial_controller.FacialController().process_image('./database/tests/ruben1.jpg')

    # loads images and tests to array
    load_encoding = facial_controller.FacialController().load_known_faces()
    # print(load_encoding.shape)
    # converts array to encoding

    
    # print("capture: ",capture_test, "\nload: ",load_encoding)

    
    # result = facial_controller.FacialController.match_processed_image(capture_test,load_encoding)
    # print(result[0])



def main():
    # test_database()
    # new_db_test = TestDatabase()
    # new_db_test.test_student_table()
    
    
    
    test_facial()

    # student_table = databaseController.StudentTable()
    # student_table.create('Ruben Reyes', '1', facial_controller.FacialController().process_image('./database/tests/ruben2.jpg'))
    # all_students = student_table.read()

    # # student_table.delete_all()
    # print(student_table.read())

if __name__ == '__main__':
    main() 
