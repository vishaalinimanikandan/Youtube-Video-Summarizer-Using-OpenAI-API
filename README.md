# YouTube Summarizer WhatsApp Chatbot

This project builds a WhatsApp chatbot that takes a YouTube video URL as input, retrieves the video's transcript, summarizes its content using an LLM (Large Language Model), and returns the summary to the user. It uses Flask to create an API endpoint and Twilio for WhatsApp integration.

---

## Features

- **YouTube URL Validation**: Ensures the input is a valid YouTube link.
- **Transcript Retrieval**: Extracts the transcript of the video using `youtube_transcript_api` and `YoutubeLoader` from LangChain.
- **LLM-Powered Summarization**: Summarizes the video transcript using Together AI's Llama 3.1 model.
- **WhatsApp Integration**: Communicates with users via WhatsApp using Twilio's sandbox.

---
##Flow
![image](https://github.com/user-attachments/assets/e0168c8c-5448-47db-9995-a96a40211e2c)
![image](https://github.com/user-attachments/assets/80dbf631-e445-4ca4-8ca4-bc1ded58e956)

## Installation

### Prerequisites

- Python 3.8 or later
- A Together AI API key
- A Twilio account with WhatsApp sandbox enabled
- Ngrok for tunneling the local Flask server

### Clone the Repository

```bash
git clone https://github.com/your-username/youtube-summarizer-chatbot.git
cd youtube-summarizer-chatbot
