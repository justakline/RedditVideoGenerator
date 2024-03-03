import json
from moviepy.editor import *
from vosk import Model, KaldiRecognizer

from helper import *
from createVideo import *
from generateStory import *
import questions




def createVideo(language):
    model = Model(f"./vosk_models/{language}")
    background_start = []
    translated_question = translateText(question, language)
    translated_post = translateText(script, language)
    intro_video = createIntroOfVideo(translated_question, model, background_video, background_start, language)
    body_video = createBodyOfVideo(translated_post, model, background_video, background_start, language)
    full_video  = createFinalVideo([intro_video, body_video])
    full_video.write_videofile(f"final_output_{language}.mp4", fps=24, audio=True)





script = """I embarked on an adventure that I had been dreaming about for years: skydiving. The thrill of free-falling through the sky, the rush of adrenaline, and the ultimate test of courage were all things I craved. So, on a seemingly ordinary weekend, I decided it was time to turn this dream into reality. I was a bit nervous, of course, but the excitement far outweighed any fear.

After arriving at the skydiving center, I went through a brief training session. They taught us how to position our bodies during the fall and, most importantly, how to deploy our parachutes. "Listen carefully," the instructor said, "in the rare event your main chute doesn't open, you need to know how to use your reserve." I listened intently, memorizing every step, never actually believing I would need to use that knowledge.

The plane ride up was filled with anticipation. As we reached altitude, the instructor gave us the signal, and one by one, we jumped. The sensation of jumping out of a plane is indescribable. The cold rush of air, the deafening roar in my ears, and the ground so far below that it seemed like a different world.

Then, the moment I feared happened. I pulled the cord to deploy my parachute, but nothing happened. I was in free fall, and my main parachute had failed. Panic surged through me, but then, clarity. I remembered the instructions for deploying the reserve chute. With a deep breath, I pulled the reserve cord, and to my immense relief, it opened, slowing my descent to a safe landing speed.

As I floated down, the world below me slowly coming into focus, I felt a mix of emotions. Fear, relief, exhilaration, and above all, a profound appreciation for life. When my feet finally touched the ground, I was overwhelmed with gratitude. I had faced one of my greatest fears and survived.

This experience, while terrifying, taught me invaluable lessons about courage, resilience, and the importance of preparation. It was a reminder that life is fragile and should be lived to the fullest. Would I skydive again? It might take some time before I answer that question, but one thing is for certain: I will never forget the day I danced with danger and lived to tell the tale"""

question = questions[0]
script = generateStory()

question = "What is the scariest moment of your life?"

background_video = VideoFileClip("./assets/minecraft.mp4", audio=False, target_resolution=(1440, 812))

# Start [] shows where the next clip should start for a smooth transition

languages = ["en", "es", "fr", "de", "pt", "zh-CN", "hi"]
languages = ["hi", "zh-CN"]



for language in languages:
    # break
    # threading.
    createVideo(language)
    




