import streamlit as st
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
    margin-top: -10px;
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
    st.markdown("""
    <div class='menu-box'>
        <div class='menu-item'>Gallery</div>
        <div class='menu-item'>About</div>
    </div>
    """, unsafe_allow_html=True)


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
