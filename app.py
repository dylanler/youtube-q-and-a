import openai
import os
from langchain.document_loaders import TextLoader, YoutubeLoader
#pytube, gradio, langchain, openai
import gradio as gr
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.indexes import VectorstoreIndexCreator

os.environ["OPENAI_API_KEY"] = "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"

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

    f= open("temp.txt","w+")
    f.write(get_captions(user_question))
    f.close() 

    loader = TextLoader("temp.txt")

    index = VectorstoreIndexCreator().from_loaders([loader])
    os.remove("temp.txt")

    query = user_question
    answer = index.query(query)

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

