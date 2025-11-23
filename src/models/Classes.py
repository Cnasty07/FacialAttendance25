import os
import datetime

from pydantic import Field , BaseModel, ConfigDict , BeforeValidator
from pydantic.types import  StrictInt, StrictStr

from typing import Optional , Annotated

from pymongoose.mongo_types import Types, Schema

PyObjectId = Annotated[str, BeforeValidator(str)]

# INFO: Classes Model Class

# FIXME: Removed roster for now to simplify the model.

# -- CLASSES MODEL --
class ClassesModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: StrictStr = Field(description="Name of the class/course", min_length=1)
    course_code: StrictInt = Field(description="Numeric course code", ge=1)
    start_time: datetime.time
    end_time: datetime.time

    model_config = ConfigDict({
        "arbitrary_types_allowed": True,
        "extra": "forbid",
        "validate_assignment": True,
    })



# -- Classes Schema for PyMongoose --
class ClassesSchema(Schema):
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

def main():
    pass

if __name__ == "__main__":
    main()