# Facial Attendance System

- by Chris Nastasi & Ruben Reyes

## Description

This project aims to create a facial attendance system that detects unique faces and updates attendance values in the database for specific classes and specific students.

### Features

- Features


###


### Database Structure

- DATABASE SYSTEMS

```

    Class {
        class_id: int, PK
        room_num: int
        class_name: string
        class_description: string
        start_date: date
        end_date: date
        schedule: string
    }
    Student {
        student_id: int, PK
        class_id: int, FK
        student_name: string
    }
    Attendance {
        attendance_id: int, PK
        student_id: int, FK
        class_id: int, FK
        date: date
        status: boolean
    }

```