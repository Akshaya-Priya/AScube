# Video Speech Translation and Dubbing

## Overview
This project processes a video file by extracting speech, converting it to text, translating it into a target language (Kannada), converting the translated text into speech, and merging the generated audio back with the original video. The project utilizes Python and several libraries for speech recognition, translation, and video processing.

## Features
- Extracts audio from a video file.
- Converts speech to text using Google Speech Recognition.
- Translates the extracted text into Kannada using Google Translate.
- Converts the translated text into speech using gTTS.
- Merges the generated audio with the original video.

## Prerequisites
Ensure the following dependencies are installed:

```sh
pip install moviepy speechrecognition googletrans==4.0.0-rc1 gtts playsound pydub
```

Additionally, download and install [FFmpeg](https://ffmpeg.org/download.html) and ensure its binary path is correctly set in the script.

## Usage

1. Place the input video file (`input.mp4`) in the project directory.
2. Run the script using:

```sh
python script.py
```

3. The processed video with translated and dubbed audio will be saved as `output_video_kannada.mp4`.

## Functions Explanation

### `merge_video_audio(input_video, input_audio, output_file)`
Merges the translated and dubbed audio with the original video.

### `text_to_speech(text, lang, filename)`
Converts translated text into speech and saves it as an audio file.

### `translate_text(input_text, target_lang)`
Translates input text into the specified target language (Kannada by default).

### `recognize_speech(audio_chunk, num)`
Processes audio chunks to recognize and convert speech to text.

### `process_audio_chunks(audio_file, chunk_size_ms=10000)`
Splits the audio file into chunks and processes them for speech recognition and translation.

### `convert_audio_to_wav(audio_file)`
Converts an audio file to WAV format using FFmpeg.

### `recognize_speech_from_video(video_file)`
Extracts audio from the video, processes speech-to-text conversion, translates text, generates audio, and initiates the dubbing process.

### `main()`
Orchestrates the complete process from speech extraction to video generation.

## Notes
- Ensure that `ffmpeg.exe` is available in the specified path.
- If `gtts` or `playsound` fails, try installing alternative text-to-speech libraries like `pyttsx3`.
- The script processes audio in chunks to improve accuracy and efficiency.

## License
This project is open-source and can be modified as needed.

