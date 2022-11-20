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
import os
import json

# model_size = st.selectbox(
#     'Which model would you like to use?',
#     ("tiny", "base", "small", "medium", "large"))

# Load whisper model
# model = whisper.load_model(model_size)
model = whisper.load_model('base')

# Define functions
def whisper_to_text(file_path):
	transcribe = model.transcribe(audio=file_path, language='en')
	segments_array = clean_transcription(transcribe)
	return segments_array

def clean_transcription(transcribe):
  """
  YouTube ending: ?t=132
  All the end of the sentence are full stops. But it also includes question marks
  This function merges sentences and timestamps
  """

  # Round timing to no dp, round down
  prev_sen_ended = True
  temp_string = ''
  temp_array = []

  # Empty array to keep timing and text
  segments_array = []

  for segment in transcribe['segments']:
    # print("Start:", math.floor(segment['start']))
    # print("End:", math.floor(segment['end']))
    # print("Text:", segment['text'])
    # print("Last text", segment['text'][-1])

    # If the segment does not end with full stop, push timing into temp_array, and update temp_string with text
    if segment['text'][-1] != '.':

      # Only key in timing if prev sentence has ended
      if prev_sen_ended == True:
        temp_array.append(math.floor(segment['start']))
      
      temp_string += segment['text']

      prev_sen_ended = False

    # If the segment ends with a full stop, ignore timing, and append temp_string with space + text
    # Push to segments_array
    # reset temp array and temp_string
    else:
      if prev_sen_ended == True:
        temp_array.append(math.floor(segment['start']))


      temp_string += segment['text']
      temp_array.append(temp_string.strip())
      segments_array.append(temp_array)
      
      # Reset temp string and array
      temp_string = ""
      temp_array = []

      # Inform that prev sentence ended
      prev_sen_ended = True

  return segments_array

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


		# Extract all files in playlist as mp3

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


		# Transcribe all with Whisper

		# Initialise empty dictionary
		transcribed_json = {}

		for mp3_path in video_path_array:
			st.write(f"Extracting from < {mp3_path.split('/')[-1]} >")
			segments_array = whisper_to_text(mp3_path)
			st.write(segments_array)
			st.write("")

			transcribed_json[mp3_path.split('/')[-1][:-4]] = segments_array

		with open('transcribed.json', 'w', encoding ='utf8') as json_file:
			json.dump(transcribed_json, json_file, ensure_ascii = False)

		print("All mp3 files transcribed and saved as json!")


		# Opening saved JSON file
		f = open('transcribed.json')
		  
		# returns JSON object as 
		# a dictionary
		transcribed_texts = json.load(f)
		st.write(transcribed_texts)
