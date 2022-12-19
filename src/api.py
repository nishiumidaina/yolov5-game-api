import os
import datetime
import pafy
import cv2
from fastapi import FastAPI
import subprocess
from subprocess import PIPE
from pydantic import BaseModel

app = FastAPI()

class GreetingModel(BaseModel):
    detect_url: str
    detect_mode: int
    detect_class: int

@app.post("/detect/")
async def detect(text:GreetingModel):
    dir_path = 'target_images'
    basename = 'camera_capture_cycle'
    ext = 'jpg'

    video = pafy.new(text.detect_url)
    best = video.getbest(preftype="mp4")
    cap = cv2.VideoCapture(best.url)
    
    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    ret, frame = cap.read()
    img_path = cv2.imwrite('{}_{}.{}'.format(base_path, datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'), ext), frame)

    '''
        proc = subprocess.run('python yolov5/detect.py', stdout=PIPE, stderr=PIPE, shell=True)
        proc_str = eval(proc.stdout.decode('utf-8'))

    '''
    return text.detect_url