import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf

if "show_about" not in st.session_state:
    st.session_state.show_about = False

# Menu session state
if "menu_open" not in st.session_state:
    st.session_state.menu_open = False

def toggle_menu():
    st.session_state.menu_open = not st.session_state.menu_open

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="SnapBreed AI",
    page_icon="🐶",
    layout="centered"
)

# ---- CUSTOM CSS ----
st.markdown("""
<style>

body {
    background-color: #000000;
}

/* Remove Streamlit default padding */
.block-container {
    padding-top: 2rem;
}

/* Top Navigation Bar */
.top-nav {
    display: flex;
    align-items: center;
    gap: 15px;
    padding-left: 10px;
    margin-bottom: 60px;
}

.menu-icon {
    font-size: 30px;
    color: white;
    cursor: pointer;
}

.title-text {
    font-size: 28px;
    font-weight: 700;
    color: white;
    font-family: 'Poppins', sans-serif;
}


.upload-title {
    font-size: 20px;
    font-weight: 600;
    color: white;
    margin-bottom: 20px;
}


.upload-text {
    color: white;
    margin-top: 10px;
    font-size: 15px;
}

/* Hide default Streamlit file uploader text */
.css-1u5t076 {
    display: none;
}
.menu-box {
    background-color: #1C1C1C;
    padding: 12px;
    border-radius: 10px;
    width: 120px;
    margin-left: 10px;
    margin-top: 10px;
    border: 1px solid #333;
}

.menu-item {
    color: white;
    padding: 8px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 15px;
}

.menu-item:hover {
    background-color: #333;
}


</style>
""", unsafe_allow_html=True)

# ---- TOP NAV ----
col1, col2 = st.columns([1, 5])

with col1:
    if st.button("☰", key="menu_btn", help="Menu"):
        toggle_menu()

with col2:
    st.markdown("<div class='title-text'>SnapBreed AI</div>", unsafe_allow_html=True)

# ---- DROPDOWN MENU ----
if st.session_state.menu_open:

    about_clicked = st.button("About", key="about_btn")

    st.markdown("</div>", unsafe_allow_html=True)


    if about_clicked:
        st.session_state.show_about = True


if not st.session_state.menu_open:
    about_clicked = False


if st.session_state.show_about:
    st.markdown("""
    <div style="padding:20px; background:#111; border-radius:10px; border:1px solid #444;">
    <h3 style='color:#ffcc00;'>📌 About SnapBreed AI</h3>

    <p style='color:white; font-size:16px;'>
    SnapBreed AI is a <b>college mini-project</b> for  
    <b>SSCE Bangalore</b>.
    </p>

    <p style='color:white;'>
    <b>Purpose:</b><br>
    • Dog breed identification using AI<br>
    • TensorFlow image classifier<br>
    • Streamlit web UI<br>
    </p>
    </div>
    """, unsafe_allow_html=True)

    close_btn=st.button("Close",key="close_about")
    if close_btn:
        st.session_state.show_about=False 



# ---- UPLOAD CARD ----
st.markdown('<div class="upload-card">', unsafe_allow_html=True)
st.markdown('<div class="upload-title">Upload Picture</div>', unsafe_allow_html=True)

st.markdown('<div class="upload-box">', unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=['jpg', 'jpeg', 'png'])

st.markdown('<div class="upload-text">Drag and drop picture here, or browse your computer</div>',
            unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # End upload-box
st.markdown('</div>', unsafe_allow_html=True)  # End upload-card

# If user uploads
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.subheader("🔍 Detecting Breed...")

    # Load pretrained model
    @st.cache_resource
    def load_model():
        return tf.keras.applications.MobileNetV2(weights="imagenet")

    model = load_model()

    # Preprocess function
    def preprocess(img):
        img = img.resize((224, 224))
        img = np.array(img)
        img = tf.keras.applications.mobilenet_v2.preprocess_input(img)
        return np.expand_dims(img, axis=0)

    # Prediction
    image = Image.open(uploaded_file)
    processed = preprocess(image)

    preds = model.predict(processed)
    decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=3)

    # Extract dog breed only (filter non-dog classes)
    dog_labels = []
    for (_, label, prob) in decoded[0]:
        if any(x in label.lower() for x in ["dog", "hound", "terrier", "retriever", "shepherd", "pug", "husky"]):
            dog_labels.append((label.replace("_", " ").title(), prob))

    # If dog breed found
    if dog_labels:
        breed, confidence = dog_labels[0]
        st.success(f"**🥇 Predicted Breed:** {breed}")
        st.write(f"Confidence: `{confidence*100:.2f}%`")
    else:
        st.error("Could not identify a dog breed. Try another image.")
