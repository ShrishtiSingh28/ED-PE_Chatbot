import streamlit as st
from chatbot_core import ChatbotCore
import os


st.set_page_config(
    page_title="Doc Rxmen",
    page_icon="🏥",
    layout="centered"
)


st.markdown("""
<style>
    .stButton button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #1A5BD9;
        color: white !important;
        font-weight: bold;
        border: none !important;
        box-shadow: none !important;
    }
    .stButton button:hover {
        background-color: #2072AF !important;
        color: white !important;
        border: none !important;
        box-shadow: none !important;
    }
    .stButton button:active, .stButton button:focus {
        color: white !important;
        background-color: #2072AF !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
    }
    .css-18e3th9 {
        padding-top: 2rem;
    }
    .css-1d391kg {
        padding-top: 3.5rem;
    }
    h1 {
        color: #1A5BD9;
    }
    .final-analysis {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    .category {
        color: #1A5BD9;
        font-size: 1.2em;
        margin-bottom: 10px;
    }
    .additional-factors {
        background-color: #e6e9ef;
        padding: 15px;
        border-radius: 5px;
        margin-top: 15px;
    }
    .recommendations {
        margin-top: 20px;
        padding: 15px;
        border-left: 4px solid #1A5BD9;
    }
    .chat-history {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    .chat-entry {
        margin-bottom: 10px;
    }
    .question {
        font-weight: bold;
    }
    .answer {
        margin-left: 20px;
    }
    .result-title {
        font-size: 1.2em;
        color: #fff;
        font-weight: 600;
        margin-bottom: 0.2em;
    }
    .result-value {
        font-size: 2em;
        color: #fff;
        font-weight: 700;
        margin-bottom: 0.7em;
    }
</style>
""", unsafe_allow_html=True)

def reset_session():
    st.session_state.chatbot.reset()
    st.session_state.language_selected = False
    st.session_state.concern_selected = False
    st.session_state.chat_started = False
    st.session_state.current_response = None

# Initialize session state
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = ChatbotCore()
if 'language_selected' not in st.session_state:
    st.session_state.language_selected = False
if 'concern_selected' not in st.session_state:
    st.session_state.concern_selected = False
if 'chat_started' not in st.session_state:
    st.session_state.chat_started = False
if 'current_response' not in st.session_state:
    st.session_state.current_response = None


st.title("Doc Rxmen")


with st.sidebar:
    if st.button("Start Over", key="sidebar_reset"):
        reset_session()
        st.rerun()


if not st.session_state.language_selected:
    st.header("Select Language / भाषा चुनें")
    language_options = st.session_state.chatbot.get_language_options()
    
    cols = st.columns(len(language_options))
    for idx, lang in enumerate(language_options):
        if cols[idx].button(lang):
            st.session_state.chatbot.set_language(lang)
            st.session_state.language_selected = True
            st.rerun()


elif not st.session_state.concern_selected:
    concerns = st.session_state.chatbot.get_concern_options()
    st.header("Choose your concern" if st.session_state.chatbot.current_language == "en" 
              else "Apni samasya chunein")
    
    cols = st.columns(len(concerns))
    for idx, concern in enumerate(concerns):
        if cols[idx].button(concern):
            st.session_state.chatbot.set_concern(concern)
            st.session_state.concern_selected = True
            st.session_state.chat_started = True
            st.rerun()


elif st.session_state.chat_started:
    
    if not st.session_state.current_response:
        st.session_state.current_response = st.session_state.chatbot.get_next_question()
    
    
    if isinstance(st.session_state.current_response, dict):
        if "output_format" in st.session_state.current_response:
            if st.session_state.current_response["output_format"] == "initial":
                
                sections = st.session_state.current_response["sections"]
                st.markdown(sections["title"], unsafe_allow_html=True)
                st.write(sections["text"])
                
                cols = st.columns(len(sections["options"]))
                for idx, option in enumerate(sections["options"]):
                    if cols[idx].button(option, key=f"option_{idx}"):
                        next_response = st.session_state.chatbot.get_next_question(option)
                        st.session_state.current_response = next_response
                        st.rerun()
            
            elif st.session_state.current_response["output_format"] == "diagnosis":
                
                st.markdown('<div class="final-analysis">', unsafe_allow_html=True)
                st.markdown('<div class="result-title">Final Analysis</div>', unsafe_allow_html=True)
                
                sections = st.session_state.current_response["sections"]
                if "category" in sections:
                    st.markdown(f'<div class="result-value">{sections["category"].replace("## ", "")}</div>', unsafe_allow_html=True)
                if "causes_header" in sections and "causes" in sections:
                    st.markdown(f'<div class="result-title">{sections["causes_header"].replace("## ", "")}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="result-value">{sections["causes"]}</div>', unsafe_allow_html=True)
                if "specialist_header" in sections and "specialist" in sections:
                    st.markdown(f'<div class="result-title">{sections["specialist_header"].replace("## ", "")}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="result-value">{sections["specialist"]}</div>', unsafe_allow_html=True)
                
                
                st.markdown('<div class="chat-history">', unsafe_allow_html=True)
                st.markdown("### Consultation History")
                for entry in st.session_state.chatbot.chat_history:
                    st.markdown(f"""
                    <div class="chat-entry">
                        <div class="question">Q: {entry['question']}</div>
                        <div class="answer">A: {entry['answer']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("Start New Assessment", key="final_reset"):
                        reset_session()
                        st.rerun()
        else:
            
            st.write(f"### {st.session_state.current_response['text']}")
            cols = st.columns(len(st.session_state.current_response['options']))
            
            for idx, option in enumerate(st.session_state.current_response['options']):
                if cols[idx].button(option, key=f"option_{idx}"):
                    next_response = st.session_state.chatbot.get_next_question(option)
                    st.session_state.current_response = next_response
                    st.rerun()


st.markdown("---") 