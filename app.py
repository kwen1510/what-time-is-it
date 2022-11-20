import streamlit as st
import pathlib
from pathlib import Path
import whisper

HERE = Path(__file__).parent
print(HERE)


st.title("What Time is it?")

uploaded_mp4_file = st.file_uploader("Upload Video File", accept_multiple_files=False)

model_size = 'tiny'

model = whisper.load_model(model_size)

print("hello world")

# When mp4 file uploaded
if uploaded_mp4_file is not None:

	filename = pathlib.Path(uploaded_mp4_file.name).stem
	
	mp4_file_path = HERE / f'./{filename}_binaries.mp4'

	with open(mp4_file_path, 'wb') as binary_file:
		video_bytes = uploaded_mp4_file.getvalue()
		binary_file.write(video_bytes)

	with open(mp4_file_path, "rb") as file:
		download_video_bytes = file.read() # read a byte (a single character in text)
		# print(download_video_bytes)

	transcription = model.transcribe(f"{HERE}/{file_name}", language = 'en')
	st.write("Done with transcription!")
