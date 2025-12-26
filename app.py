import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf
from streamlit_lottie import st_lottie
import requests

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SnapBreed AI",
    page_icon="🐶",
    layout="centered"
)

# ---------------- LOAD CSS ----------------
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "show_about" not in st.session_state:
    st.session_state.show_about = False

# ---------------- LOTTIE LOADER (ONLINE) ----------------
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

# ---------------- LOTTIE URLS ----------------
DOG_LOTTIE_URL = "https://assets9.lottiefiles.com/packages/lf20_jcikwtux.json"
SCAN_LOTTIE_URL = "https://assets10.lottiefiles.com/packages/lf20_qp1q7mct.json"

dog_lottie = load_lottie_url(DOG_LOTTIE_URL)

# ---------------- HERO SECTION ----------------
st.markdown("""
<h1>🐾 SnapBreed AI</h1>
<p>AI-powered dog breed recognition using Deep Learning</p>
</div>
""", unsafe_allow_html=True)

# ---------------- ABOUT ----------------
if st.button("ℹ️ About Project"):
    st.session_state.show_about = not st.session_state.show_about

if st.session_state.show_about:
    st.markdown("""
    <div class="glass-card">
        <h3>📌 About SnapBreed AI</h3>
        <p>
        A college mini-project developed at <b>SSCE Bangalore</b>.
        </p>
        <ul>
            <li>🐶 Dog Breed Identification</li>
            <li>🧠 TensorFlow CNN (MobileNetV2)</li>
            <li>🌐 Streamlit Web Application</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ---------------- UPLOAD ----------------
st.markdown("""
<div class="glass-card">
    <h2>📤 Upload Dog Image</h2>
    <p>Drag & drop or browse an image</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

# ---------------- PREDICTION ----------------
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    scan_lottie = load_lottie_url(SCAN_LOTTIE_URL)

    st.markdown('<div class="glass-card glow">', unsafe_allow_html=True)
    st_lottie(scan_lottie, height=180)
    st.markdown(
        "<h3 style='text-align:center'>🔍 AI Analyzing Image...</h3>",
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

    @st.cache_resource
    def load_model():
        return tf.keras.applications.MobileNetV2(weights="imagenet")

    model = load_model()

    def preprocess(img):
        img = img.resize((224, 224))
        img = np.array(img)
        img = tf.keras.applications.mobilenet_v2.preprocess_input(img)
        return np.expand_dims(img, axis=0)

    processed = preprocess(image)
    preds = model.predict(processed)
    decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=3)

    dog_labels = []
    for (_, label, prob) in decoded[0]:
        if any(x in label.lower() for x in [
            "dog", "hound", "terrier", "retriever",
            "shepherd", "pug", "husky"
        ]):
            dog_labels.append((label.replace("_", " ").title(), prob))

    if dog_labels:
        breed, confidence = dog_labels[0]
        percent = int(confidence * 100)

        st.markdown(f"""
        <div class="glass-card result">
            <h2>🐕 {breed}</h2>
            <p>Prediction Confidence</p>
            <div class="progress-bar">
                <div class="progress-fill" style="width:{percent}%;">
                    {percent}%
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("❌ Could not identify a dog breed. Try another image.")
