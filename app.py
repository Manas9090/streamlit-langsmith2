import streamlit as st
import openai
from langsmith import Client, traceable
st.write("Secrets:", st.secrets)
# Load API keys securely
openai.api_key = st.secrets["openai"]["api_key"]
client = Client(
    api_key=st.secrets["langsmith"]["api_key"],
    project_name=st.secrets["langsmith"]["project_name"],
tracing=st.secrets["langsmith"]["tracing"]
)
if client:
    print("client initializer") 
    st.write("client initializer")

# Add tracing decorator to monitor the function
@traceable(name="Sentiment Analysis", metadata={"app": "Streamlit Sentiment Analysis"})
def sentiment_analysis(text): 
    try:
        with st.spinner("Analyzing sentiment..."):
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"Analyze the sentiment of the following text:\n\n{text}"}
                ],
                max_tokens=100
            )
            return response.choices[0].message.content
    except Exception as e:
        client.log_error(str(e))  # Log errors to LangSmith
        return f"Error: {e}"

# Streamlit UI
st.title("Sentiment Analysis App")
st.write("Enter a text below to analyze its sentiment:")

user_input = st.text_area("Input text", "")

if st.button("Analyze Sentiment"): 
    if user_input.strip():
        sentiment = sentiment_analysis(user_input)
        st.success(f"*Sentiment analysis result:* {sentiment}")
    else:
        st.warning("Please enter some text to analyze.")
