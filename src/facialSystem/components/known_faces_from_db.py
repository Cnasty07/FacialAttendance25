import os
import cv2
import face_recognition
import numpy as np
import sqlite3
import pandas as pd

try:
    from ...controllers.databaseController import ClassTable, StudentTable
except:
    from controllers.databaseController import ClassTable, StudentTable     


# TODO: get tables from db to add to known faces
#       1. class specific to pull students from db
#       2. get student id and face data
#       3. add to known faces


class KnownFaces:
    def __init__(self, db_path):
            self.db_path = db_path
            self.known_face_encodings = []
            self.known_face_names = []

    def load_known_faces(self,class_id):
        # gets class id from interface
        class_table = ClassTable()
        class_table.read(class_id=class_id)
        student_ids_for_class = class_table.read(class_id=class_id)

        # fetches student ids for class

        # fetches student face data for each student
        # adds student face data to known faces
        # student_table_data = StudentTable(self.db_path)
        
        # for student_id in student_ids_for_class:
        #     student_table_data.cursor.execute("SELECT student_id, student_face_data FROM student WHERE class_id = ?", (class_id,))
        #     student_face_data = student_table_data.read(student_id)
        #     self.known_face_encodings.append(student_face_data)
        #     self.known_face_names.append(student_id)
            
        # # cursor.execute("SELECT , student_id, student_face_data FROM student")
        # rows = class_table.cursor.fetchall()
        # for row in rows:
        #     name, encoding = row
        #     encoding = np.frombuffer(encoding, dtype=np.float64)
        #     self.known_face_encodings.append(encoding)
        #     self.known_face_names.append(name)
        class_table.conn.close()

    def get_known_faces(self):
        return self.known_face_encodings, self.known_face_names
    
    
def main():
    
    db_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../database/school.db')
    known_faces = KnownFaces(db_name)
    known_faces.load_known_faces(1)

if __name__ == '__main__':
    main() 
