import sqlite3
import face_recognition
import numpy as np

def get_known_faces_from_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, encoding FROM known_faces")
    rows = cursor.fetchall()
    conn.close()
    
    known_face_encodings = []
    known_face_names = []
    
    for row in rows:
        name, encoding = row
        known_face_encodings.append(np.frombuffer(encoding, dtype=np.float64))
        known_face_names.append(name)
    
    return known_face_encodings, known_face_names

def compare_faces(known_face_encodings, known_face_names, image_path):
    unknown_image = face_recognition.load_image_file(image_path)
    unknown_face_encodings = face_recognition.face_encodings(unknown_image)
    
    for unknown_face_encoding in unknown_face_encodings:
        results = face_recognition.compare_faces(known_face_encodings, unknown_face_encoding)
        face_distances = face_recognition.face_distance(known_face_encodings, unknown_face_encoding)
        
        best_match_index = np.argmin(face_distances)
        if results[best_match_index]:
            name = known_face_names[best_match_index]
            print(f"Match found: {name}")
        else:
            print("No match found")

if __name__ == "__main__":
    db_path = 'path_to_your_database.db'
    image_path = 'path_to_your_image.jpg'
    
    known_face_encodings, known_face_names = get_known_faces_from_db(db_path)
    compare_faces(known_face_encodings, known_face_names, image_path)