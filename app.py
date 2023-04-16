import openai
import os
from langchain.document_loaders import TextLoader, YoutubeLoader
#pytube, gradio, langchain, openai
import gradio as gr
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms import OpenAI

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

previous_youtube_url = None
index = None

def get_video_id(url):
    video_id = None
    if 'youtu.be' in url:
        video_id = url.split('/')[-1]
    else:
        video_id = url.split('watch?v=')[-1]
    return video_id

def get_captions(url):
    try:
        video_id = get_video_id(url)
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(['en'])
        captions = transcript.fetch()

        formatted_captions = ''
        for caption in captions:
            formatted_captions += caption['text'] + ' '

        return formatted_captions

    except Exception as e:
        print(e)
        return "Error. Could not fetch captions."



def answer_question(youtube_url, user_question):
    # You can implement your logic here to process the video, transcribe it, and answer the user question.
    # For now, let's return the user question as output.
    global previous_youtube_url
    global index
    
    if previous_youtube_url == youtube_url:
        #index = VectorstoreIndexCreator().from_loaders([loader])
        query = user_question
        answer = index.query(llm=OpenAI(model="text-davinci-003"), question = query)
    else:
        f= open("temp.txt","w+")
        f.write(get_captions(youtube_url))
        f.close() 
        loader = TextLoader("temp.txt")
    
        index = VectorstoreIndexCreator().from_loaders([loader])
        os.remove("temp.txt")

        query = user_question
        answer = index.query(llm=OpenAI(model="text-davinci-003"), question = query)

    return answer

iface = gr.Interface(
    fn=answer_question,
    inputs=[
        gr.inputs.Textbox(lines=1, placeholder="Enter YouTube URL here..."),
        gr.inputs.Textbox(lines=1, placeholder="Enter your question here...")
    ],
    outputs=gr.outputs.Textbox(),
    title="YouTube Video Question Answering",
    description="Enter a YouTube URL and a question related to the video content. The app will return the answer if answer exists in the video."
)
if __name__ == "__main__":
    iface.launch()

