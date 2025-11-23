# Models Folder Outline

## Outline

Due to the changes in database it seems necessary to explain the changes. There are 4 model classes that correspond to the user.

1. User
2. Classes
3. Face
4. Attendance

```mermaid
---
title: Model Layout
---
classDiagram
    class User["Student--User"]
    User : +String name
    User : +String email
    User : +Array enrolled_classes
    User : +Array face_data
    User : +Array attendance_record

    class Classes
    Classes : +String name
    Classes : +Integer course_code
    Classes : +Array roster
    Classes : +Date start_time
    Classes : +Date end_time

    class Face
    User <|-- Face
    Face : +ObjectId student_id
    Face : +ObjectId class_id
    Face : +Array face_encoding

    class Attendance
    Classes <|-- Attendance
    Attendance : +ObjectId student_id
    Attendance : +ObjectId class_id
    Attendance : +Date attendance_date
    Attendance : +Bool status

```

## Notes

1. Still subject to change as I iterate.
2. The User Dataclass is loaded after login (assuming we get to that point).
3. As of now, have not tested the models in the main program.
4. Working on how to manage the relationships between documents in NoSQL MongoDB. Primarily just trying to keep ID's as the relation.
