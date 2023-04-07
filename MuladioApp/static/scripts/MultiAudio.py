import pytube # Used for downloading Youtube of videos
import openai # Used for text genertion task (here it is used for translation of original audio transcript into target language)
import whisper # Used for generating transcript of user specified audio/video
from pydub import AudioSegment # Used for manipulating Audio Files like (adding silence, trimming audio, speeding up audio)
from gtts import gTTS # Used for text-speech purposes in various languages
import re
from ... import config

class MultiAudio:

    LANGUAGES = {
    "en": "english",
    "zh": "chinese",
    "de": "german",
    "es": "spanish",
    "ru": "russian",
    "ko": "korean",
    "fr": "french",
    "ja": "japanese",
    "pt": "portuguese",
    "tr": "turkish",
    "pl": "polish",
    "ca": "catalan",
    "nl": "dutch",
    "ar": "arabic",
    "sv": "swedish",
    "it": "italian",
    "id": "indonesian",
    "hi": "hindi",
    "fi": "finnish",
    "vi": "vietnamese",
    "he": "hebrew",
    "uk": "ukrainian",
    "el": "greek",
    "ms": "malay",
    "cs": "czech",
    "ro": "romanian",
    "da": "danish",
    "hu": "hungarian",
    "ta": "tamil",
    "no": "norwegian",
    "th": "thai",
    "ur": "urdu",
    "hr": "croatian",
    "bg": "bulgarian",
    "lt": "lithuanian",
    "la": "latin",
    "mi": "maori",
    "ml": "malayalam",
    "cy": "welsh",
    "sk": "slovak",
    "te": "telugu",
    "fa": "persian",
    "lv": "latvian",
    "bn": "bengali",
    "sr": "serbian",
    "az": "azerbaijani",
    "sl": "slovenian",
    "kn": "kannada",
    "et": "estonian",
    "mk": "macedonian",
    "br": "breton",
    "eu": "basque",
    "is": "icelandic",
    "hy": "armenian",
    "ne": "nepali",
    "mn": "mongolian",
    "bs": "bosnian",
    "kk": "kazakh",
    "sq": "albanian",
    "sw": "swahili",
    "gl": "galician",
    "mr": "marathi",
    "pa": "punjabi",
    "si": "sinhala",
    "km": "khmer",
    "sn": "shona",
    "yo": "yoruba",
    "so": "somali",
    "af": "afrikaans",
    "oc": "occitan",
    "ka": "georgian",
    "be": "belarusian",
    "tg": "tajik",
    "sd": "sindhi",
    "gu": "gujarati",
    "am": "amharic",
    "yi": "yiddish",
    "lo": "lao",
    "uz": "uzbek",
    "fo": "faroese",
    "ht": "haitian creole",
    "ps": "pashto",
    "tk": "turkmen",
    "nn": "nynorsk",
    "mt": "maltese",
    "sa": "sanskrit",
    "lb": "luxembourgish",
    "my": "myanmar",
    "bo": "tibetan",
    "tl": "tagalog",
    "mg": "malagasy",
    "as": "assamese",
    "tt": "tatar",
    "haw": "hawaiian",
    "ln": "lingala",
    "ha": "hausa",
    "ba": "bashkir",
    "jw": "javanese",
    "su": "sundanese",
}

    def __init__(self):

        openai.api_key = config.OPENAI_API_KEY

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


    def combineTranscriptText(self,transcript):
        # Combining transcript text alongwith timestamps
        transcript_segments = transcript['segments']
        transcript_text = ""
        for segment in transcript_segments:
            transcript_text += segment['text'] + "[" + str(segment['start']) + ":" + str(segment['end']) + ']'
        
        print(transcript_text)
        return transcript_text



    def translateTranscriptText(self,transcript_text, target_language):
        # Translating transcript into urdu
        chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": f"You are a helpful translating assistant for translating user messages into {target_language}."},
                {"role":"assistant", "content": f"Translate given text into {target_language}.\nText:\n" + transcript_text}
                
            ]
        )
        translated_text = chat_completion['choices'][0]['message']['content']

        return translated_text



    def textToSpeech(self,translated_text, target_lang):
        # Converting translated text into audio
        # Also filling the silence gaps in transalted audio which are present in original audio

        translated_text_segments = translated_text.split("]")

        print(translated_text)

        print("target language:", target_lang)

        prev_segment_end = 0.0

        full_audio = AudioSegment.silent(duration=0.0)

        for no, segment in enumerate(translated_text_segments):

            try:

                text, time = segment.split("[")

                start, end = time.split(":")

                start, end = float(start), float(end)

                seg_audio = gTTS(text=text, lang=target_lang)

                seg_audio.save(f"./MuladioApp/static/res/audios/{no}.mp3")

                # Load the audio file
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
                
            except Exception as e:
                print(e)


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

            language = next(key for key, val in MultiAudio.LANGUAGES.items() if target_lang.lower() == val)

            print(language)

        except:

            return "Invalid Language."
        

        try:
            audioFilePath = self.downloadAudio(url)

            transcriptOfAudio = self.transcribeAudio(audioFilePath)

            combinedTranscriptText = self.combineTranscriptText(transcriptOfAudio)

            translatedTranscriptText = self.translateTranscriptText(combinedTranscriptText, language)
            

            translatedTranscriptAudio = self.textToSpeech(translatedTranscriptText,language)

            translatedTranscriptAudio.export("./MuladioApp/static/res/audios/target/translated_audio.mp3", format="mp3")

            return translatedTranscriptAudio.duration_seconds, video_id
        
        except Exception as e:
            print(e)
            return "Error Occurred."

# obj = MultiAudio()
# obj.generateAudio(url='https://www.youtube.com/watch?v=5uiUz1_HsFg',target_lang='URDU')