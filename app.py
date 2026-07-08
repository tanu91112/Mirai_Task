import streamlit as st

# -----------------------------
# Identity Echo Interface
# -----------------------------

st.title("Identity Echo Interface")
st.write("Enter your details below and press the button to send your message.")

# User Inputs
name = st.text_input("Name")
message = st.text_input("Message")

# Button
if st.button("Transmit"):

# Validation
    if not name.strip():
        st.error("Please provide your name.")

    elif not message.strip():
        st.warning("Please type a message to transmit.")

    else:
# Success Output
        st.success(
            f"Transmission successful! Greetings, {name}. "
            f"We received your message: {message}"
        )

# Optional Challenge: Token Estimator
        characters = len(message)
        estimated_tokens = characters / 4

        st.info(
            f"System Check: Your message will consume approximately "
            f"{estimated_tokens:.2f} tokens from our context window."
        )