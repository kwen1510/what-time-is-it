import streamlit as st
from pytube import YouTube  # !pip install pytube
from pytube.exceptions import RegexMatchError
from tqdm.auto import tqdm  # !pip install tqdm
import whisper
import math
import whisper
import ffmpeg
import subprocess
import base64

# Load whisper model
model = whisper.load_model("base")

# Streamlit stuff goes here
st.title("What time is it?")

with st.form("my_form"):
	playlist_url = st.text_input('Input YouTube URL',"https://www.youtube.com/playlist?list=PL1n2-n-o82sxNG4r2GyOQ7iX3Kg9KBz1s")

# Every form must have a submit button.
	submitted = st.form_submit_button("Submit")

	if submitted:

		video_path_array = []

		st.write("Extracting YouTube playlist")

		from pytube import Playlist, YouTube
		playlist = Playlist(playlist_url)
		metadata = []
		for video in playlist:
		  metadata.append(YouTube(video))

		# for meta in metadata:
		#   print(dir(meta))

		reconstructedMeta = [ 
		    {
		      "title": meta.title, 
		      "description": meta.description, 
		      "url": f"https://youtu.be/{meta.video_id}", 
		      "keywords": meta.keywords, 
		      "author": meta.author, 
		      "publishedData": meta.publish_date, 
		      "ChannelId": meta.channel_url[31:], 
		      "videoId": meta.video_id 
		     } for meta in metadata]

		# st.write(reconstructedMeta)

		# where to save
		save_path = "./mp3"

		for i, row in enumerate(reconstructedMeta):
		    # url of video to be downloaded
		    url = row['url']

		    # try to create a YouTube vid object
		    try:
		        yt = YouTube(url)
		    except RegexMatchError:
		        print(f"RegexMatchError for '{url}'")
		        continue

		    itag = None
		    # we only want audio files
		    files = yt.streams.filter(only_audio=True)
		    for file in files:

		        # print(file.mime_type)

		        # and of those audio files we grab the first audio for mp4 (eg mp3)
		        if file.mime_type == 'audio/mp4':
		            itag = file.itag
		            break
		    if itag is None:
		        # just incase no MP3 audio is found (shouldn't happen)
		        print("NO MP3 AUDIO FOUND")
		        continue

		    # get the correct mp3 'stream'
		    stream = yt.streams.get_by_itag(itag)
		    # downloading the audio
		    stream.download(output_path=save_path, filename=f"{row['title']}.mp3")

		    video_path_array.append(f"{save_path}/{row['title']}.mp3")


		st.write("All mp3 files extracted")

		for mp3_path in video_path_array:
			st.write(f"Extracting from {mp3_path.split('/')[-1]}")
			transcription = model.transcribe(mp3_path, language = 'en')
			st.write(transcription['text'])
			st.write("")
