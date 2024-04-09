import os
from whisperBackend import Translator
from whisperBackend import FileCreater


class SubtitleService:
    def __init__(self) -> None:
        self.file_path = None
        self.languages = None
        self.filetype = None
        self.translator = Translator()
        self.bulk = False

    def create_subtitles(
        self, file_path: str, languages: list[str], filetypes: list[str], bulk: bool = False
    ) -> None:
        # Create subtitles for a given file.

        # Args:
        #     file_path (str): The path of the audio/video file.
        #     languages (list[str]): The list of languages to translate the subtitles into.
        #     filetypes (list[str]): The list of file extensions for the output subtitles.
        #     bulk (bool, optional): Flag indicating whether to process multiple files in bulk. Defaults to False.
        self.file_path = file_path
        self.languages = languages
        self.filetype = filetypes
        self.translator = Translator()
        self.file_creater = FileCreater()
        self.bulk = bulk

        if bulk:
            # Get a list of all the audio files in the folder from the given audio/video file
            files = [f for f in os.listdir(os.path.split(self.file_path)[0]) if f.endswith(os.path.split(self.file_path)[1].split(".")[1])]
            
            # Loop over all the audio files in the folder
            path = (os.path.split(file_path)[0])
            for file in files:
                file_path = os.path.join(path, file)
                for language in self.languages:
                    # Translate the audio file to the specified language
                    transcription_response = self.translator.translate(file_path, str(language))
                    
                    # Create a file with the specified file extensions for each language
                    for extension in filetypes:
                        self.file_creater.format_writer(
                            file_path, extension, transcription_response, language
                        )
            return

        # Transcribe and translate the video and create the output files with the specified file extensions
        for language in self.languages:
            # Translate the video to the specified language
            transcription_response = self.translator.translate(self.file_path, str(language))
            
            # Create a file with the specified file extensions for each language
            for extension in filetypes:
                self.file_creater.format_writer(
                    file_path, extension, transcription_response, language
                )
