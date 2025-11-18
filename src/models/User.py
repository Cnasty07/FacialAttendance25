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


## -- END OF STUDENT USER MODEL --



## -- ADMIN USER MODEL --
class AdminUserModel(UserModel):
    role: StrictStr = Field(description="Role of the admin user", min_length=1, alias="role")

## -- END OF ADMIN USER MODEL --


def main():
    print("Test")
    # from src.controllers.remoteDatabaseController import remoteController
    # rdc = remoteController() # connect to DB
    
    # # new_student = rdc.get_student("alice@example.com") # gets single student from db
    # # student = StudentUserModel.from_mongo(new_student) # convert to pydantic model
    # # print(type(student.face_data))
    
    # new_student = StudentUserModel(
    #     name="Ruben Reyes",
    #     email="rreyes@tamusa.edu",
    #     face_data= []
    # )
    # face_data_encoding = [-0.020214959979057312, 0.04823107272386551, 0.09015103429555893, -0.050497930496931076, 0.025843920186161995, -0.005287497770041227, -0.04980546608567238, -0.0991913229227066, 0.11601994931697845, -0.14017634093761444, 0.22910569608211517, -0.012691516429185867, -0.19086889922618866, -0.0739898607134819, -0.021474061533808708, 0.16852112114429474, -0.16225256025791168, -0.15294978022575378, -0.07976768165826797, -0.06346189230680466, 0.05949011817574501, -0.011332922615110874, -0.06966444849967957, 0.053340595215559006, -0.17387016117572784, -0.3367103338241577, -0.056988805532455444, -0.08749478310346603, -0.03600757569074631, -0.07037677615880966, -0.0673011764883995, -0.0008221145253628492, -0.1566217690706253, 0.007236035540699959, -0.02518971636891365, 0.03944769874215126, -0.08303820341825485, -0.11732520908117294, 0.16082611680030823, 0.06531994789838791, -0.1244097501039505, 0.0426800511777401, 0.026970194652676582, 0.26371484994888306, 0.22457686066627502, 0.021907398477196693, 0.061527881771326065, -0.04934816062450409, 0.1638544201850891, -0.28010526299476624, 0.04651135206222534, 0.11192744225263596, 0.13790948688983917, 0.12156731635332108, 0.1084631159901619, -0.1438412070274353, -0.023742375895380974, 0.06660439074039459, -0.09450268000364304, 0.08894098550081253, 0.0022377909626811743, 0.008467938750982285, 0.017094042152166367, -0.09421052038669586, 0.18049709498882294, 0.052815962582826614, -0.1745525747537613, -0.0214040819555521, 0.11100216209888458, -0.1013927087187767, -0.08328315615653992, -0.06060859188437462, -0.1324283629655838, -0.20514164865016937, -0.3079852759838104, 0.06844553351402283, 0.34967362880706787, 0.17323115468025208, -0.23701614141464233, -0.0392506867647171, -0.05896873027086258, 0.004965668078511953, 0.1080223023891449, 0.0337168350815773, -0.044890109449625015, -0.03975573182106018, -0.0863802507519722, 0.026051046326756477, 0.2269763946533203, -0.0023323826026171446, -0.04734073951840401, 0.20890110731124878, -0.059122536331415176, 0.02561931498348713, -0.022116975858807564, 0.07037786394357681, -0.13926827907562256, 0.054667361080646515, -0.11554984748363495, 0.016211777925491333, 0.04231899976730347, -0.03130922093987465, 0.0025701520498842, 0.13858731091022491, -0.14537934958934784, 0.16859088838100433, 0.005723296198993921, 0.037940606474876404, 0.03469497337937355, 0.10158871114253998, -0.2430792599916458, -0.04718952625989914, 0.10256646573543549, -0.17210637032985687, 0.13015450537204742, 0.20324410498142242, 0.06321442872285843, 0.08721312880516052, 0.12094653397798538, 0.0271715447306633, -0.029163630679249763, -0.001183156855404377, -0.20360225439071655, -0.08257985860109329, 0.05399128422141075, 0.05513042211532593, 0.03072187677025795, 0.03439202532172203]
    # new_student.face_data.append(np.array(face_data_encoding, dtype=np.float32))


    # print("Student Face Data:", new_student.face_data)
    # print("Student Face Data Type:", type(new_student.face_data[0]))


    # studentRemote = StudentUser(
    #     name = new_student.name,
    #     email = new_student.email,
    #     face_data = new_student.face_data
        
    # )
    # new_entry = student.model_dump_for_mongo(keep_id=True) # prepare for mongo insert
    # print(new_entry)
    # print(student, type(student))

if __name__ == "__main__":
    main()