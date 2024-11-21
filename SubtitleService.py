import os
from whisperBackend import Transcriber


class SubtitleService:
    def __init__(self) -> None:
        self.file_path = None
        self.filetype = None
        self.translator = Transcriber()
        self.bulk = False

    def create_subtitles(
        self, file_path: str, filetypes: list[str], bulk: bool = False
    ) -> None:
        # Create subtitles for a given file.

        # Args:
        #     file_path (str): The path of the audio/video file.
        #     filetypes (list[str]): The list of file extensions for the output subtitles.
        #     bulk (bool, optional): Flag indicating whether to process multiple files in bulk. Defaults to False.
        self.file_path = file_path
        self.filetype = filetypes
        self.translator = Transcriber()
        self.bulk = bulk

        if bulk:
            # Get a list of all the audio files in the folder from the given audio/video file
            files = [f for f in os.listdir(os.path.split(self.file_path)[0]) if f.endswith(os.path.split(self.file_path)[1].split(".")[1])]
            
            # Loop over all the audio files in the folder
            path = (os.path.split(file_path)[0])
            for file in files:
                file_path = os.path.join(path, file)
                transcription_response = self.translator.transcribe(file_path, filetypes)
            return
        else: 
            transcription_response = self.translator.transcribe(self.file_path, filetypes)