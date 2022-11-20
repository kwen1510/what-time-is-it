import streamlit as st
import pathlib
from pathlib import Path
import whisper

HERE = Path(__file__).parent
print(HERE)


st.title("What Time is it?")

uploaded_file = st.file_uploader("Upload Video File", accept_multiple_files=False)

model_size = 'tiny'

model = whisper.load_model(model_size)

print("hello world")

if uploaded_file is not None:
	file_name = uploaded_file.name
	print(file_name)
	print("Transcribing...")
	transcription = model.transcribe(f"{HERE}/{file_name}", language = 'en')
	print("Done with transcription!")
