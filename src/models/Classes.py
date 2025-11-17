import os
import datetime

from pydantic import Field , BaseModel, ConfigDict , BeforeValidator
from pydantic.types import  StrictInt, StrictStr

from typing import Optional , Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]

# INFO: Classes Model Class
    ## This is the Classes Model that will be used to represent class/course data.
    ## FIXME: Removed roster for now to simplify the model.

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

def main():
    pass

if __name__ == "__main__":
    main()