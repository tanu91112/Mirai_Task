import streamlit as st
import requests
import random
from urllib.parse import quote

# Page Config
st.set_page_config(
    page_title="AI Image Studio",
    page_icon="🎨",
    layout="centered"
)

st.title("🎨 AI Image Studio")
st.write("Generate amazing AI images using Pollinations AI")

# Sidebar
st.sidebar.header("⚙️ Settings")

art_style = st.sidebar.selectbox(
    "Choose Art Style",
    [
        "Realistic",
        "Anime",
        "Cyberpunk",
        "Fantasy",
        "Watercolor",
        "Digital Art"
    ]
)

width = st.sidebar.slider(
    "Image Width",
    min_value=256,
    max_value=1024,
    value=512,
    step=64
)

height = st.sidebar.slider(
    "Image Height",
    min_value=256,
    max_value=1024,
    value=512,
    step=64
)

magic_enhance = st.sidebar.checkbox("✨ Enable Magic Enhance")

# Surprise prompts
surprise_prompts = [
    "An astronaut riding a horse on Mars",
    "A cyberpunk street food vendor in Tokyo",
    "A dragon drinking coffee in New York",
    "A futuristic underwater city",
    "A robot chef cooking pizza in space"
]

prompt = st.text_input(
    "Enter your image prompt",
    placeholder="Example: A futuristic city at sunset"
)

col1, col2 = st.columns(2)

generate = col1.button("🎨 Generate Image")
surprise = col2.button("🎲 Surprise Me!")

# Surprise Me Feature
if surprise:
    prompt = random.choice(surprise_prompts)
    st.info(f"Surprise Prompt: {prompt}")
    generate = True

if generate:

    if prompt.strip() == "":
        st.warning("Please enter a prompt.")
    else:

        full_prompt = f"{prompt}, {art_style}"

        # Magic Enhance Feature
        if magic_enhance:
            full_prompt += (
                ", masterpiece, 8k resolution, highly detailed, "
                "trending on artstation, unreal engine 5 render"
            )

        encoded_prompt = quote(full_prompt)

        # Task 1 Fix: Width & Height parameters
        url = (
            f"https://image.pollinations.ai/prompt/"
            f"{encoded_prompt}"
            f"?width={width}&height={height}"
        )

        with st.spinner("Generating image..."):
            response = requests.get(url)

        if response.status_code == 200:

            image_bytes = response.content

            st.image(
                image_bytes,
                caption=full_prompt,
                use_container_width=True
            )

            # Task 2 Fix: PNG filename
            st.download_button(
                label="📥 Download Image",
                data=image_bytes,
                file_name=f"{art_style}_image.png",
                mime="image/png"
            )

        else:
            st.error(
                f"Image generation failed. Status code: {response.status_code}"
            )