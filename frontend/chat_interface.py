import streamlit as st
from api_utils import get_api_response
from datetime import datetime

# ---------------- CUSTOM CHAT CSS ---------------- #
def add_chat_css():
    st.markdown("""
    <style>
        /* Scrollable chat container */
        .chat-scroll {
            max-height: 70vh;
            overflow-y: auto;
            padding: 8px 10px 12px 10px; /* top/right/bottom/left */
            display: flex;
            flex-direction: column;
            gap: 12px; /* space between messages */
            scroll-behavior: smooth;
        }

        /* Each row controls left/right placement */
        .chat-row {
            display: flex;
            width: 100%;
        }
        .chat-row.user {
            justify-content: flex-end;
        }
        .chat-row.assistant {
            justify-content: flex-start;
        }

        /* Fade-in animation for new messages */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(5px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Message bubble */
        .bubble {
            position: relative;
            padding: 10px 14px;
            border-radius: 15px;
            max-width: 78%;
            animation: fadeIn 0.25s ease-in-out;
            word-wrap: break-word;
            margin: 4px 0;
            line-height: 1.35;
        }

        /* User bubble style */
        .user-bubble {
            background-color: #2E7DFF;
            color: white;
            border-radius: 16px 16px 4px 16px;
            margin-right: 4px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.06);
        }

        /* Assistant bubble style */
        .assistant-bubble {
            background-color: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 16px 16px 16px 4px;
            margin-left: 4px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        }

        /* Bubble width tuning for less visual symmetry */
        @media (min-width: 640px) {
            .user-bubble { max-width: 70%; }
            .assistant-bubble { max-width: 72%; }
        }

        /* Timestamp inside bubble */
        .timestamp {
            display: block; 
            margin-top: 4px; 
            font-size: 10px;
            text-align: right;  
            position: static;
        }
        /* For timestamps inside user (blue) bubbles */
        .user-bubble .timestamp {
            color: rgba(255, 255, 255, 0.75);  /* light text for dark background */
        }
        /* For timestamps inside assistant (white) bubbles */
        .assistant-bubble .timestamp {
            color: #6B7280;  /* darker gray for contrast on white */
        }
        /* Hover effect - subtle tint */
        .bubble:hover {
            background-color: rgba(0,0,0,0.02); /* light grey for white bubbles */
        }
        .user-bubble:hover {
            background-color: #1f66e0; /* slightly darker blue for user bubbles */
        }
    </style>
    """, unsafe_allow_html=True)

# ---------------- CHAT INTERFACE ---------------- #
def display_chat_interface():
    add_chat_css()

    # Capture user input
    if prompt := st.chat_input("Type your message..."):
        # Add user message to history
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "time": datetime.now().strftime("%H:%M")
        })

        # Get assistant response
        with st.spinner("🤖 Thinking..."):
            response = get_api_response(prompt, st.session_state.session_id, st.session_state.model)

        if response:
            st.session_state.session_id = response.get('session_id')
            st.session_state.messages.append({
                "role": "assistant",
                "content": response['answer'],
                "time": datetime.now().strftime("%H:%M")
            })
        else:
            st.error("Failed to get a response from the API.")

    # Render messages left/right aligned
    st.markdown("<div class='chat-scroll'>", unsafe_allow_html=True)
    for message in st.session_state.messages:
        role_class = "user" if message["role"] == "user" else "assistant"
        bubble_class = "user-bubble" if message["role"] == "user" else "assistant-bubble"
        timestamp = message.get("time", datetime.now().strftime("%H:%M"))

        st.markdown(
            f"""
            <div class='chat-row {role_class}'>
                <div class='bubble {bubble_class}'>
                    {message['content']}
                    <div class='timestamp'>{timestamp}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Auto scroll to bottom
    st.markdown("""
    <script>
        var chatDiv = document.querySelector('.chat-scroll');
        if (chatDiv) { chatDiv.scrollTop = chatDiv.scrollHeight; }
    </script>
    """, unsafe_allow_html=True)