import os
from numpy import unicode_
import Constants
import torch
import math
import whisperx
import gc


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
        self.device = "cuda" 
        self.batch_size = 16 # reduce if low on GPU mem
        compute_type = "float16" # change to "int8" if low on GPU mem (may reduce accuracy)
        self.model = whisperx.load_model("large-v2", self.device, compute_type=compute_type)
        
    # Transcribes and Translates the given file (Audio or Video)
    def transcribe(self, filepath: str, filetypes)-> dict[str, str | list]:
        try:
            audio = whisperx.load_audio(filepath)
            result = self.model.transcribe(audio, batch_size=self.batch_size)

            print(result["segments"])

            #model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=self.device)
            #result = whisperx.align(result["segments"], model_a, metadata, audio, self.device, return_char_alignments=False)

            #print(result["segments"])
            segmentList = result["segments"]

            for filetype in filetypes:

                if filetype == "srt":
                    self.createSrt(filepath, segmentList)

                if filetype == "vtt":
                    self.createVtt(filepath, segmentList)
        except Exception:
                exit

    def createSrt(self, filepath: str, segments):
        count = 0
        with open(filepath.split(".")[0] + ".srt", 'w') as f:  # Open file for writing
            for idx, segment in enumerate(segments, 1):
                duration = f"{convert_seconds_to_hms(segment['start'])} --> {convert_seconds_to_hms(segment['end'])}\n"
                text = f"{segment['text'].lstrip()}\n\n"

                f.write(f"{idx}\n{duration}{text}")  # Write formatted string to the file
                print(f"{duration}{text}",end='')
            f.close()

    def createVtt(self, filepath: str, segments):
        with open(filepath.split(".")[0] + ".vtt", 'w') as f:  # Open file for writing
            f.write("WEBVTT\n\n")
            for segment in segments:
                duration = f"{convert_seconds_to_hms(segment['start'], True)} --> {convert_seconds_to_hms(segment['end'], True)}\n"
                text = f"{segment['text'].lstrip()}\n\n"

                f.write(f"{duration}{text}")  # Write formatted string to the file
                print(f"{duration}{text}",end='')
            f.close()