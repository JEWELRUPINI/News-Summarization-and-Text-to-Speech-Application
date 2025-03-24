# utils.py

import os
import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator
from gtts import gTTS

AUDIO_FOLDER = "audio_files"
os.makedirs(AUDIO_FOLDER, exist_ok=True)

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
