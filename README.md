# YouTube Video Question Answering App

This is a Python application that allows users to ask questions related to the content of a YouTube video and receive answers based on the video's captions. The application uses OpenAI's GPT model to process the captions and answer the user's question.

## Dependencies

To use this app, you will need the following libraries installed:

- openai
- pytube
- gradio
- langchain
- youtube_transcript_api

You can install these libraries using pip:

pip install openai pytube gradio langchain youtube_transcript_api


## Usage

1. Obtain an API key for OpenAI's GPT model.
2. Set the `OPENAI_API_KEY` environment variable with your API key:

```bash
export OPENAI_API_KEY=your_api_key_here

3. Run the application:

python app.py

The app will launch in your web browser. Enter a YouTube URL and a question related to the video content. The app will return the answer if it exists in the video.
Code Overview
The main components of the app are:

get_video_id(url): This function extracts the video ID from a YouTube URL.
get_captions(url): This function fetches the captions of the YouTube video using the YouTube Transcript API.
answer_question(youtube_url, user_question): This is the main function that processes the user's input, fetches the video captions, creates an index using langchain, and queries the OpenAI GPT model to answer the user's question.
The Gradio interface is used to create a user-friendly web interface for the app. The iface.launch() command starts the app and opens it in your default web browser.

Troubleshooting
If you encounter any issues with fetching captions, make sure that the YouTube video has English captions available. If you encounter any issues with the OpenAI API, make sure that your API key is valid and you have not exceeded your usage limits.

License
This project is licensed under the MIT License. See the LICENSE file for details.

