import os
import dlib


def is_gpu_available() -> bool:
    """Checks if a compatible GPU is available for dlib to use.

    Returns:
        bool: True if a compatible GPU is available, False otherwise.
    """
    try:
        os.add_dll_directory(os.environ['CUDA_PATH'])
        dlib.DLIB_USE_CUDA = True
        print("Cuda detected. Using GPU acceleration.")
        return True
    except Exception as e:
        print("Cuda not detected. Defaulting to cpu.", e)
        return False