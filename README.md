# Facial Recognition Attendance System

- by Chris Nastasi, Nicholas Hernandez, Ian Arredondo
- previous contributor: Ruben Reyes

## Description

This project aims to create a facial attendance system that detects unique faces and updates attendance values in the database for specific classes and specific students.

## To Run

Please install the dependencies provided using:

```{bash}
pipenv shell
```

And then use the command:

```{bash}
pipenv run python main.py
```

## Overview

A Python-based facial recognition system for managing and recording student attendance. It utilizes machine learning for face detection and recognition, integrated with a SQLite database for data management, and provides a user-friendly GUI built with Tkinter.

## Features

- **Face Detection and Recognition**: Identifies and verifies student faces using `face_recognition` and `dlib`.
- **Database Management**: Handles student and attendance records with SQLite.
- **User Interface**: Interactive GUI for capturing images and confirming attendance.
- **Modular Architecture**: Organized codebase with separate modules for components and controllers.
- **Unit Testing**: Ensures code reliability with comprehensive tests.

### Schema

``` SQL

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

### Project Structure

``` python
.
├── Pipfile
├── Pipfile.lock
├── README.md
├── components
│   ├── __init__.py
│   ├── capture.py
│   ├── comparison.py
│   └── recognition.py
├── controllers
│   ├── __init__.py
│   ├── databaseController.py
│   └── facialController.py
├── database
│   ├── __init__.py
│   ├── recordsController.py
│   ├── schema.sql
│   ├── school.db
│   └── tests
│       ├── Musk.webp
│       ├── Musk3.jpg
│       ├── MuskComp.jpg
│       ├── face_20241126_082103.jpg
│       ├── face_20241126_082841.jpg
│       ├── girlTest.jpg
│       ├── groupPic.jpg
│       ├── ruben1.jpg
│       └── ruben2.jpg
├── main.py
├── setup.py
└── tests
│   └── test_db_data.py
│   ├── test_remote_db.py
│   └── test_facial.py
│   └── test_model_db.py
└── ui
│   ├── __init__.py
│   └── admin_panel.py
│   └── choose_user_panel.py
│   └── facial_student_panel.py
```
