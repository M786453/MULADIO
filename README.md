# MULADIO

MULADIO is a web application built using Python Django that enables users to watch YouTube videos in their preferred language. The application aims to eliminate the language barrier on the YouTube platform, allowing users to access videos from around the world in their native language. By providing this service, MULADIO seeks to increase the accessibility of YouTube content and expand the reach of content creators to a global audience.

## Table of Contents

- [Development](#Development)
- [Environment Setup](<Environment Setup>)
    - [Virtual Environment](<Virtual Environment>)
    - [Prerequisites](Prerequisites)
    - [Running on Localhost](<Running on Localhost>)

## Development

MULADIO's primary features rely on cutting-edge technologies such as Openai's Whisper, Google's GTTS library, and Openai's Chat Completion API. Whisper is utilized to transcribe the audio of YouTube videos, while Chat Completion API is used to translate the transcript. GTTS library is leveraged to convert text into speech in any language. Additionally, Pytube library is used to download YouTube videos' audio, and Pydub is used to manipulate audio files, such as combining, trimming, silencing, or speeding up audios. 

## Environment Setup

Following is the complete procedure to setup and run this project on your local environment.

### Virtual Environment

Create a virtual environment:

Windows:

            py -m venv MULADIO-VENV
            
Linux:

            python -m venv MULADIO-VENV 
           
Activate environment:

Windows/Linux:

Run `activate` executable in order to activate virtual environment.

            ./MULADIO-VENV/Scripts/activate

            
            
### Cloning MULADIO

Clone MULADIO in recently created MULADIO-VENV directory.

            git clone https://github.com/M786453/MULADIO.git


### Prerequisites

You should have following in your virtual environment:

* Openai's Whisper
        
                py -m pip install git+https://github.com/openai/whisper.git
Note: In order to run whisper, you must have `ffmpeg` installed and path of it's executable in environment variables.

* Openai's API
        
                py -m pip install openai

* Pytube
        
                py -m pip install pytube

* Pydub
                
                py -m pip install pydub

* GTTS
                
                py -m pip install gtts

### Runing on Localhost

Navigate in MULADIO project directory and run following command:

        py manage.py runserver

This will run MULADIO on localhost. Now you can access MULADIO using url given in your command line.
