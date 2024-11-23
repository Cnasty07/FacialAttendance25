import os
import cv2
import face_recognition
import numpy as np
import sqlite3
from ...data.db.recordsController import StudentTable, ClassTable

# TODO: get tables from db to add to known faces
#       1. class specific to pull students from db
#       2. get student id and face data
#       3. add to known faces


class KnownFaces:
    def __init__(self, db_path):
            self.db_path = db_path
            self.known_face_encodings = []
            self.known_face_names = []

    def load_known_faces(self):
        class_table = ClassTable(self.db_path)
        class_id = 12345
        student_ids_for_class = class_table.read(class_id=class_id)
        
        student_table_data = StudentTable(self.db_path)
        
        for student_id in student_ids_for_class:
            student_table_data.cursor.execute("SELECT student_id, student_face_data FROM student WHERE class_id = ?", (class_id,))
            student_face_data = student_table_data.read(student_id)
            self.known_face_encodings.append(student_face_data)
            self.known_face_names.append(student_id)
            
        # cursor.execute("SELECT , student_id, student_face_data FROM student")
        rows = cursor.fetchall()
        for row in rows:
            name, encoding = row
            encoding = np.frombuffer(encoding, dtype=np.float64)
            self.known_face_encodings.append(encoding)
            self.known_face_names.append(name)
        conn.close()

    def get_known_faces(self):
        return self.known_face_encodings, self.known_face_names
    
    
def main():
    known_faces = KnownFaces('../../data/db/records.db')

if __name__ == '__main__':
    main() 
