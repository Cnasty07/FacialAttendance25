import os
import sqlite3


class DB_Controller:
    """Database Controller for managing database interactions."""
    def __init__(self, db_path='data/db/records.db'):
        # Ensure the database directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Connect to the SQLite database
        self.connection_obj = sqlite3.connect(db_path)
        self.cursor_obj = self.connection_obj.cursor()

        # Initialize tables
        self._initialize_tables()

    def _initialize_tables(self):
        """Creates the database tables if they do not exist."""
        self.cursor_obj.execute('''CREATE TABLE IF NOT EXISTS class (
                                    class_id INTEGER PRIMARY KEY,
                                    class_name TEXT NOT NULL,
                                    teacher_id INTEGER NOT NULL
                                )''')

        self.cursor_obj.execute('''CREATE TABLE IF NOT EXISTS student (
                                    student_id INTEGER PRIMARY KEY,
                                    student_name TEXT NOT NULL,
                                    class_id INTEGER,
                                    FOREIGN KEY (class_id) REFERENCES class(class_id)
                                )''')

        self.cursor_obj.execute('''CREATE TABLE IF NOT EXISTS attendance (
                                    attendance_id INTEGER PRIMARY KEY,
                                    student_id INTEGER,
                                    date TEXT NOT NULL,
                                    status TEXT NOT NULL,
                                    FOREIGN KEY (student_id) REFERENCES student(student_id)
                                )''')

        self.cursor_obj.execute('''CREATE TABLE IF NOT EXISTS facial_data (
                                    data_id INTEGER PRIMARY KEY,
                                    student_id INTEGER,
                                    facial_features TEXT NOT NULL,
                                    FOREIGN KEY (student_id) REFERENCES student(student_id)
                                )''')
        self.connection_obj.commit()

    def new_entry(self, table_name, data):
        """Inserts a new record into the specified table."""
        try:
            if table_name == 'class':
                self.cursor_obj.execute(
                    'INSERT INTO class (class_id, class_name, teacher_id) VALUES (?, ?, ?)', data)
            elif table_name == 'student':
                self.cursor_obj.execute(
                    'INSERT INTO student (student_id, student_name, class_id) VALUES (?, ?, ?)', data)
            elif table_name == 'attendance':
                self.cursor_obj.execute(
                    'INSERT INTO attendance (attendance_id, student_id, date, status) VALUES (?, ?, ?, ?)', data)
            elif table_name == 'facial_data':
                self.cursor_obj.execute(
                    'INSERT INTO facial_data (data_id, student_id, facial_features) VALUES (?, ?, ?)', data)
            else:
                raise ValueError("Table not recognized")
            self.connection_obj.commit()
        except sqlite3.Error as e:
            print(f"Database error during insertion: {e}")
        except ValueError as ve:
            print(f"Value error: {ve}")

    def read_entry(self, table_name, record_id):
        """Reads a record by ID from the specified table."""
        try:
            if table_name == 'class':
                self.cursor_obj.execute('SELECT * FROM class WHERE class_id = ?', (record_id,))
            elif table_name == 'student':
                self.cursor_obj.execute('SELECT * FROM student WHERE student_id = ?', (record_id,))
            elif table_name == 'attendance':
                self.cursor_obj.execute('SELECT * FROM attendance WHERE attendance_id = ?', (record_id,))
            elif table_name == 'facial_data':
                self.cursor_obj.execute('SELECT * FROM facial_data WHERE data_id = ?', (record_id,))
            else:
                raise ValueError("Table not recognized")
            return self.cursor_obj.fetchone()
        except sqlite3.Error as e:
            print(f"Database error during read operation: {e}")
        except ValueError as ve:
            print(f"Value error: {ve}")
            return None

    def update_entry(self, table_name, record_id, data):
        """Updates a record in the specified table."""
        try:
            if table_name == 'class':
                self.cursor_obj.execute(
                    'UPDATE class SET class_name = ?, teacher_id = ? WHERE class_id = ?',
                    (*data, record_id))
            elif table_name == 'student':
                self.cursor_obj.execute(
                    'UPDATE student SET student_name = ?, class_id = ? WHERE student_id = ?',
                    (*data, record_id))
            elif table_name == 'attendance':
                self.cursor_obj.execute(
                    'UPDATE attendance SET student_id = ?, date = ?, status = ? WHERE attendance_id = ?',
                    (*data, record_id))
            elif table_name == 'facial_data':
                self.cursor_obj.execute(
                    'UPDATE facial_data SET student_id = ?, facial_features = ? WHERE data_id = ?',
                    (*data, record_id))
            else:
                raise ValueError("Table not recognized")
            self.connection_obj.commit()
        except sqlite3.Error as e:
            print(f"Database error during update operation: {e}")
        except ValueError as ve:
            print(f"Value error: {ve}")

    def delete_entry(self, table_name, record_id):
        """Deletes a record by ID from the specified table."""
        try:
            if table_name == 'class':
                self.cursor_obj.execute('DELETE FROM class WHERE class_id = ?', (record_id,))
            elif table_name == 'student':
                self.cursor_obj.execute('DELETE FROM student WHERE student_id = ?', (record_id,))
            elif table_name == 'attendance':
                self.cursor_obj.execute('DELETE FROM attendance WHERE attendance_id = ?', (record_id,))
            elif table_name == 'facial_data':
                self.cursor_obj.execute('DELETE FROM facial_data WHERE data_id = ?', (record_id,))
            else:
                raise ValueError("Table not recognized")
            self.connection_obj.commit()
        except sqlite3.Error as e:
            print(f"Database error during deletion: {e}")
        except ValueError as ve:
            print(f"Value error: {ve}")

    def close_db(self):
        """Closes the database connection."""
        if self.connection_obj:
            self.connection_obj.close()


def main():
    pass

if __name__ == '__main__':
    main() 
