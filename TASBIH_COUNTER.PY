# app.py
import streamlit as st
from PIL import Image, ImageOps
import os
import glob

# Page config
st.set_page_config(page_title="Digital Tasbih", page_icon="🕋", layout="centered")

# Styling
BACKGROUND = "#FFF0F5"
FRAME_BG = "#FFE4E8"
TEXT = "#4A4A4A"
ACCENT = "#FF99AC"
BUTTON = "#FFB6C1"

st.markdown(
    f"""
    <style>
        .main {{background-color: {BACKGROUND}; padding: 1rem 2rem;}}
        .title {{text-align:center; color:{TEXT}; margin-bottom:0.2rem;}}
        .subtitle {{text-align:center; color:{TEXT}; margin-top:0; margin-bottom:1rem;}}
        .counter {{font-size:4.5rem; font-weight:700; color:{TEXT}; text-align:center;}}
        .stButton>button {{
            background-color: {BUTTON};
            color: {TEXT};
            padding: 10px 28px;
            border-radius: 10px;
            font-size: 18px;
            border: none;
        }}
        .stButton>button:hover {{ background-color: {ACCENT}; color: #fff; }}
        .small-muted {{ color: #777; font-size:0.9rem; text-align:center; }}
        .challenge-box {{ background: {FRAME_BG}; padding: 12px; border-radius: 10px; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Dhikrs dictionary
DHIKRS = {
    "Subhanallah": "Glory be to Allah",
    "Alhamdulillah": "Praise be to Allah",
    "Allahu Akbar": "Allah is the Greatest",
    "La ilaha illallah": "There is no god but Allah",
    "Astaghfirullah": "I seek forgiveness from Allah"
}

st.markdown("<h1 class='title'>Digital Tasbih</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>A simple, beautiful tasbih counter for dhikr</p>", unsafe_allow_html=True)

# Session state
if "count" not in st.session_state:
    st.session_state.count = 0
if "total_count" not in st.session_state:
    st.session_state.total_count = 0
if "slide_index" not in st.session_state:
    st.session_state.slide_index = 0

# Image loader (auto loads all images in images/ folder)
IMAGES_FOLDER = "images"
image_paths = []
if os.path.isdir(IMAGES_FOLDER):
    image_paths = sorted(
        glob.glob(os.path.join(IMAGES_FOLDER, "*.png"))
        + glob.glob(os.path.join(IMAGES_FOLDER, "*.jpg"))
        + glob.glob(os.path.join(IMAGES_FOLDER, "*.jpeg"))
    )

# Top controls: Dhikr selection
st.subheader("Select Dhikr")
selected = st.selectbox("", list(DHIKRS.keys()), index=list(DHIKRS.keys()).index("Astaghfirullah"))
st.markdown(f"<div class='small-muted'>{DHIKRS[selected]}</div>", unsafe_allow_html=True)

# Counter display
st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
st.markdown(f"<div class='counter'>{st.session_state.count}</div>", unsafe_allow_html=True)

# Buttons
col1, col2, col3 = st.columns([1,1,1])
with col1:
    if st.button("COUNT"):
        st.session_state.count += 1
        st.session_state.total_count += 1

with col2:
    if st.button("RESET"):
        st.session_state.count = 0

with col3:
    if st.button("ADD +10"):
        st.session_state.count += 10
        st.session_state.total_count += 10

# Challenges
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
st.markdown("<h3 style='color:#4A4A4A;'>Daily Challenges</h3>", unsafe_allow_html=True)

challenge_goal = 1000
col_a, col_b = st.columns(2)
with col_a:
    st.markdown("<div class='challenge-box'>", unsafe_allow_html=True)
    st.markdown(f"**{selected}**: {st.session_state.count} / {challenge_goal}")
    if st.session_state.count >= challenge_goal:
        st.success("MashaAllah! You completed the daily challenge.")
    st.markdown("</div>", unsafe_allow_html=True)

with col_b:
    st.markdown("<div class='challenge-box'>", unsafe_allow_html=True)
    st.markdown(f"**Total Dhikr (this session)**: {st.session_state.total_count}")
    st.markdown("</div>", unsafe_allow_html=True)

# Slideshow area
st.markdown("<hr/>", unsafe_allow_html=True)
st.markdown("<h3 style='color:#4A4A4A;'>Dhikr Slideshow</h3>", unsafe_allow_html=True)

if image_paths:
    # Show current image (resized for better appearance)
    try:
        img_path = image_paths[st.session_state.slide_index % len(image_paths)]
        img = Image.open(img_path)
        # Fit image nicely
        img = ImageOps.contain(img, (900, 600))
        st.image(img, use_column_width=True)
    except Exception as e:
        st.error(f"Error loading image: {e}")

    # Slideshow controls
    left, middle, right = st.columns([1,2,1])
    with left:
        if st.button("Previous Image"):
            st.session_state.slide_index = (st.session_state.slide_index - 1) % len(image_paths)
    with right:
        if st.button("Next Image"):
            st.session_state.slide_index = (st.session_state.slide_index + 1) % len(image_paths)
    # Optional auto-play toggle
    autoplay = st.checkbox("Auto-play (5s)", value=False)
    if autoplay:
        import time
        time.sleep(0.01)  # small pause to allow UI update
        # NOTE: streamlit reruns on state change; provide simple autoplay via button press UX
        if st.button("Advance (Auto)"):
            st.session_state.slide_index = (st.session_state.slide_index + 1) % len(image_paths)
else:
    st.info("Put your slideshow images inside the `images/` folder. Supported: .png, .jpg, .jpeg")

# Footer / small note
st.markdown("<hr/>", unsafe_allow_html=True)
st.markdown("<p class='small-muted'>Tip: Use the <strong>COUNT</strong> button for each dhikr. Use RESET to start over for a new set.</p>", unsafe_allow_html=True)
