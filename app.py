from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from langchain.prompts import PromptTemplate
from langchain import LLMChain
from langchain_together import ChatTogether
from langchain_community.document_loaders import YoutubeLoader
from youtube_transcript_api import YouTubeTranscriptApi
import re

# Initialize Flask app
app = Flask(__name__)

# Set up the LLM
API_KEY = "your_together_ai_api_key"
llm = ChatTogether(api_key=API_KEY, temperature=0.0, model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo")

# Define a PromptTemplate
product_description_template = PromptTemplate(
    input_variables=["video_transcript"],
    template="""
    Read through the entire transcript carefully.
           Provide a concise summary of the video's main topic and purpose.
           Extract and list the five most interesting or important points from the transcript. 
           For each point: State the key idea in a clear and concise manner.

        - Ensure your summary and key points capture the essence of the video without including unnecessary details.
        - Use clear, engaging language that is accessible to a general audience.
        - If the transcript includes any statistical data, expert opinions, or unique insights, 
        prioritize including these in your summary or key points.

    Video transcript: {video_transcript}    
    """
)

# LLM chain
chain = LLMChain(llm=llm, prompt=product_description_template)

# Validate YouTube URL
def is_youtube_url(url):
    youtube_regex = (
        r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'
    )
    return re.match(youtube_regex, url)

# Summarize video function
def summarise(video_url):
    try:
        # Load the transcript using LangChain's YoutubeLoader
        loader = YoutubeLoader.from_youtube_url(video_url, add_video_info=False)
        data = loader.load()

        # Extract transcript content
        video_transcript = data[0].page_content

        # Generate summary using the LLMChain
        summary = chain.invoke({"video_transcript": video_transcript})

        # Return the summary text
        return summary["text"]
    except Exception as e:
        return f"Error: Unable to summarize the video. {str(e)}"

# Define the Flask route for summarization
@app.route('/summary', methods=['POST'])
def summary():
    url = request.form.get('Body')  # Get the URL from the WhatsApp message
    print(f"Received URL: {url}")

    if is_youtube_url(url):
        response = summarise(url)
    else:
        response = "Please check if this is a correct YouTube video URL."
    print(f"Response: {response}")

    # Create a Twilio messaging response
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(response)

    return str(resp)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
