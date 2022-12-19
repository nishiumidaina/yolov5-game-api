import os
import pafy
from fastapi import FastAPI
import subprocess
from subprocess import PIPE
from pydantic import BaseModel

class GreetingModel(BaseModel):
    detect_mode: int
    detect_class: int

app = FastAPI()

@app.post("/detect/")
async def detect(int: GreetingModel):
    proc = subprocess.run('python yolov5/detect.py', stdout=PIPE, stderr=PIPE, shell=True)
    proc_str = eval(proc.stdout.decode('utf-8'))

    return proc_str