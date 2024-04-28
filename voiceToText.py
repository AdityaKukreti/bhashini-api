import whisper

class VoiceToText:
    def __init__(self) -> None:
        self.model = whisper.load_model("base")

    def getTranscription(self, audio_data,language):
        # Load the audio data using librosa
        result = self.model.transcribe(audio_data, language=language)
        return result['text']


