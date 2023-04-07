from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .static.scripts.MultiAudio import MultiAudio
import json
import os
# Create your views here.
def muladio(request):
    template = loader.get_template("muladio.html")
    return HttpResponse(template.render())



def generate(request):

    try:

        mulit_audio = MultiAudio()
        
        url = request.GET["url-input"]

        lang = request.GET['lang']

        if len(url) == 0 or len(lang) == 0:

            return HttpResponse("URL/LANG FIELD EMPTY.")
        
        output = mulit_audio.generateAudio(url, lang)
        
        if type(output) == str:
            
            # If type of output is str, it means it is error description

            if output == "Invalid/Unsupported Language.":

                return HttpResponse("Invalid/Unsupported Language.")
            
            elif output == "Invalid Youtube Video URL.":

                return HttpResponse("Invalid Youtube Video URL.")
            
            elif output == "Error Occurred.":

                return HttpResponse("Error Occurred.")
        
        else:


            audio_length, video_id = output

            data = {
                'video_id': video_id,
                'audio_length':audio_length
            }

            return HttpResponse(json.dumps(data))
    
    except Exception as e:
        print(e)
        return HttpResponse("Error Occured.")


def clean(request):
    
    audio_directory_path = "./MuladioApp/static/res/audios"

    translated_audio_path = "./MuladioApp/static/res/audios/target/translated_audio.mp3"


    # Removing translated file
    try:

        if os.path.isfile(translated_audio_path):

            os.remove(translated_audio_path)
    
    except:

        return HttpResponse("Error removing translated file.")

    # Removing original and segment audios
    for filename in os.listdir(audio_directory_path):

        try:
            
            file_path = os.path.join(audio_directory_path, filename)

            if os.path.isfile(file_path):

                os.remove(file_path)

                print(f"File '{filename}' removed successfuly")
            
        except:

            return HttpResponse("Error removing file.")
    
    return HttpResponse("Cleaned successfuly.")

    





