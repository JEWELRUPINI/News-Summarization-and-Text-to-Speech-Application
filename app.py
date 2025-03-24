import streamlit as st
import requests

BACKEND_URL = "http://13.201.168.170:7860/sentiment"

st.title("News Summarization and Text-to-Speech Application")
#st.write("Enter a company name")

company_name = st.text_input("Enter Company Name:", "Tesla")

if st.button("Search"):
    st.write(f"🔍 Fetching news for **{company_name}**...")

    response = requests.post(BACKEND_URL, json={"company_name": company_name})

    if response.status_code == 200:
        data = response.json()
        if "error" in data:
            st.error(data["error"])
        else:
            # Display news articles and sentiment
            st.subheader("📰 News Articles and Sentiments")
            for idx, article in enumerate(data["articles"], 1):
                st.write(f"**{idx}. {article['title']}**")
                st.write(f"_Summary:_ {article['summary']}")
                st.write(f"_Topic:_ {article['topic']}")
                st.write(f"_Sentiment:_ **{article['sentiment']}**")
                st.write(f"[Read more]({article['link']})")
                st.write("---")

            # Show comparative sentiment analysis
            st.subheader("📊 Sentiment Analysis Summary")
            st.write(f"🔹 **Positive Articles:** {data['sentiment_counts']['Positive']}")
            st.write(f"🔸 **Negative Articles:** {data['sentiment_counts']['Negative']}")
            st.write(f"⚪ **Neutral Articles:** {data['sentiment_counts']['Neutral']}")

            # Display and download Hindi audio summary
            st.subheader("🔊 Listen to Hindi Summary")
            audio_url = data["audio_download_url"]
            st.audio(audio_url, format="audio/mp3")

            st.markdown(f'<a href="{audio_url}" download="summary_audio.mp3"><button>📥 Download Audio</button></a>', unsafe_allow_html=True)
    else:
        st.error("Failed to fetch data from the backend. Make sure FastAPI is running.")