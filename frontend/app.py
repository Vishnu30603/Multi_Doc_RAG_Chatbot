import streamlit as st
from sidebar import display_sidebar
from chat_interface import display_chat_interface

# Custom CSS for header styling
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_base64 = get_base64_image("logo.png")

st.markdown(f"""
<style>
.header-container {{
    display: flex;
    align-items: center;
    gap: 4px;
}}
.header-logo {{
    height: 200px;
    width: auto;
    image-rendering: crisp-edges;
}}
.header-title {{
    font-size: 4 rem;
    font-weight: bold;
    margin: 0;
    line-height: 1;
}}
</style>
<div class="header-container">
    <img src="data:image/png;base64,{logo_base64}" class="header-logo">
    <h1 class="header-title">Multi-Doc RAG Chatbot</h1>
</div>
""", unsafe_allow_html=True)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = None

# Display the sidebar
display_sidebar()

# Display the chat interface
display_chat_interface()
