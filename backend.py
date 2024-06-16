import moviepy.editor as mp
import speech_recognition as sr
import os
import subprocess
from pydub import AudioSegment
import threading
from googletrans import Translator
from gtts import gTTS
from playsound import playsound

from moviepy.editor import VideoFileClip, AudioFileClip


def merge_video_audio(input_video, input_audio, output_file):
    # Load video and audio clips
    video_clip = VideoFileClip(input_video)
    audio_clip = AudioFileClip(input_audio)

    video_clip = video_clip.subclip(0, audio_clip.duration)
    # Set audio for the video clip
    video_clip = video_clip.set_audio(audio_clip)

    # Write the video file with merged audio
    video_clip.write_videofile(output_file, codec='libx264', audio_codec='aac', temp_audiofile='temp_audio.aac', remove_temp=True)

    # Close clips to free up resources
    video_clip.close()
    audio_clip.close()

def text_to_speech(text, lang='kn', filename='output.wav'):
    
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)
    #playsound(filename)
    

def translate_text(input_text, target_lang='kn'):
   
    translator = Translator()
    translated_text = translator.translate(input_text, dest=target_lang)
    
    return translated_text.text

def recognize_speech(audio_chunk,num):
    recognizer = sr.Recognizer()
    audio_file_name="temp"+str(num)+".wav"
    audio_chunk.export(audio_file_name, format="wav")  # Export to temporary wav file
    with sr.AudioFile(audio_file_name) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"Recognized: {text}")
        return text
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def process_chunk(chunk,num,results,translated):
    results.insert(num,recognize_speech(chunk,num))
    translated.insert(num,translate_text(results[num],'kn'))
    

def process_audio_chunks(audio_file, chunk_size_ms=10000):
    audio = AudioSegment.from_file(audio_file)
    global thread_no
    # Split audio into chunks
    chunks = []
    for i in range(0, len(audio), chunk_size_ms):
        chunk = audio[i:i + chunk_size_ms]
        chunks.append(chunk)

    # Process each chunk in a separate thread
    threads = []
    result=[]
    translated=[]
    for chunk in chunks[:]:
        thread_no+=1
        thread = threading.Thread(target=process_chunk ,args=(chunk,thread_no, result,translated))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    original= " ".join(result)
    trans=" ".join(translated)
    return original,trans

    #return result,translated
    

def convert_audio_to_wav(audio_file):
    wav_file = os.path.splitext(audio_file)[0] + '.wav'
    ffmpeg_path = 'C:\\Users\\aksha\\Downloads\\ffmpeg-master-latest-win64-gpl\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe'
    cmd = [ffmpeg_path, '-i', audio_file, '-vn', '-ar', '44100', '-ac', '2', '-b:a', '192k', wav_file]

    if not os.path.exists(ffmpeg_path):
        print(f"Error: ffmpeg not found at {ffmpeg_path}")
        return None

    try:
        subprocess.run(cmd, check=True)
        return wav_file
    except subprocess.CalledProcessError as e:
        print(f"Error converting audio to WAV: {e}")
        return None

def recognize_speech_from_video(video_file):
    if not os.path.exists(video_file):
        print(f"Error: Video file {video_file} not found")
        return

    video_clip = mp.VideoFileClip(video_file)
    audio_clip = video_clip.audio

    temp_audio_file = "temp_audio.mp3"
    audio_clip.write_audiofile(temp_audio_file)
    audio_wav_file = convert_audio_to_wav(temp_audio_file)

    if audio_wav_file:
        result_text,trans_text = process_audio_chunks(audio_wav_file)
        print("Final Recognized Text: ", result_text)
        print("Trabslated Text:",trans_text)
    else:
        print("Failed to convert audio to WAV.")
    
    # Clean up temporary files
    if os.path.exists(temp_audio_file):
        os.remove(temp_audio_file)
    if audio_wav_file and os.path.exists(audio_wav_file):
        os.remove(audio_wav_file)

    text =trans_text  # Example text in Hindi
    language = 'kn'  # any language code
    output_file = 'output.mp3'

    text_to_speech(text, lang=language, filename=output_file)
    # os.remove(output_file)  # Clean up the audio file after playing
thread_no=-1

def main():
    input_video = 'input.mp4' # Update with your video file path
    recognize_speech_from_video(input_video)
    input_audio = 'output.mp3'
    output_file = 'output_video_kannada.mp4'

    merge_video_audio(input_video, input_audio, output_file)

if __name__ == "__main__":
    main()
