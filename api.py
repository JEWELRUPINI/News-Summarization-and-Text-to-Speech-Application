# api.py
import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from utils import get_news_bing, analyze_sentiment, generate_hindi_audio
from googletrans import Translator

app = FastAPI()

class CompanyRequest(BaseModel):
    company_name: str

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
    file_path = os.path.join("audio_files", filename)
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    return FileResponse(file_path, media_type="audio/mpeg", filename=filename)

