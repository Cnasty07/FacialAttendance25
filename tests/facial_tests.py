import unittest
from ..src.facialSystem import facial_controller
from ..src.facialSystem.components import capture, comparison, recognition

class FacialTests(unittest.TestCase):
    def setUp(self):
        self.known_faces = facial_controller.FacialController("known_faces")
        return super().setUp()
    
    @unittest.skipIf("Not implemented", facial_controller.start_new_entry() == None)
    def test_face_recognition(self):
        self.assertTrue(True)
    
    def test_capture(self):
        self.assertTrue(True)
    
    def test_face_comparison(self):
        self.assertTrue(True)

    def tearDown(self):
        return super().tearDown()

      

if __name__ == '__main__':
    unittest.main()