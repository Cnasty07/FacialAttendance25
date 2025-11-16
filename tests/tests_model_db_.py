import pytest

import src.controllers.remoteDatabaseController as rdc
import src.models.User as user_model

def test_student_model_creation():
    with pytest.raises(user_model.ValidationError):
        student_instance = user_model.StudentUser(
            name="",
            email="invalidemail",
            enrolled_classes=[],
            face_data=[]
        )
        assert student_instance is None

def test_mongo_connection():
    with pytest.raises(ConnectionError):
        db_controller = rdc.StudentDatabaseController()
        assert db_controller.get_collection("Student") is not None
    