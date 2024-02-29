from helper import *
import random





def createIntroOfVideo(question, model, background_video, background_start, language="en" ):
    audio_file_name = f"{language}_intro_audio.wav"
    
    # Convert text to speech
    textToSpeech(question, audio_file_name, language)
    audio_file = AudioFileClip(audio_file_name)
    
    # Transcribe audio with timestamps
    segments = []
    trancscribeAudioWithTimestamps(audio_file_name, model, segments)
    
    # Creating the question box
    intro_card_file_name = "./assets/reddit_post_image.png"
    createIntroCard(question, intro_card_file_name, background_video.size[0], language)
    
    # Create the image Clip
    intro_image = ImageClip(intro_card_file_name)
    intro_image.duration = segments[-1]["end"] 
    intro_image = intro_image.set_position("center")
    intro_image = intro_image.set_audio(audio_file)
    
    
    # Load the background video and make it smaller
    random_start = random.randint(1, int(background_video.duration)- 10*60)
    bg = background_video.subclip(random_start, random_start +  intro_image.duration + 1 )
    background_start.append(random_start +  intro_image.duration + 1 )
    
    
    # Composite the video clip ontop of the background video
    intro_video = CompositeVideoClip([bg, intro_image], size=bg.size)
    intro_video.duration = bg.duration
   

    return intro_video
    

def createBodyOfVideo(script,model, background_video, background_start, language = "en"):
    audio_file_name = f"{language}_body_audio.wav"

    # Convert text to speech
    textToSpeech(script, audio_file_name, language)
    audio_file = AudioFileClip(audio_file_name)



    # Transcribe audio with timestamps
    segments = []
    trancscribeAudioWithTimestamps(audio_file_name, model, segments)

    # Load background clip
    video_duration = segments[-1]['end']
    bg = background_video.subclip(background_start[-1], background_start[-1] + video_duration + 1)

    # Create text clips for each segment
    text_clips =[]
    createTextClips(segments, bg.size, text_clips, language)
    body_video = CompositeVideoClip([bg] + text_clips, size=bg.size)
   
    # Add audio
    body_video.audio = audio_file

    # Export the final video
    body_video.duration = bg.duration
    return body_video

# Composite together all the video clips
def createFinalVideo(videos):
    total_duration = 0
    for video in videos:
        total_duration += video.duration

    # Make sure the timing of the video/audio of each clips corresponds correctly
    videos[0].end =  videos[0].start + videos[0].duration
    for i in range(1, len(videos)):
        videos[i].start =  videos[i-1].end
        videos[i].end =  videos[i].start + videos[i].duration 
        videos[i].audio.start =  videos[i].start
        videos[i].audio.end =  videos[i].audio.start + videos[i].audio.duration
        
    full_video = CompositeVideoClip(videos, size=videos[0].size)
    full_video.duration = total_duration
    return full_video