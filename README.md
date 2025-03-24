News Summarization and Text-to-Speech Application
This project is a News Summarization and Text-to-Speech Application API built using FastAPI for the backend and Streamlit for the frontend (if needed). It provides sentiment analysis of news articles related to a specific company, generates a Hindi summary of the news, and converts the summary into an audio file. The API uses BeautifulSoup to scrape Bing news, VADER for sentiment analysis, Google Translate for translation, and gTTS to generate the audio. The app is deployed using Hugging Face and is hosted on an AWS EC2 instance, making it accessible publicly.

Table of Contents
Features
Dependencies
Setup Instructions
Folder Structure

How to Use
API Endpoints
Deployment
Contributing
License
Features
Fetches news articles from Bing News based on a company name.
Performs sentiment analysis on the fetched news articles using VADER.
Translates the news title and summary to Hindi using Google Translate.
Generates a Hindi audio file of the news summary using gTTS.
Provides a downloadable audio file of the summary via an API.
API to get sentiment analysis of news articles related to a company.
Deployed using Hugging Face and hosted on AWS EC2, allowing public access.
link- https://huggingface.co/spaces/jewelrupini/News_Summarization_and_Text_to_Speech_Application

Dependencies
This project requires the following Python libraries:
fastapi - FastAPI for creating the backend API.
uvicorn - ASGI server for serving the FastAPI application.
pydantic - Data validation using Pydantic models.
requests - For making HTTP requests to fetch news articles.
beautifulsoup4 - For parsing HTML and scraping news articles from Bing.
vaderSentiment - For performing sentiment analysis.
googletrans - For translating text to Hindi.
gtts - For converting text to speech (audio).
os - For file system operations.
To install all the dependencies, run the following command:

Bash, Copy, Edit
pip install -r requirements.txt
requirements.txt:
fastapi
uvicorn
pydantic
requests
beautifulsoup4
vaderSentiment
googletrans==4.0.0-rc1
gtts
Setup Instructions
Clone the repository:
First, clone the repository to your local machine:
bash
Copy
Edit
git clone https://github.com/your-username/news-sentiment-analysis-api.git
cd news-sentiment-analysis-api
Install dependencies:
Install the required Python dependencies:
bash
Copy
Edit
pip install -r requirements.txt
Create audio directory:
Make sure to create a folder for storing the generated audio files:
bash
Copy
Edit
mkdir audio_files
Run the FastAPI server locally (optional):

If you want to run the app locally before deploying, start the FastAPI server using uvicorn:

bash
Copy
Edit
uvicorn api:app --reload
This will start the server on http://127.0.0.1:8000.

Folder Structure
Here is the folder structure for the project:

graphql
Copy
Edit
news-sentiment-analysis-api/
│
├── api.py                # FastAPI app with API routes
├── utils.py              # Utility functions (news scraping, sentiment analysis, etc.)
├── audio_files/          # Folder to store generated audio files
├── requirements.txt      # List of Python dependencies
└── README.md             # Project documentation
How to Use
Access the API:
After running the server, you can access the API documentation at http://127.0.0.1:8000/docs (locally). This provides an interactive interface for testing the API.
POST Request to /sentiment:
To analyze the sentiment of news articles related to a company, make a POST request to the /sentiment endpoint. The body of the request should include the company name.
Example Request:

json
Copy
Edit
{
  "company_name": "Tesla"
}
Example Response:

json
Copy
Edit
{
  "articles": [
    {
      "title": "Tesla announces new product",
      "summary": "Tesla's new product is a game-changer in the EV industry...",
      "topic": "Electric Vehicles",
      "sentiment": "Positive",
      "link": "https://www.example.com/tesla-announces-new-product"
    },
    ...
  ],
  "sentiment_counts": {
    "Positive": 8,
    "Negative": 2,
    "Neutral": 0
  },
  "summary_text": "Tesla कंपनी के समाचार सारांश: ...",
  "audio_file": "Tesla.mp3",
  "audio_download_url": "http://127.0.0.1:8000/download_audio/Tesla.mp3"
}
GET Request to /download_audio/{filename}:

To download the generated audio file (Hindi summary), make a GET request to the /download_audio/{filename} endpoint. Replace {filename} with the name of the audio file.

Example Request:

bash
Copy
Edit
GET http://127.0.0.1:8000/download_audio/Tesla.mp3
This will return the audio file generated for the news summary in Hindi.

API Endpoints
/sentiment (POST)
Description: Analyzes sentiment of news articles related to a company.

Request Body:

json
Copy
Edit
{
  "company_name": "Company Name"
}
Response:

json
Copy
Edit
{
  "articles": [
    { "title": "Title", "summary": "Summary", "sentiment": "Positive", "link": "URL" },
    ...
  ],
  "sentiment_counts": {
    "Positive": 10,
    "Negative": 0,
    "Neutral": 0
  },
  "summary_text": "Hindi summary text",
  "audio_file": "filename.mp3",
  "audio_download_url": "http://your-server/download_audio/filename.mp3"
}
/download_audio/{filename} (GET)
Description: Serves the generated audio file for download.

Parameters: filename (e.g., Tesla.mp3)

Response: Audio file (MP3 format).

Deployment
Hugging Face Deployment
The backend FastAPI app is deployed on Hugging Face for ease of access and scale. This allows the API to be accessed publicly.

AWS EC2 Instance
For hosting the public server, we use an AWS EC2 instance with a public IP. The FastAPI app is deployed and accessible via this server, allowing users to access the sentiment analysis functionality.

Set up the EC2 instance on AWS with appropriate security groups.

Deploy FastAPI app to the EC2 instance.

Configure a public IP to access the app from anywhere.

You can access the deployed API via the public IP address of the EC2 instance, for example:

arduino
Copy
Edit
http://your-ec2-public-ip:7860
Contributing
Contributions are welcome! If you find a bug or want to add a new feature, feel free to submit a pull request or open an issue.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Now, with the Hugging Face link included, anyone can easily access your deployment and follow the instructions to use the app. Let me know if you need any more changes!

https://huggingface.co/spaces/jewelrupini/News_Summarization_and_Text_to_Speech_Application







