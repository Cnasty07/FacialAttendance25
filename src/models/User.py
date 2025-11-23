import bson
import numpy as np
from pydantic import BeforeValidator, Field, StrictStr, BaseModel, ConfigDict
from typing import Optional, Annotated , Any , Dict

from pymongoose.mongo_types import Types, Schema

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

    
    # Build Pydantic model from a pymongoose / pymongo document (dict)
    @classmethod
    def from_mongo(cls, doc: Dict[str, Any]) -> "StudentUserModel":
        if not doc:
            raise ValueError("No document provided")
        d = dict(doc)  # shallow copy
        # convert ObjectId to str for Pydantic field if present
        if "_id" in d and isinstance(d["_id"], bson.ObjectId):
            d["_id"] = str(d["_id"])
        # Ensure face_data is list-of-lists of floats
        fd = d.get("face_data")
        if fd is None:
            d["face_data"] = []
        else:
            # pymongoose may store face_data as flat list or nested; normalize
            normalized: list[list[float]] = []
            if isinstance(fd, list) and fd and all(isinstance(x, (int, float)) for x in fd):
                # treat as single embedding
                normalized = [[float(x) for x in fd]]
            else:
                for item in fd:
                    if isinstance(item, (list, tuple, np.ndarray)):
                        arr = np.asarray(item, dtype=float).tolist()
                        normalized.append([float(x) for x in arr])
                    else:
                        # fallback: try to coerce scalar to single-value vector
                        normalized.append([float(item)])
            d["face_data"] = normalized
        return cls.model_validate(d)

    # Produce a dict safe for pymongo / pymongoose insert/update
    def model_dump_for_mongo(self, keep_id: bool = True) -> Dict[str, Any]:
        doc = self.model_dump()  # pydantic v2
        # convert id string -> ObjectId if possible and desired
        if "_id" in doc and doc["_id"] is not None:
            try:
                doc["_id"] = bson.ObjectId(doc["_id"])
            except Exception:
                # leave as-is (could be None or non-ObjectId)
                pass
        # Ensure face_data entries are plain python lists of floats

        def _convert(obj: Any) -> Any:
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            if isinstance(obj, list):
                return [_convert(x) for x in obj]
            if isinstance(obj, dict):
                return {k: _convert(v) for k, v in obj.items()}
            return obj
        doc["face_data"] = _convert(doc.get("face_data", []))
        # Optionally remove _id if you don't want to overwrite existing docs on insert
        if not keep_id and "_id" in doc:
            doc.pop("_id", None)
        return doc

    # JSON for API responses (ObjectId -> str)
    def to_json(self, **kwargs) -> str:
        # model_dump_json will use standard encoders — ensure ObjectId and ndarrays are serializable
        # fallback: convert with model_dump then stringify
        out = self.model_dump()
        if "_id" in out and isinstance(out["_id"], bson.ObjectId):
            out["_id"] = str(out["_id"])
        return BaseModel.model_construct(type(self)).model_validate(out).model_dump_json() if False else __import__("json").dumps(out)



# -- StudentUser Schema For PyMongoose --
class StudentUserSchema(Schema):
    schema_name = "Student"

    id = None
    name = str
    email = str
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


## -- END OF STUDENT USER MODEL --



## -- ADMIN USER MODEL --
class AdminUserModel(UserModel):
    role: StrictStr = Field(description="Role of the admin user", min_length=1, alias="role")

## -- END OF ADMIN USER MODEL --


def main():
    print("Test")

if __name__ == "__main__":
    main()