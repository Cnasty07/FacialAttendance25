import os
from abc import ABC, abstractmethod

import bson
import numpy as np

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.collection import Collection
from pymongo.database import Database

import pydantic
from src.models import User
# python -m pip install "pymongo[srv]"

# INFO: This is the Database Controller for MongoDB using pymongo

# TODO: Finish implementing CRUD operations and add concurrency for non-blocking calls.


class RemoteDatabaseControllerBase:
    def __init__(self) -> None:
        self.client = MongoClient(host=os.getenv(
            "MONGO_URI"), server_api=ServerApi("1"), connect=True)
        self.db = self.client["EmbeddedAppData"]
        self.collection: Collection

    def get_database(self):
        try:
            self.db = self.client["EmbeddedAppData"]
            return self.db
        except Exception as e:
            print("Error connecting to database:", e)
            return None

    def get_collection(self, collection: str):
        try:
            self.collection = self.db[collection]
            return self.collection
        except Exception as e:
            print("Error getting collection:", e)
            return None

    def get_single_student(self, student_email: str):
        user_collection = self.db["Student"].find_one({"email": student_email})
        return user_collection

    def get_all_classes(self):
        classes_collection = self.db["Classes"].find()
        return list(classes_collection)


class StudentDatabaseController(RemoteDatabaseControllerBase):
    def get_single_student(self, student_email: str):
        return super().get_single_student(student_email)

    def get_enrolled_classes(self, student_email: str):
        student = self.db["Student"].find_one({"email": student_email})
        if student:
            return student.get("enrolled_classes", [])
        return []

    def get_student_face_data(self, student_email: str):
        student = self.db["Student"].find_one({"email": student_email})
        if student:
            return student.get("face_data", [])
        return []

    def update_student_face_data(self, student_email: str, new_face_data: list):
        result = self.db["Student"].update_one(
            {"email": student_email},
            {"$set": {"face_data": new_face_data}}
        )
        return result.modified_count > 0

    def update_student_enrolled_classes(self, student_email: str, new_classes: list):
        result = self.db["Student"].update_one(
            {"email": student_email},
            {"$set": {"enrolled_classes": new_classes}}
        )
        return result.modified_count > 0


# Testing Purposes
def main():
    dbc = StudentDatabaseController()
    # collection = db.get_collection("Classes").find()
    # for doc in collection:
    #     doc_id = doc["name"]
    #     print(doc_id)
    # print(db.get_single_student("chris@facialattendance.com"))

    ## FIXME: Need to figure out how to convert numpy arrays to lists for Pydantic compatibility and mongo insertion
    # testing adding ruben student
    new_student = User.StudentUser(
        name="Ruben Reyes",
        email="rreyes@tamusa.edu",
        enrolled_classes=[],
        face_data=[np.array([-0.020214959979057312, 0.04823107272386551, 0.09015103429555893, -0.050497930496931076, 0.025843920186161995, -0.005287497770041227, -0.04980546608567238, -0.0991913229227066, 0.11601994931697845, -0.14017634093761444, 0.22910569608211517, -0.012691516429185867, -0.19086889922618866, -0.0739898607134819, -0.021474061533808708, 0.16852112114429474, -0.16225256025791168, -0.15294978022575378, -0.07976768165826797, -0.06346189230680466, 0.05949011817574501, -0.011332922615110874, -0.06966444849967957, 0.053340595215559006, -0.17387016117572784, -0.3367103338241577, -0.056988805532455444, -0.08749478310346603, -0.03600757569074631, -0.07037677615880966, -0.0673011764883995, -0.0008221145253628492, -0.1566217690706253, 0.007236035540699959, -0.02518971636891365, 0.03944769874215126, -0.08303820341825485, -0.11732520908117294, 0.16082611680030823, 0.06531994789838791, -0.1244097501039505, 0.0426800511777401, 0.026970194652676582, 0.26371484994888306, 0.22457686066627502, 0.021907398477196693, 0.061527881771326065, -0.04934816062450409, 0.1638544201850891, -0.28010526299476624, 0.04651135206222534, 0.11192744225263596, 0.13790948688983917, 0.12156731635332108, 0.1084631159901619, -0.1438412070274353, -0.023742375895380974, 0.06660439074039459, -0.09450268000364304, 0.08894098550081253, 0.0022377909626811743, 0.008467938750982285, 0.017094042152166367, -0.09421052038669586,
                            0.18049709498882294, 0.052815962582826614, -0.1745525747537613, -0.0214040819555521, 0.11100216209888458, -0.1013927087187767, -0.08328315615653992, -0.06060859188437462, -0.1324283629655838, -0.20514164865016937, -0.3079852759838104, 0.06844553351402283, 0.34967362880706787, 0.17323115468025208, -0.23701614141464233, -0.0392506867647171, -0.05896873027086258, 0.004965668078511953, 0.1080223023891449, 0.0337168350815773, -0.044890109449625015, -0.03975573182106018, -0.0863802507519722, 0.026051046326756477, 0.2269763946533203, -0.0023323826026171446, -0.04734073951840401, 0.20890110731124878, -0.059122536331415176, 0.02561931498348713, -0.022116975858807564, 0.07037786394357681, -0.13926827907562256, 0.054667361080646515, -0.11554984748363495, 0.016211777925491333, 0.04231899976730347, -0.03130922093987465, 0.0025701520498842, 0.13858731091022491, -0.14537934958934784, 0.16859088838100433, 0.005723296198993921, 0.037940606474876404, 0.03469497337937355, 0.10158871114253998, -0.2430792599916458, -0.04718952625989914, 0.10256646573543549, -0.17210637032985687, 0.13015450537204742, 0.20324410498142242, 0.06321442872285843, 0.08721312880516052, 0.12094653397798538, 0.0271715447306633, -0.029163630679249763, -0.001183156855404377, -0.20360225439071655, -0.08257985860109329, 0.05399128422141075, 0.05513042211532593, 0.03072187677025795, 0.03439202532172203]), np.array([0.4, 0.5, 0.6]]
    )
    studentjson = new_student.model_dump()
    print(studentjson.keys())
    dbc.db["Student"].insert_one(studentjson)
    print(dbc.db["Student"].find_one({"email": "rreyes@tamusa.edu"}))

    # dbc.close()


if __name__ == "__main__":
    main()
