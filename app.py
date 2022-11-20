import whisper
import pathlib
from pathlib import Path
from tempfile import NamedTemporaryFile
import streamlit as st
import ffmpeg
from moviepy.editor import *

HERE = Path(__file__).parent
# print(HERE)

# Functions

def mp4tomp3(mp4file, mp3file):
	videoclip=VideoFileClip(mp4file)
	audioclip=videoclip.audio
	audioclip.write_audiofile(mp3file)
	audioclip.close()
	videoclip.close()

st.title("What Time is it?")

uploaded_mp4_file = st.file_uploader("Upload Video File", accept_multiple_files=False)

model = whisper.load_model("base")

# When mp4 file uploaded
if uploaded_mp4_file is not None:
	
	st.write("Transcribing...")
	
	with NamedTemporaryFile(suffix="mp3") as temp:
		st.write(uploaded_mp4_file.getvalue())
# 		mp4tomp3("Calorimetry.mp4","audio.mp3")
# 		temp.write(uploaded_mp4_file.getvalue())
# 		temp.seek(0)
# 		result = model.transcribe(temp.name)
# 		st.write(result["text"])
		
		
# 	filename = pathlib.Path(uploaded_mp4_file.name).stem
	
# 	mp4_file_path = HERE / f'./{filename}_binaries.mp4'

# 	with open(mp4_file_path, 'wb') as binary_file:
# 		video_bytes = uploaded_mp4_file.getvalue()
# 		binary_file.write(video_bytes)
		
# 		st.write(mp4_file_path)

# 	transcription = model.transcribe(mp4_file_path, language = 'en')

# 	st.write(transcription['text'])	
# 	st.write("Done with transcription!")
