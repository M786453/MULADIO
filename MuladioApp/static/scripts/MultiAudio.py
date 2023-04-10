import pytube # Used for downloading Youtube of videos
import openai # Used for text genertion task (here it is used for translation of original audio transcript into target language)
from pydub import AudioSegment # Used for manipulating Audio Files like (adding silence, trimming audio, speeding up audio)
from gtts import gTTS # Used for text-speech purposes in various languages
from gtts.lang import tts_langs
import re
from ... import config

class MultiAudio:

    LANGUAGES = tts_langs() # dictionary of languages supported by gtts alongwith language codes

    AUDIOS_DIRECTORY_PATH = "./MuladioApp/static/res/audios/"

    OUTPUT_AUDIO_PATH = AUDIOS_DIRECTORY_PATH + "target/translated_audio.mp3"

    def __init__(self):

        openai.api_key = config.OPENAI_API_KEY

        self.t_lang = ""

        self.video_time_length = 0



    def downloadAudio(self, url):
        # Downloading audio of youtube video in the form of a file
        video = pytube.YouTube(url)
        audio = video.streams.get_audio_only()
        audioFilePath = audio.download(self.AUDIOS_DIRECTORY_PATH,'original.mp4')
        self.video_time_length = video.length
        return audioFilePath



    def transcribeAudio(self,audioFilePath):
        # Transcribing Audio File
        audioFile = open(audioFilePath, 'rb')
        transcript = openai.Audio.translate('whisper-1', audioFile,response_format='srt')
        return transcript



    def combineTranscriptText(self, transcript):

      # Splitting srt file into segments of texts
      segments_raw = transcript.split('\n\n')

      # Storing time and text of each segment
      transcript_segments = [segment.split('\n')[1:] for segment in segments_raw if len(segment.split('\n'))==3]

      combined_text = ""

      # Combining text and timestamps of each segment together
      for segment in transcript_segments:

          seg_text = segment[1]

          timestamp = segment[0]

          start, end = timestamp.split(' --> ')

          start = self.time_to_seconds(start)

          end = self.time_to_seconds(end)
          
          combined_text += seg_text + " [" + str(start) + ":" + str(end) + '] '


      return combined_text


    def chatGptTranslate(self, text):
        #translate text into user specified language using Chatgpt
        #It is slower than text-davinci-003 but results are quite better.
        #It's api cost is quite less than text-davinci-003 model
        chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": f"You are a helpful translating assistant for translating user messages into {self.t_lang}."},
                {"role":"assistant", "content": f"Translate given text into {self.t_lang}.\nText:\n" + text}
                
            ]
        )

        translated_text = chat_completion['choices'][0]['message']['content']

        return translated_text
    
    def devinciTranslate(self, text):
      #translate text into user specified language using GPT-3 text-davinci-003 Model
      #It is faster than chatgpt completion but results are not good than chatgpt
      #It's api cost is quite more than chatgpt
      response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Translate following text into {self.t_lang} and do not repeat translation:\n{text}\nTranslation:\n",
        temperature=0,
        max_tokens=2035,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
      )

      return response['choices'][0]['text']


    def textToSpeech(self,translated_text):

        translated_text_segments = translated_text.split("]")
        
        prev_segment_end = 0.0

        full_audio = AudioSegment.silent(duration=0.0)

        # Converting each segment's text into speech
        # Combining each segment's speech with full_audio in order to get complete audio
        for no, segment in enumerate(translated_text_segments):

            try:
                text, time = segment.split("[")

                start, end = time.split(":")

                start, end = float(start), float(end)

                print("start", start, "end", end)

                seg_audio = gTTS(text=text, lang=self.t_lang)

                seg_audio.save( self.AUDIOS_DIRECTORY_PATH + f"{no}.mp3")

                audio = AudioSegment.from_file(self.AUDIOS_DIRECTORY_PATH + f"{no}.mp3")

                print(audio.duration_seconds)

                #If there is any gap between end of previous segment and start of current segment
                #then create a silence segment and add it in start of current segment's audio 
                #and combine it with full_audio
                if prev_segment_end != start:

                          # Define the length of silence to add in milliseconds
                          silence_duration = (start - prev_segment_end) * 1000
                          print("silence duration",silence_duration)
                          # Generate a silent audio segment of the desired duration
                          silence_segment = AudioSegment.silent(duration=silence_duration)

                          # Concatenate the silent segment to the beginning of the audio file
                          audio_with_silence = silence_segment + audio

                          full_audio += audio_with_silence

                else:

                          full_audio += audio
                
                prev_segment_end = end

            except Exception as e:

              print(e)

        # If 
        if prev_segment_end != self.video_time_length:

            # Define the length of silence to add in milliseconds
            silence_duration = (self.video_time_length - prev_segment_end) * 1000

            # Generate a silent audio segment of the desired duration
            silence_segment = AudioSegment.silent(duration=silence_duration)

            # Concatenate the silent segment to the beginning of the audio file
            full_audio =  full_audio + silence_segment
        

        return full_audio

    def time_to_seconds(self,time_str):
        # Split the time string into hours, minutes, seconds, and milliseconds
        parts = time_str.split(':')
        seconds_parts = parts[2].split(',')
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(seconds_parts[0])
        milliseconds = int(seconds_parts[1])
        
        # Convert the time to seconds
        total_seconds = (hours * 3600) + (minutes * 60) + seconds + (milliseconds / 1000)
        
        return total_seconds

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

            combinedTextWithTimestamps = self.combineTranscriptText(transcriptOfAudio)

            # translatedText = self.devinciTranslate(combinedTextWithTimestamps)

            translatedText = self.chatGptTranslate(combinedTextWithTimestamps)

            print(translatedText)

            translatedTranscriptAudio = self.textToSpeech(translatedText)

            translatedTranscriptAudio.export(self.OUTPUT_AUDIO_PATH, format="mp3")

            return translatedTranscriptAudio.duration_seconds, video_id
        
        except Exception as e:
            
            print(e)
            return "Error Occurred."

# obj = MultiAudio()
# obj.generateAudio(url='https://www.youtube.com/watch?v=5uiUz1_HsFg',target_lang='URDU')