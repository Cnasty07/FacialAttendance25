from dataclasses import dataclass
import numpy as np
import bson
from abc import ABC, abstractmethod

@dataclass(init=True, repr=True)
class Face:
    student_id: bson.ObjectId
    class_id: bson.ObjectId
    face_encoding: np.ndarray


def main():
    pass

if __name__ == "__main__":
    main()