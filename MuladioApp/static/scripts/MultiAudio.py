import pytube # Used for downloading Youtube of videos
import openai # Used for text genertion task (here it is used for translation of original audio transcript into target language)
import whisper # Used for generating transcript of user specified audio/video
from pydub import AudioSegment # Used for manipulating Audio Files like (adding silence, trimming audio, speeding up audio)
from gtts import gTTS # Used for text-speech purposes in various languages
from gtts.lang import tts_langs
import re
from ... import config

class MultiAudio:

    LANGUAGES = tts_langs() # dictionary of languages supported by gtts alongwith language codes

    def __init__(self):

        openai.api_key = config.OPENAI_API_KEY

        self.t_lang = ""

        self.video_time_length = 0


    def downloadAudio(self, url):
        # Downloading audio of youtube video in the form of a file
        video = pytube.YouTube(url)
        audio = video.streams.get_audio_only()
        audioFilePath = audio.download('./MuladioApp/static/res/audios/','original.mp4')
        self.video_time_length = video.length
        return audioFilePath
    
    def transcribeAudio(self,audioFilePath):
        # Transcribing Audio File
        model = whisper.load_model("tiny")
        transcript = model.transcribe(audioFilePath,word_timestamps=True)
        return transcript

    def translateSegText(self, segment_text):

        chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": f"You are a helpful translating assistant for translating user messages into {self.t_lang}."},
                {"role":"assistant", "content": f"Translate given text into {self.t_lang}.\nText:\n" + segment_text}
                
            ]
        )

        translated_text = chat_completion['choices'][0]['message']['content']

        return translated_text

    def textToSpeech(self,transcript):

        transcript_segments = transcript['segments']

        prev_segment_end = 0.0

        full_audio = AudioSegment.silent(duration=0.0)

        for no, segment in enumerate(transcript_segments):

          start = segment['start']

          end = segment['end']

          seg_text = segment['text']

          transalted_text = self.translateSegText(seg_text)

          seg_audio = gTTS(text=transalted_text, lang=self.t_lang)

          seg_audio.save(f"./MuladioApp/static/res/audios/{no}.mp3")

          audio = AudioSegment.from_file(f"./MuladioApp/static/res/audios/{no}.mp3")

          if prev_segment_end != start:

                    # Define the length of silence to add in milliseconds
                    silence_duration = (start - prev_segment_end) * 1000

                    # Generate a silent audio segment of the desired duration
                    silence_segment = AudioSegment.silent(duration=silence_duration)

                    # Concatenate the silent segment to the beginning of the audio file
                    audio_with_silence = silence_segment + audio

                    full_audio += audio_with_silence

          else:

                    full_audio += audio
          
          prev_segment_end = end

        
        if prev_segment_end != self.video_time_length:

            # Define the length of silence to add in milliseconds
            silence_duration = (self.video_time_length - prev_segment_end) * 1000

            # Generate a silent audio segment of the desired duration
            silence_segment = AudioSegment.silent(duration=silence_duration)

            # Concatenate the silent segment to the beginning of the audio file
            full_audio =  full_audio + silence_segment
        

        return full_audio

    def get_youtube_video_id(self, url):
        # regular expression pattern for extracting the video ID from a YouTube video URL
        pattern = r"^(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=))([\w-]{11})(?:\S+)?$"
        
        # use the pattern to extract the video ID from the URL
        match = re.match(pattern, url)
        
        # if the match is not None, return the video ID
        if match is not None:
            return match.group(1)
        else:
            return None

    def generateAudio(self,url, target_lang):
       
        # Generate audio of youtube video in target language

        video_id = self.get_youtube_video_id(url)
            
        if video_id == None:
            return "Invalid Youtube Video URL."

        try:

           self.t_lang = next(key for key, val in MultiAudio.LANGUAGES.items() if target_lang.lower() == val.lower())

        except:

            return "Invalid/Unsupported Language."
        

        try:

            audioFilePath = self.downloadAudio(url)

            transcriptOfAudio = self.transcribeAudio(audioFilePath)
            
            translatedTranscriptAudio = self.textToSpeech(transcriptOfAudio)

            translatedTranscriptAudio.export("./MuladioApp/static/res/audios/target/translated_audio.mp3", format="mp3")

            return translatedTranscriptAudio.duration_seconds, video_id
        
        except Exception as e:
            
            print(e)
            return "Error Occurred."

# obj = MultiAudio()
# obj.generateAudio(url='https://www.youtube.com/watch?v=5uiUz1_HsFg',target_lang='URDU')