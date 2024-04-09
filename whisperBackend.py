from datetime import timedelta
import os
import whisper
import Constants

class FileCreater:
    # takes the transcription and writes it into a subtitle format file, only formats implemented by whisper work
    def format_writer(self, filepath: str, output_extension, transcription_response, file_language_name = ""):
        path, file_name = os.path.split(filepath)
        output_filename = file_name.split(".")[0] + "_" + file_language_name + "." + output_extension
        output_writer = whisper.utils.get_writer(output_extension, path)
        output_writer(transcription_response, output_filename)


# Translates given and also transcribes at the same time 
class Translator:
    def __init__(self) -> None:
        self.model = whisper.load_model(Constants.model_size)
        
    # Transcribes and Translates the given file (Audio or Video)
    def translate(self, filepath: str, language: str)-> dict[str, str | list]:
        translate_response = self.model.transcribe(filepath, language = language, verbose = False)
        return translate_response