import streamlit as st
import google.generativeai as genai
from langsmith import traceable
import os

genai.configure(api_key=st.secrets["gemini"]["api_key"])

os.environ["LANGSMITH_API_KEY"] = st.secrets["langsmith"]["api_key"]
os.environ["LANGSMITH_TRACING"] = st.secrets["langsmith"]["tracing"]
os.environ["LANGSMITH_PROJECT"] = st.secrets["langsmith"]["project"]
os.environ["LANGSMITH_ENDPOINT"] = st.secrets["langsmith"]["endpoint"]


@traceable(name="checking")
def sentiment_analysis(text):
    try:
        with st.spinner("Analyzing sentiment..."):
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(
                f"Analyze the sentiment of the following text:\n\n{text}"
            )
            return response.text
    except Exception as e:
        return f"Error: {e}"

st.title("Sentiment Analysis App")
st.write("Enter a text below to analyze its sentiment:")

user_input = st.text_area("Input text", "")

if st.button("Analyze Sentiment"):
    if user_input.strip():
        sentiment = sentiment_analysis(user_input)
        st.success(f"Sentiment analysis result: {sentiment}")
    else:
        st.warning("Please enter some text to analyze.")
