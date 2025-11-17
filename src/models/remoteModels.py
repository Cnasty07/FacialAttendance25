from pymongoose.mongo_types import Types, Schema


# -- StudentUser Schema --
class StudentUser(Schema):
    schema_name = "Student"

    id = None
    name = None
    email = None
    face_data = None
    
    def __init__(self, **kwargs):
        self.schema = {
            "name": {
                "type": Types.String,
                "minlength": 1
            },
            "email": {
                "type": Types.String,
                "minlength": 5,
                "maxlength": 50
            },
            "face_data": [{
                "type": Types.Number,
            }]
        }
        super().__init__(self.schema_name, self.schema, kwargs)

    def __str__(self) -> str:
        return f"StudentUser(name={self.name}, email={self.email})"

# -- END --

# -- FaceData Schema --
class FaceData(Schema):
    schema_name = "FaceData"

    id = None
    encoding = None

    def __init__(self, **kwargs):
        self.schema = {
            "encoding": [{
                "type": Types.Number,
            }]
        }
        super().__init__(self.schema_name, self.schema, kwargs)

    def __str__(self) -> str:
        return f"FaceData(encoding_length={self.encoding}"

# -- END --


# -- Classes Schema --
class Classes(Schema):
    schema_name = "Classes"

    id = None
    name = str
    course_code = int
    start_time = None
    end_time = None

    def __init__(self, **kwargs):
        self.schema = {
            "name": {
                "type": Types.String,
                "minlength": 1,
                "maxlength": 100
            },
            "course_code": {
                "type": Types.Number,
            },
            "start_time": {
                "type": Types.Date,
            },
            "end_time": {
                "type": Types.Date,
            },
        }
        super().__init__(self.schema_name, self.schema, kwargs)

    def __str__(self) -> str:
        return f"Classes(name={self.name}, course_code={self.course_code})"

# -- END --