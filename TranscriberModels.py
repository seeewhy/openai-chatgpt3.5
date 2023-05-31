import openai
import whisper
import os
import torch

def get_model(use_api):
    if use_api:
        return APIWhisperTranscriber()
    else:
        return WhisperTranscriber()

class WhisperTranscriber:
    def __init__(self):
        self.lang = "en"
        self.audio_model = self.load_model()
        print(f"[INFO] Whisper using GPU: " + str(torch.cuda.is_available()))

    def get_transcription(self, wav_file_path):
        try:
            result = self.audio_model.transcribe(wav_file_path, fp16=torch.cuda.is_available(), language = self.lang)
        except Exception as e:
            print(e)
            return ''
        return result['text'].strip()
    
    def change_lang(self, language):
        self.lang = language
        self.load_model() 
       
    def load_model(self):
         if self.lang == "en":
            self.audio_model = whisper.load_model(os.path.join(os.getcwd(), 'tiny.en.pt'))
            return self.audio_model
         else:
            self.audio_model = whisper.load_model(os.path.join(os.getcwd(), 'tiny.pt'))
            return self.audio_model 

class APIWhisperTranscriber:
    def get_transcription(self, wav_file_path):
        try:
            with open(wav_file_path, "rb") as audio_file:
                result = openai.Audio.translate("whisper-1", audio_file)
        except Exception as e:
            print(e)
            return ''
        return result['text'].strip()