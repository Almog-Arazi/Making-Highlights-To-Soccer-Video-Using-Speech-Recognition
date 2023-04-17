
import warnings
import os
import threading
import time
import pygame
import speech_recognition as sr
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip
from pydub import AudioSegment

# Ignore warnings from dependencies
warnings.filterwarnings("ignore")
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    
# Keywords to look for in audio
KEYWORDS = ["magnificent", "brilliant", "stunning", "goall", "gool", "goal", "wow", "sensational", "beauty"]

# Merge loud and keyword moments into important moments
def merge_moments(loud_moments, keyword_moments, tolerance=3000):
    important_moments = []
    merged_moments = sorted(loud_moments + keyword_moments)

    for moment in merged_moments:
        if not important_moments:
            important_moments.append(moment)
        else:
            last_moment = important_moments[-1]
            if moment - last_moment >= tolerance or moment in keyword_moments:
                important_moments.append(moment)

    return important_moments

# Extract audio from video file
def extract_audio(video_file_path):
    video = VideoFileClip(video_file_path)
    audio_file_path = "audio.wav"
    video.audio.write_audiofile(audio_file_path)
    video.audio.close()
    return audio_file_path

# Find peaks moments in audio file
def find_loud_moments(audio_file_path, min_duration):
    audio = AudioSegment.from_wav(audio_file_path)
    loudness = audio.dBFS
    important_moments = []
    start_time = None
    for i, chunk in enumerate(audio[::30]):
        if chunk.dBFS >= loudness - 30:
            if start_time is None:
                start_time = i * 30
        elif start_time is not None:
            duration = i * 30 - start_time
            if duration >= min_duration:
                important_moments.append(start_time)
            start_time = None
    return important_moments

# Find moments in video with specific keywords
def find_keyword_moments(video_file_path, keywords, chunk_duration=5):
    video = VideoFileClip(video_file_path)
    audio = video.audio
    audio_duration = int(audio.duration)
    temp_files = []
    keyword_moments = []

    r = sr.Recognizer()

    # Split audio into chunks and check for keywords in each chunk
    for i in range(0, audio_duration, chunk_duration):
        audio_chunk = audio.subclip(i, min(i + chunk_duration, audio_duration))
        audio_chunk_file_path = f"temp_audio_{i}.wav"
        audio_chunk.write_audiofile(audio_chunk_file_path)
        temp_files.append(audio_chunk_file_path)

        # Transcribe audio and look for keywords
        with sr.AudioFile(audio_chunk_file_path) as source:
            audio_data = r.record(source)
            try:
                text = r.recognize_google(audio_data)
                for keyword in keywords:
                    if keyword.lower() in text.lower():
                        keyword_moments.append(i * 1000)  # Convert to milliseconds
                        print(f"Recognized '{keyword}' at chunk time: {i} seconds")
                        break
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print(f"Error at time {i}-{min(i+chunk_duration, audio_duration)} seconds; {e}")
    # Clean up temporary audio files
    for temp_file in temp_files:
        os.remove(temp_file)

    return keyword_moments

#create video clip
def create_video(video_file_path, important_moments, output_video_file_path, intro_video_file_path):
    intro_clip = VideoFileClip(intro_video_file_path)
    clips = [intro_clip]

     # Loop through each important moment and extract a 6 second clip starting from that moment
    for moment in important_moments:
        start_time = moment / 1000
        end_time = start_time + 6
        clip = VideoFileClip(video_file_path).subclip(start_time, end_time)
        clips.append(clip)
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_video_file_path, fps=25)
    final_clip.close()

def add_music(video_file_path, music_file_path, output_with_music_file_path):
    video = VideoFileClip(video_file_path)
    audio = AudioFileClip(music_file_path)
    audio = audio.subclip(0, video.duration)
    final_clip = video.set_audio(audio)
    final_clip.write_videofile(output_with_music_file_path)
    final_clip.close()

# Initialize the mixer and load the audio file
 # Start playing the audio
def play_audio(audio_file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file_path)
    pygame.mixer.music.play()

def play_video(video_file_path):
    clip = VideoFileClip(video_file_path)
    audio_file_path = "temp_audio.wav"
    clip.audio.write_audiofile(audio_file_path)
    audio_thread = threading.Thread(target=play_audio, args=(audio_file_path,))
    audio_thread.start()

    pygame.init()
    pygame.display.set_caption(os.path.basename(video_file_path))
    screen = pygame.display.set_mode((clip.size[0], clip.size[1]))

    clock = pygame.time.Clock()
    quit_flag = False
    for t in range(int(clip.duration * clip.fps)):
        if quit_flag:
            break

        frame_image = clip.get_frame(t / clip.fps)
        frame_surface = pygame.surfarray.make_surface(frame_image.swapaxes(0, 1))
        screen.blit(frame_surface, (0, 0))
        pygame.display.flip()
        clock.tick(clip.fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_flag = True
                break

    pygame.event.post(pygame.event.Event(pygame.QUIT))
    
    pygame.mixer.music.stop()
    pygame.quit()
    os.remove(audio_file_path)

 # Set the paths to the input and output files
def main():
    video_file_path = "soccer_game-short.mp4"
    min_duration = 1000
    output_video_file_path = "output.mp4"
    output_with_music_file_path = "output_with_music.mp4"
    music_file_path = "music.mp3"
    intro_video_file_path = "almog_intro.wmv"

    audio_file_path = extract_audio(video_file_path)
    loud_moments = find_loud_moments(audio_file_path, min_duration)
    keyword_moments = find_keyword_moments(video_file_path, KEYWORDS)

    important_moments = merge_moments(loud_moments, keyword_moments)
    important_moments.sort()

    for i, moment in enumerate(important_moments):
        timestamp = time.strftime("%H:%M:%S", time.gmtime(moment / 1000))
        print(f"Important Moment {i + 1}: {timestamp}")

    create_video(video_file_path, important_moments, output_video_file_path, intro_video_file_path)
    add_music(output_video_file_path, music_file_path, output_with_music_file_path)
    play_video(output_with_music_file_path)

if __name__ == "__main__":
    main()


