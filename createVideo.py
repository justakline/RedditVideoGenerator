from helper import *
import random





def createIntroOfVideo(model, background_video, start ):
    audio_file_name = "intro_audio.wav"
    
    script = "How big is your penis?"

    # Convert text to speech
    textToSpeech(script, audio_file_name)
    audio_file = AudioFileClip(audio_file_name)
    
    # Transcribe audio with timestamps
    segments = []
    trancscribeAudioWithTimestamps(audio_file_name, model, segments)
    
    # Creating the question box
    intro_card_file_name = "reddit_post_image.png"
    createIntroCard(script, intro_card_file_name, background_video.size[0])
    
    # Create the image Clip
    intro_image = ImageClip(intro_card_file_name)
    intro_image.duration = segments[-1]["end"] 
    intro_image.start = 0
    intro_image = intro_image.set_position("center")
    intro_image = intro_image.set_audio(audio_file)
    
    
    # Load the background video and make it smaller
    random_start = random.randint(1, int(background_video.duration)- 10*60)
    background_video = background_video.subclip(random_start, random_start +  intro_image.duration )
    
    # Composite the video clip ontop of the background video
    print(background_video.size)
    intro_video = CompositeVideoClip([background_video, intro_image], size=background_video.size)
    intro_video.duration = background_video.duration

    intro_video.write_videofile("video.mp4", fps=24, audio=True)
    
    # For the next video clip
    start  = intro_image.duration
    






def createBodyOfVideo(script,model, background_video, start ):
    
   
    audio_file_name = "audio.wav"

    # Convert text to speech
    textToSpeech(script, audio_file_name)
    audio_file = AudioFileClip(audio_file_name)



    # Transcribe audio with timestamps
    segments = []
    trancscribeAudioWithTimestamps(audio_file_name, model, segments)

    # Load background clip
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