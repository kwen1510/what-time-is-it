import streamlit as st

st.title("What time is it?")

with st.form("my_form"):
	youtube_url = st.text_input('Input YouTube URL')

# Every form must have a submit button.
	submitted = st.form_submit_button("Submit")

	if submitted:
		st.write(youtube_url)
