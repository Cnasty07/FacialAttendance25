## TODO: To properly setup the project, you have to rebuild the wheel and upgrade setuptools using the following commands:
# 1. pip install wheel setuptools pip --upgrade
# 2. pip install git+https://github.com/ageitgey/face_recognition_models --verbose

# FIX: currently not yet implemente above commands.

from setuptools import setup, find_packages

setup(
    name='FacialAttendance',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'opencv-python',
        'dlib',
        'face_recognition',
        'pandas', 
        'scikit-learn',
        'Pillow',
        'setuptools',
        'pydantic',
        'pymongo[srv]',
        'pymongoose',
        
        
    ],
    entry_points={
        'console_scripts': [
            'facialattendance=facialattendance.__main__:main',
        ],
    },
    author='Chris Nastasi & Ruben Reyes',
    author_email='cnast01@jaguar.tamu.edu',
    description='A facial recognition based attendance system',
    url='https://github.com/Cnasty07/FacialAttendance',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)