import streamlit as st

st.title("What time is it?")

with st.form("my_form"):
	youtube_url = st.text_input('Input YouTube URL', "https://www.youtube.com/playlist?list=PL1n2-n-o82sxNG4r2GyOQ7iX3Kg9KBz1s")

# Every form must have a submit button.
	submitted = st.form_submit_button("Submit")

	if submitted:
		st.write(youtube_url)
