import os
import sqlite3


#main code 
class DB_Controller:
    def __init__(self):
        self.connection_obj = sqlite3.connect('data/db/records.db')
        self.cursor_obj = self.connection_obj.cursor()
    
    def new_entry(self, table_name, data):
        if table_name == 'class':
            self.cursor_obj.execute('INSERT INTO class (class_id, class_name, teacher_id) VALUES (?, ?, ?)', data)
        elif table_name == 'student':
            self.cursor_obj.execute('INSERT INTO student (student_id, student_name, class_id) VALUES (?, ?, ?)', data)
        elif table_name == 'attendance':
            self.cursor_obj.execute('INSERT INTO attendance (attendance_id, student_id, date, status) VALUES (?, ?, ?, ?)', data)
        elif table_name == 'facial_data':
            self.cursor_obj.execute('INSERT INTO facial_data (data_id, student_id, facial_features) VALUES (?, ?, ?)', data)
        else:
            raise ValueError("Table not recognized")
        self.connection_obj.commit()

    def close_db(self):
        self.connection_obj.close()
    
    


def main():
    pass

if __name__ == '__main__':
    main() 
