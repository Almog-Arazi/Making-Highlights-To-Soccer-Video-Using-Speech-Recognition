# Making Highlights To Soccer Video Using Speech Recognition
Video Summarizer is a Python script that processes a video file, extracting the audio and identifying important moments in the video based on loudness and specific keywords like "goal". It then creates a new video file containing these important moments with an intro clip and background music.

This script was developed during the course "**From Idea to App using AI Tools,"** leveraging the ChatGPT AI language model. It uses **Google Speech Recognition** to identify the presence of specified keywords in the video's audio.

## Script Breakdown
Import necessary libraries and modules.
Set keywords to look for in audio.

####  Define several functions:
**merge_moments():** Merge loud and keyword moments into important moments.
**extract_audio():**Extract audio from the video file.
**find_loud_moments():** Find peaks in the audio file's loudness.
**find_keyword_moments():** Find moments in the video with specific keywords.
**create_video():** Create a new video file from important moments and intro video.
**add_music()**Add background music to the video.
**play_audio():** Play the audio using pygame.mixer.
**play_video():** Play the video with audio using pygame.

####Define the main() function:
Set the paths for input and output files.
Extract audio from the video file.
Find loud moments and keyword moments in the audio.
Merge loud moments and keyword moments into important moments.
Create a new video file containing important moments with an intro clip.
Add background music to the new video file.
Play the final video with audio.
Call the main() function when the script is run.

*The script is designed to work with a soccer game video, but it can be adapted for other types of videos by changing the keywords and input/output file paths.*

### Features
- Extracts important moments from an input video based on loudness and specified keywords
- Merges the extracted moments and adds an intro clip to create a summarized video
- Adds background music to the summarized video
- Plays the final video with music

### Dependencies
- moviepy
- pygame
- speech_recognition
- pydub

## Preview


https://s11.gifyu.com/images/ezgif.com-video-to-gif0436a06bc1302b19.gif

https://youtu.be/NHXYywwBJzs

[<img src="https://i9.ytimg.com/vi/NHXYywwBJzs/mqdefault.jpg?sqp=CJiS_6IG-oaymwEmCMACELQB8quKqQMa8AEB-AH-CYAC0AWKAgwIABABGFcgXChlMA8=&rs=AOn4CLBLUGxj3zbuww3pGS9ponES5x5esQ" width="50%">](https://youtu.be/NHXYywwBJzs "Preview")



