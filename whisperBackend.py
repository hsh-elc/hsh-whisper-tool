import os
from numpy import unicode_
import stable_whisper
import Constants
from faster_whisper import WhisperModel
import torch
import math


def convert_seconds_to_hms(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = math.floor((seconds % 1) * 1000)
    output = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{milliseconds:03}"
    return output


# Translates given and also transcribes at the same time 
class Transcriber:
    def __init__(self) -> None:
        os.environ['KMP_DUPLICATE_LIB_OK']='True'
        torch.cuda.is_available()
        self.model = stable_whisper.load_faster_whisper(Constants.model_size)
        
    # Transcribes and Translates the given file (Audio or Video)
    def transcribe(self, filepath: str, filetypes)-> dict[str, str | list]:
        self.segments, info = self.model.transcribe(filepath)
        segmentList = list(self.segments)
        for filetype in filetypes:

            if filetype == "srt":
                self.createSrt(filepath, segmentList)

            if filetype == "vtt":
                self.createVtt(filepath, segmentList)
                

    def createSrt(self, filepath: str, segments):
        count = 0
        with open(filepath.split(".")[0] + ".srt", 'w') as f:  # Open file for writing
            for segment in segments:
                count +=1
                duration = f"{convert_seconds_to_hms(segment.start)} --> {convert_seconds_to_hms(segment.end)}\n"
                text = f"{segment.text.lstrip()}\n\n"

                f.write(f"{count}\n{duration}{text}")  # Write formatted string to the file
                print(f"{duration}{text}",end='')
            f.close()

    def createVtt(self, filepath: str, segments):
        with open(filepath.split(".")[0] + ".vtt", 'w') as f:  # Open file for writing
            f.write("WEBVTT\n\n")
            for segment in segments:
                duration = f"{convert_seconds_to_hms(segment.start)} --> {convert_seconds_to_hms(segment.end)}\n"
                text = f"{segment.text.lstrip()}\n\n"

                f.write(f"{duration}{text}")  # Write formatted string to the file
                print(f"{duration}{text}",end='')
            f.close()