import librosa
import requests
from fastapi import FastAPI

app = FastAPI()
audio_file = "input_audio/assignment_audio.wav"
min_threshold = 3000  # to skip starting 3 seconds (in milliseconds)
checker_duration = 500  # steps to check in milliseconds
end_steps = 3  # no. of stops to reach in order to break
max_duration = 50000  # max. duration in milliseconds (50 seconds)


@app.get("/")
def home():
    return {"message": "Microservice - 1"}


@app.get("/check")
def check_():
    span = 20
    length_in_milli = librosa.get_duration(path=audio_file) * 1000
    for mili in range(1, int(length_in_milli)):
        if mili % span == 0:
            body = {
                "file": audio_file,
                "sec": mili,
                "checker_duration": checker_duration,
                "min_threshold": min_threshold,
                "end_steps": end_steps,
                "max_duration": max_duration
            }
            check = requests.post("http://microservice2:8001/check", json=body).json()
            print(check, 'result')
            if check["stop"]:
                if mili >= max_duration:
                    return {"speech_exists": f"Maximum duration ({max_duration / 1000} seconds) reached...."}
                return {
                    "speech_exists": f"Breaking at: {mili / 1000}s because speech the has ended at {(mili/1000) - ((checker_duration * end_steps) / 1000)}s."}
    return {"speech_exists": False}
