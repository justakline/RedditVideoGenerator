
from gtts import gTTS
from pydub import AudioSegment
import wave
from vosk import Model, KaldiRecognizer
import json
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont, ImageColor
import random
import os
from googletrans import Translator, LANGUAGES



def translateText(script, language):
    translator = Translator()
    translated_text = translator.translate(script, src="en", dest=language).text
    return translated_text

# Create the audio, save it as an audiio file, and make sure it is the correct format
def textToSpeech(script, title="audio.wav", language="en"):
    """Different Languages"""
    
    tts = gTTS(text=script, lang=language)
    tts.save(f"{title}")
    (AudioSegment.from_file(title)).export(title, format="wav")
    
# audio_file_name (String): path to the audio file
# model (Model from vosk): the speech to text model
# segments (List) : where the list of the transcribed audio and timestamps will be stored
def trancscribeAudioWithTimestamps(audio_file_name, model, segments ):
    results = []
    with wave.open(audio_file_name, "rb") as wf:
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)  # Enable word-level timestamps
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                results.append(json.loads(rec.Result()))

        results.append(json.loads(rec.FinalResult()))
        wf.close()
    # Parse the results
    for result in results:
        if 'result' in result:
            for word_info in result['result']:
                segments.append({
                    'text': word_info['word'],
                    'start': word_info['start'],
                    'end': word_info['end']
                })
    
                

    
    # end_trying = False
    # while(not end_trying):
    #     try:
    #         os.remove(audio_file_name)
    #         end_trying = True
    #     except:
    #         pass
            
    
                
    ############   Format of segments   ###############
    """
    [
        {text: "", start: 0, end: 1},
        {text: "", start: 1, end:2},
    ...
    ]
    """

# segments (List) : where the list of the transcribed audio and timestamps is stored
# video_dimensions (Tuple[Int, Int]): Dimensions of the video
# text_clips (List): List of text_clips created by this function
def createTextClips(segments, video_dimensions ,text_clips, language = 'en'):
    font_size = int(0.1354 * video_dimensions[0])
    video_font = "Arial-Bold"
    
    match language:
        case "zh-CN":
            video_font = "./fonts/zh-CN.ttc"
        case "hi":
            video_font = "./fonts/hi.ttf"
        
    for seg in segments:
        clip = TextClip(seg['text'],font=video_font, fontsize=font_size, color='white', stroke_color="black",stroke_width=2, bg_color='transparent', size=video_dimensions, method="caption", align="center")
        clip.start = float(seg['start'])
        clip.duration = (float(seg['end']) - float(seg['start']))
        clip.end = float(seg['end'])
        clip.set_position("center")
        text_clips.append(clip)


# Creates the intro card as a .png using a script
def createIntroCard(script, file_name, width, language="en"):
    # Define the size of the image
    header_font_size = int(width*0.0443)
    header_x = int(width*0.1231)
    body_font_size = int(width*0.0591)
    body_line_start = int(width*0.1231)
    image_size = int( width*0.0492)
    
    font = ImageFont.truetype('arialbd.ttf', body_font_size)
    match language:
        case "zh-CN":
            font = ImageFont.truetype('./fonts/zh-CN.ttc', body_font_size) 
        case "hi":
            font = ImageFont.truetype('./fonts/hi.ttf', body_font_size) 
    

        
    body_text = script
    body_text = body_text.split(" ")
    body_text = [t + " " for t in body_text]
    
    # Body Text
    # for wrapping
    line_spacing = body_font_size
    line_number = 0
    line = ""
    lines = []
    for i in range(0, len(body_text)):
        if(font.getlength(line + str(body_text[i])) < width):
            line += body_text[i]
        else:
            lines.append([line, body_line_start + (line_spacing*line_number) ])
            line_number +=1
            line = body_text[i]
        if (i == len(body_text) -1):
            lines.append([line, body_line_start + (line_spacing*line_number) ])

    
    height = int(lines[-1][1] + 4*line_spacing)
    
    background_color = (255, 255, 255)
    text_color = (0, 0, 0)
    
    
    
    # Create a new blank image
    image = Image.new('RGB', (width, height), color = background_color)
    draw = ImageDraw.Draw(image)


    for l in lines:
        draw.text( (10, l[1]), l[0], fill=text_color, font=font)
        
    
    # Load a font
    font = ImageFont.truetype('arial.ttf', header_font_size)    
    # Reddit Post Header
    header_text = f"{random.choice([
    'r/LetsNotMeet',
    'r/NoSleep',
    'r/ShortStories',
    'r/WritingPrompts',
    'r/LifeProTips',
    'r/Relationships',
    'r/Parenting',
    'r/ProRevenge',
    'r/PettyRevenge',
    'r/EntitledParents',
    'r/TIFU',  
    'r/UnresolvedMysteries',
    'r/Confessions',
    'r/AmItheAsshole',
    'r/TwoXChromosomes',  
    'r/OffMyChest',
    'r/TrueOffMyChest'

])}"
    draw.text((header_x, 10), header_text, fill= (163, 163, 163  ), font=font)
    
    section_text = f"u/{randomUserGenerator()} - {random.randint(1,8)}y"
    draw.text((header_x, 10+int(header_font_size)), section_text, fill= (44, 179, 226 ), font=font)
        

    # Interaction counts
    
  
    font = ImageFont.truetype('arial.ttf', header_font_size)
  
 
    
    image.paste(Image.open("./assets/reddit.png").resize([int(image_size*1.8) ,int(image_size*1.8 )]), ( 10,10 ))
    
    image.paste(Image.open("./assets/up_arrow.png").resize([image_size ,image_size ]), ( int(width/25) - image_size,height- int(font.size *1.5) ))
    interactions_text = f"{ str(random.randint(1,100)) +"k"} "
    draw.text((width/25, height- int( font.size *1.5)), interactions_text, fill=text_color, font=font)
    image.paste(Image.open("./assets/down_arrow.png").resize([image_size ,image_size ]), ( int(width/35 + font.getlength(interactions_text) + width/100),height-  int(font.size *1.5 )))
   
    interactions_text = f"{str(random.randint(1,100)) +"k"} "
    image.paste(Image.open("./assets/comment.png").resize([image_size ,image_size ]), ( int(9*width/20-image_size),height-  int(font.size *1.5)))
    draw.text((9*width/20, height-  int( font.size *1.5)), interactions_text, fill=text_color, font=font)
    
    interactions_text = f"Share"
    image.paste(Image.open("./assets/share.png").resize([image_size ,image_size ]), ( int(7*width/8-image_size),height- int( font.size *1.5)))
    draw.text((7*width/8, height-  int( font.size *1.5)), interactions_text, fill=text_color, font=font)
    

    # Save the image
    image.save(file_name)

def randomUserGenerator():
     # Some common words used in usernames
    words = ['gamer', 'dude', 'girl', 'queen', 'king', 'noob', 'pro', 'player', 'shadow', 'hunter', 'warrior', 'ninja', 'wizard', 'ranger', 'rookie', 'veteran', 'champion', 'master', 'ace', 'legend', 'ghost', 'dragon', 'tiger', 'bear', 'wolf', 'eagle', 'lion', 'fish', 'hawk', 'horse', 'monkey', 'snake', 'bird', 'shark', 'cat', 'dog']

    # Randomly choose a word
    word = random.choice(words)
    
    word += random.choice(words) if random.random() < 0.9 else ''
    word += random.choice(words) if random.random() < 0.4 else ''

    # Randomly decide to add a number at the end (50% chance)
    number = str(random.randint(0, 99)) if random.random() < 0.5 else ''

    # Randomly decide to add a prefix like 'xX', 'xx', 'oO', etc (20% chance)
    prefix = random.choice(['xX', 'xx', 'oO', 'oo', '_']) if random.random() < 0.45 else ''

    # Randomly decide to add a suffix like 'Xx', 'xX', 'Oo', etc (20% chance)
    suffix = random.choice(['Xx', 'xX', 'Oo', 'oo', '_']) if random.random() < 0.3 else ''

    # Combine to create a username
    username = f"{prefix}{word}{number}{suffix}"
    return username