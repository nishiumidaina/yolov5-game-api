import os
import shutil
import datetime
import pafy
import cv2
from fastapi import FastAPI
from fastapi.responses import FileResponse
import subprocess
from subprocess import PIPE
from pydantic import BaseModel

app = FastAPI()

class GreetingModel(BaseModel):
    detect_id: int
    detect_url: str

@app.post('/detect/')
async def detect(text:GreetingModel):
    dir_path = 'target_images/%s' % text.detect_id
    basename = 'camera_capture_cycle'
    ext = 'jpg'
    
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)

    video = pafy.new(text.detect_url)
    best = video.getbest(preftype="mp4")
    cap = cv2.VideoCapture(best.url)
    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)
    ret, frame = cap.read()
    cv2.imwrite('{}_{}.{}'.format(base_path, datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'), ext), frame)

    proc = subprocess.run('python yolov5/detect.py --source %s --project %s' % (dir_path, dir_path), stdout=PIPE, stderr=PIPE, shell=True)
    proc_str = eval(proc.stdout.decode('utf-8'))

    return proc_str 

@app.get('/image/')
async def bicycle(id: int = 0):
    file = os.listdir('./target_images/%s/exp' % id)

    return FileResponse('./target_images/%s/exp/%s' % (id, file[0]))