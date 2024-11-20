import os
from fastapi import FastAPI

app = FastAPI()

#main code 
@app.get("/")
def read_root():
    return {"Hello": "World"}


def main():
    pass

if __name__ == '__main__':
    main() 
