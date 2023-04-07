# MULADIO

MULADIO is a web application built using Python Django that enables users to watch YouTube videos in their preferred language. The application aims to eliminate the language barrier on the YouTube platform, allowing users to access videos from around the world in their native language. By providing this service, MULADIO seeks to increase the accessibility of YouTube content and expand the reach of content creators to a global audience.

## Table of Contents

- [Prerequisite](#Prerequisite)
- [Development](#Development)

## Prerequisite

Following are the prerequisite APIs and libraries for MULADIO:

* Openai's Whisper
        
                pip install git+https://github.com/openai/whisper.git

* Openai's Chat Completion API
        
                pip install openai

* Pytube
        
                pip install pytube

* Pydub
                
                pip install pydub

* GTTS
                
                pip install gtts
                

## Development

MULADIO's primary features rely on cutting-edge technologies such as Openai's Whisper, Google's GTTS library, and Openai's Chat Completion API. Whisper is utilized to transcribe the audio of YouTube videos, while Chat Completion API is used to translate the transcript. GTTS library is leveraged to convert text into speech in any language. Additionally, Pytube library is used to download YouTube videos' audio, and Pydub is used to manipulate audio files, such as combining, trimming, silencing, or speeding up audios. 


