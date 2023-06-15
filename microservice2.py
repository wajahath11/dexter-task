import librosa
from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()
num = 0
ended = 0
stop = False


class Details(BaseModel):
    file: str
    sec: int
    checker_duration: int
    min_threshold: int
    end_steps: int
    max_duration: int


@app.get("/")
def home():
    return {"message": "Microservice - 2"}


@app.post("/check")
def check_someone_talking(details: Details):
    n = num + details.sec  # max/end time
    global ended
    global stop
    if n % details.checker_duration == 0 and n > details.min_threshold:
        if n >= details.max_duration:
            stop = True
            return {"stop": stop}
        audio, sample_rate = librosa.load(details.file)
        start_time = (n - details.checker_duration) / 1000
        end_time = n / 1000
        start_sample = int(start_time * sample_rate)
        end_sample = int(end_time * sample_rate)

        audio_segment = audio[start_sample:end_sample]
        rms = librosa.feature.rms(y=audio_segment)

        # Check if there is significant energy in the segment
        is_speaking = (rms > 0.01).any()

        if is_speaking:
            ended = 0
        else:
            ended += 1
            if ended == details.end_steps:
                stop = True
        return {"stop": stop}
    return {"stop": stop}
