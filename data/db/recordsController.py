import sqlite3

class DatabaseController:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()

class ClassTable(DatabaseController):
    def __init__(self, db_name):
        super().__init__(db_name)
        self.connect()
        # self.cursor.execute('''CREATE TABLE IF NOT EXISTS class (
        #                         id INTEGER PRIMARY KEY,
        #                         name TEXT NOT NULL,
        #                         room_number INTEGER NOT NULL,
        #                         description TEXT,
        #                         start_date DATE,
        #                         end_date DATE,
        #                         time TIME)''')
        # self.conn.commit()

    def create(self, name, room_number, description, start_date, end_date, time):
        self.cursor.execute('INSERT INTO class (name, room_number, description, start_date, end_date, time) VALUES (?, ?, ?, ?, ?, ?)', 
                            (name, room_number, description, start_date, end_date, time))
        self.conn.commit()

    def read(self, class_id):
        self.cursor.execute('SELECT * FROM class WHERE id = ?', (class_id,))
        return self.cursor.fetchone()

    def update(self, class_id, name, room_number, description, start_date, end_date, time):
        self.cursor.execute('UPDATE class SET name = ?, room_number = ?, description = ?, start_date = ?, end_date = ?, time = ? WHERE id = ?', 
                            (name, room_number, description, start_date, end_date, time, class_id))
        self.conn.commit()

class StudentTable(DatabaseController):
    def __init__(self, db_name):
        super().__init__(db_name)
        self.connect()
        # self.cursor.execute('''CREATE TABLE IF NOT EXISTS student (
        #                         id INTEGER PRIMARY KEY,
        #                         name TEXT NOT NULL,
        #                         classes INTEGER,
        #                         face_encodings TEXT,
        #                         FOREIGN KEY (classes) REFERENCES class(id))''')
        # self.conn.commit()

    def create(self, name, classes, face_encodings):
        self.cursor.execute('INSERT INTO student (name, classes, face_encodings) VALUES (?, ?, ?)', 
                            (name, classes, face_encodings))
        self.conn.commit()

    def read(self, student_id):
        self.cursor.execute('SELECT * FROM student WHERE id = ?', (student_id,))
        return self.cursor.fetchone()

    def update(self, student_id, name, classes, face_encodings):
        self.cursor.execute('UPDATE student SET name = ?, classes = ?, face_encodings = ? WHERE id = ?', 
                            (name, classes, face_encodings, student_id))
        self.conn.commit()

class AttendanceTable(DatabaseController):
    def __init__(self, db_name):
        super().__init__(db_name)
        self.connect()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                                id INTEGER PRIMARY KEY,
                                class_id INTEGER,
                                student_id INTEGER,
                                date DATE,
                                status TEXT,
                                FOREIGN KEY (class_id) REFERENCES class(id),
                                FOREIGN KEY (student_id) REFERENCES student(id))''')
        self.conn.commit()

    def create(self, class_id, student_id, date, status):
        self.cursor.execute('INSERT INTO attendance (class_id, student_id, date, status) VALUES (?, ?, ?, ?)', 
                            (class_id, student_id, date, status))
        self.conn.commit()

    def read(self, attendance_id):
        self.cursor.execute('SELECT * FROM attendance WHERE id = ?', (attendance_id,))
        return self.cursor.fetchone()

    def update(self, attendance_id, class_id, student_id, date, status):
        self.cursor.execute('UPDATE attendance SET class_id = ?, student_id = ?, date = ?, status = ? WHERE id = ?', 
                            (class_id, student_id, date, status, attendance_id))
        self.conn.commit()

class FaceTable(DatabaseController):
    def __init__(self, db_name):
        super().__init__(db_name)
        self.connect()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS face (
                                id INTEGER PRIMARY KEY,
                                student_id INTEGER,
                                encoding TEXT,
                                FOREIGN KEY (student_id) REFERENCES student(id))''')
        self.conn.commit()

    def create(self, student_id, encoding):
        self.cursor.execute('INSERT INTO face (student_id, encoding) VALUES (?, ?)', 
                            (student_id, encoding))
        self.conn.commit()

    def read(self, face_id):
        self.cursor.execute('SELECT * FROM face WHERE id = ?', (face_id,))
        return self.cursor.fetchone()

    def update(self, face_id, student_id, encoding):
        self.cursor.execute('UPDATE face SET student_id = ?, encoding = ? WHERE id = ?', 
                            (student_id, encoding, face_id))
        self.conn.commit()
        


def main():
    pass

if __name__ == 'main':
    main()