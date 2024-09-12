import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(
        page_title="AskGenie",
        page_icon='🧞',
        layout="wide"
    )

os.environ["API_KEY"] = ""
genai.configure(api_key=os.environ["API_KEY"])

def llm_query(context):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(context)
    return response

st.markdown(
    "<h1 style='text-align: center; font-family: Arial, sans-serif;'>AskGenie: Your Instant AI-Powered Knowledge Hub</h1>", 
    unsafe_allow_html=True
)

if 'history' not in st.session_state:
    st.session_state.history = []

def create_context():
    history = st.session_state.history
    context = ""
    for message in history:
        context += f"{message['role']}: {message['text']}\n"
    return context

def submit_question():
    question = st.session_state.question_input
    if question.strip():
        st.session_state.history.append({'role': 'User', 'text': question})
        context = create_context()
        answer = llm_query(context).text
        st.session_state.history.append({'role': 'Assistant', 'text': answer})
    else:
         st.session_state.question_input = ''
    st.session_state.question_input = ''

# Display previous chat history
for message in st.session_state.history:
    if message['role'] == 'User':
        st.write(f"**You**: {message['text']}")
    else:
        st.write(f"**Assistant**: {message['text']}")

question = st.text_input("Enter your question:", key='question_input', on_change=submit_question)
