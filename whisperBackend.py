import os
from numpy import unicode_
import stable_whisper
import Constants
from faster_whisper import WhisperModel
import torch
import math


def convert_seconds_to_hms(seconds, is_vtt: bool = False):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = math.floor((seconds % 1) * 1000)
    separator = '.' if is_vtt else ','
    output = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}{separator}{milliseconds:03}"
    return output


# Translates given and also transcribes at the same time 
class Transcriber:
    def __init__(self) -> None:
        os.environ['KMP_DUPLICATE_LIB_OK']='True'
        torch.cuda.is_available()
        self.model = stable_whisper.load_faster_whisper(Constants.model_size, device="cuda", compute_type="int8")
        
    # Transcribes and Translates the given file (Audio or Video)
    def transcribe(self, filepath: str, filetypes)-> dict[str, str | list]:
        loops: int = 0
        loops + 1 
        try:
            self.segments, info = self.model.transcribe(filepath)
            segmentList = list(self.segments)
            for filetype in filetypes:

                if filetype == "srt":
                    self.createSrt(filepath, segmentList)

                if filetype == "vtt":
                    self.createVtt(filepath, segmentList)
        except Exception:
            if loops < 4 :
                self.transcribe(filepath, filetypes)
            else:
                exit

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
                duration = f"{convert_seconds_to_hms(segment.start), True} --> {convert_seconds_to_hms(segment.end), True}\n"
                text = f"{segment.text.lstrip()}\n\n"

                f.write(f"{duration}{text}")  # Write formatted string to the file
                print(f"{duration}{text}",end='')
            f.close()