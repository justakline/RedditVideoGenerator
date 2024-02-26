from helper import *
import random





def createIntroOfVideo(model):
    audio_file_name = "intro_audio.wav"
    
    script = "how did you lose your laptop?"

    # Convert text to speech
    textToSpeech(script, audio_file_name)
    audio_file = AudioFileClip(audio_file_name)
    
    # Transcribe audio with timestamps
    segments = []
    trancscribeAudioWithTimestamps(audio_file_name, model, segments)
    
    pass






def createBodyOfVideo(script,model ):
    
   
    audio_file_name = "audio.wav"

    # Convert text to speech
    textToSpeech(script, audio_file_name)
    audio_file = AudioFileClip(audio_file_name)



    # Transcribe audio with timestamps
    segments = []
    trancscribeAudioWithTimestamps(audio_file_name, model, segments)

    # Load background clip
    background_video = VideoFileClip("./videos/minecraft.mp4")
    background_video.size = (406,720)
    video_duration = segments[-1]['end']
    random_start = random.randint(1, int(background_video.duration)-  int(video_duration))
    background_video = background_video.subclip(random_start, random_start + video_duration + 1)

    # Create text clips for each segment
    text_clips =[]
    createTextClips(segments, background_video.size, text_clips)
    body_video = CompositeVideoClip([background_video] + text_clips, size=background_video.size)
   
    # Add audio
    body_video.audio = audio_file

    # Export the final video
    body_video.duration =background_video.duration
    return body_video

def createFinalVideo(intro_video, body_video):
    pass