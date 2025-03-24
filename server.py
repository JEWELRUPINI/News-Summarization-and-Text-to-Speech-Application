from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator
from gtts import gTTS
import os
import uvicorn

app = FastAPI()

AUDIO_FOLDER = "audio_files"
os.makedirs(AUDIO_FOLDER, exist_ok=True)


class CompanyRequest(BaseModel):
    company_name: str

# Function to fetch news articles from Bing
def get_news_bing(company_name):
    search_url = f"https://www.bing.com/news/search?q={company_name}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = []
    
    for result in soup.select(".news-card"):
        title_tag = result.select_one("a.title")
        snippet_tag = result.select_one(".snippet")
        source_tag = result.select_one(".source")
        if source_tag and len(source_tag.get_text(strip=True).split()) >= 8:
            topic = source_tag.get_text(strip=True)
        elif title_tag:
            topic = " ".join(title_tag.get_text(strip=True).split()[:8])
            
        elif snippet_tag:
            topic = " ".join(snippet_tag.get_text(strip=True).split()[:8])
            
        else:
            topic = "Unknown"
        
        link = title_tag["href"] if title_tag else ""

        if title_tag and snippet_tag:
            articles.append({
                "title": title_tag.get_text(strip=True),
                "summary": snippet_tag.get_text(strip=True),
                "topic": topic,
                "link": link
            })

        if len(articles) >= 10:
            break

    return articles

# Sentiment Analysis Function
def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(text)["compound"]
    return "Positive" if score >= 0.05 else "Negative" if score <= -0.05 else "Neutral"

# Generate Hindi Summary & Audio
def generate_hindi_audio(summary_text, filename):
    audio_path = os.path.join(AUDIO_FOLDER, filename)
    tts = gTTS(text=summary_text, lang="hi")
    tts.save(audio_path)
    return filename

# Main Sentiment Analysis API
@app.post("/sentiment")
async def analyze_news_sentiment(request: CompanyRequest):
    company_name = request.company_name
    news_articles = get_news_bing(company_name)

    if not news_articles:
        return {"error": "No news articles found"}

    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    summary_text = f"{company_name} कंपनी के समाचार सारांश:\n\n"
    translator = Translator()

    results = []
    
    for idx, article in enumerate(news_articles, 1):
        title = article["title"]
        summary = article["summary"]
        topic = article["topic"]
        sentiment = analyze_sentiment(summary)

        sentiment_counts[sentiment] += 1

        title_hindi = translator.translate(title, src='en', dest='hi').text
        summary_hindi = translator.translate(summary, src='en', dest='hi').text
        sentiment_hindi = {"Positive": "सकारात्मक", "Negative": "नकारात्मक", "Neutral": "तटस्थ"}[sentiment]

        summary_text += f"समाचार {idx}: {title_hindi}\nसंक्षेप: {summary_hindi}\nभावना: {sentiment_hindi}\n\n"

        results.append({
            "title": title, 
            "summary": summary, 
            "topic": topic, 
            "sentiment": sentiment, 
            "link": article["link"]
        })

    overall_sentiment = (
        "✅ समग्र भावना: सकारात्मक" if sentiment_counts["Positive"] > sentiment_counts["Negative"] else 
        "❌ समग्र भावना: नकारात्मक" if sentiment_counts["Negative"] > sentiment_counts["Positive"] else 
        "⚖️ समग्र भावना: संतुलित या तटस्थ"
    )
    
    summary_text += f"\n{overall_sentiment}"
    audio_filename = f"{company_name.replace(' ', '_')}.mp3"
    generate_hindi_audio(summary_text, audio_filename)

    return {
        "articles": results,
        "sentiment_counts": sentiment_counts,
        "summary_text": summary_text,
        "audio_file": audio_filename,
        "audio_download_url": f"http://13.201.168.170:7860/download_audio/{audio_filename}"
    }

# API to serve audio file for download
@app.get("/download_audio/{filename}")
async def download_audio(filename: str):
    file_path = os.path.join(AUDIO_FOLDER, filename)
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    return FileResponse(file_path, media_type="audio/mpeg", filename=filename)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)