import json
from moviepy.editor import *
from vosk import Model, KaldiRecognizer

from helper import *
from createVideo import *
from generateStory import *
from questions import questions, story_types, adjectives
from random import randint
import time




def createVideo(question, script, story_type, adjective, background_video, language, relative_folder):
    model = Model(f"./vosk_models/{language}")
    background_start = []
    translated_question = translateText(question, language)
    translated_post = translateText(script, language)
    intro_video = createIntroOfVideo(translated_question, model, background_video, background_start, language)
    body_video = createBodyOfVideo(translated_post, model, background_video, background_start, language)
    full_video  = createFinalVideo([intro_video, body_video])
    full_video.write_videofile(f"{relative_folder}final_output_{story_type}_{adjective}_{language}.mp4", fps=24, audio=True)





question = questions[randint(0, len(questions)-1)]
story_type= story_types[randint(0, len(story_types)-1)]
adjective = adjectives[randint(0, len(adjectives)-1)]
current_time = time.asctime()
relative_folder = f"./videos/{current_time}"

script = generateStory(question, story_type, adjective)

background_video = VideoFileClip("./assets/minecraft.mp4", audio=False, target_resolution=(1440, 812))

# Start [] shows where the next clip should start for a smooth transition
languages = ["en", "es", "fr", "de", "pt", "zh-CN", "hi"]
languages = ["hi", "zh-CN"]
languages = ["en"]



for language in languages:
    # break
    # threading.
    createVideo(question, script, story_type,adjective,background_video,language,relative_folder)
    




