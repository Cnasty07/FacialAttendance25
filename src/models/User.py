import os
import bson
import numpy as np
from pydantic import BeforeValidator, Field, StrictStr, BaseModel, ConfigDict
from typing import Optional, Annotated 

# INFO: User Model Class
    ## This is the User Model that will be used for both Student and Admin Users
    ## After auth is complete, we can instantiate the User object with the relevant data.

PyObjectId = Annotated[str, BeforeValidator(str)]

# TODO: Implement methods for fetching user data from the database using the remoteDatabaseController.

class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: StrictStr = Field(alias="name", description="Full name of the user", min_length=1)
    email: StrictStr = Field(alias="email", description="Email address of the user",min_length=5,max_length=50)

    model_config = ConfigDict({
        "arbitrary_types_allowed": True,
        "extra": "forbid",
        "validate_assignment": True,
        "title": "User_Model",
    })

## -- STUDENT USER MODEL --
## FIXME: Issues
    ## 1. Pydantic does not support numpy arrays directly, so we need to convert them to lists for storage.
    ## 2. Attendance records and enrolled classes are commented out for now to simplify the model.
class StudentUserModel(UserModel):
    face_data: list[list[float]] = Field(alias="face_data", description="List of face encoding data arrays")
    # enrolled_classes: list[PyObjectId] = Field(alias="enrolled_classes", description="List of enrolled class IDs")
    # attendance_records: dict[bson.ObjectId, list[str]] = None  # classID: [dates]

## -- END OF STUDENT USER MODEL --



## -- ADMIN USER MODEL --
class AdminUserModel(UserModel):
    role: StrictStr = Field(description="Role of the admin user", min_length=1, alias="role")

## -- END OF ADMIN USER MODEL --
