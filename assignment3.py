import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# -------------------------------
# Load Gemini API Key
# -------------------------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# -------------------------------
# Streamlit Page Configuration
# -------------------------------
st.set_page_config(
    page_title="AI Multiverse",
    page_icon="🤖"
)

st.title("🌍 AI Multiverse")
st.write("Chat with different AI personalities that remember your conversation.")

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.header("AI Personality")

personality = st.sidebar.selectbox(
    "Choose a personality",
    (
        "Common Indian Man",
        "Crazy Salman Khan Fan",
        "Little Boy",
        "Motivational Coach",
        "Software Engineer",
        "College Professor",
        "Stand-up Comedian",
        "Entrepreneur",
        "Friendly Teacher",
        "AI Assistant"
    )
)

# -------------------------------
# Memory Vault
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear chat
if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# -------------------------------
# Display Previous Messages
# -------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------
# Chat Input
# -------------------------------
if user_message := st.chat_input("Say something..."):

    # Store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    with st.chat_message("user"):
        st.markdown(user_message)

    # Build conversation history
    conversation = ""

    for chat in st.session_state.messages:
        conversation += f"{chat['role']}: {chat['content']}\n"

    system_prompt = f"""
You are acting as {personality}.

Rules:
- Always stay in character.
- Answer naturally.
- Continue the conversation using previous chat history.

Conversation:
{conversation}

Assistant:
"""

    with st.spinner("Thinking..."):

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=system_prompt
            )

            assistant_reply = response.text

        except Exception as error:
            assistant_reply = f"Error: {error}"

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )