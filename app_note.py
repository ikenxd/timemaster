import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import date

# ==============================


# ==============================

# Check if Firebase is already initialized
# This prevents errors because Streamlit reruns the script
if not firebase_admin._apps:
    
    # Load Firebase credentials securely from Streamlit secrets
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    
    # Initialize Firebase using the credentials
    firebase_admin.initialize_app(cred)

# Create a Firestore database client
db = firestore.client()

# = = = = = = = = = = = = = = = = = = =

import streamlit as st
from datetime import date

# =========================
# STYLE
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #5E3939;
}
h1, h2, h3, label {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.title("TimeMaster")

# =========================
# INPUT SECTION
# =========================

title = st.text_input("Name your schedule")

notes = st.text_area("Desc / Notes")

selected_date = st.date_input(
    "Select a date",
    value=date(2026,3,16),
    min_value=date(2026,3,16),
    max_value=date(2026,12,31)
)

alarm_time = st.time_input("Set an alarm for", value=None)

st.write(f"You selected: {selected_date}")

# ======= SIDEBAR ========


menu = st.sidebar.radio(
    "Menu",
    ["Add Schedule", "View Notes", "About"],
    key="main_menu"
)

st.sidebar.title("Settings")
if 'theme' not in st.session_state:
    st.session_state.theme = "purple"  # default theme

def toggle_theme():
    if st.session_state.theme == "purple":
        st.session_state.theme = "red"
    else:
        st.session_state.theme = "purple"

st.sidebar.button("Change Theme", on_click=toggle_theme)

# Apply background color based on theme
if st.session_state.theme == "purple":
    bg_color = "#5D395E"
    text_color = "#D2B6D3"
else:
    bg_color = "#5E3939"  
    text_color = "#D3B6B6"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# App content
st.title("TimeMaster App")
st.write("Your current theme is", st.session_state.theme)





# =========================
# SAVE FUNCTION
# =========================

def save_note(title, notes, note_date):
    db.collection("notes").add({
        "title": title,
        "notes": notes,
        "date": str(note_date)
    })

# =========================
# SAVE BUTTON
# =========================

if st.button("💾 Save Note"):

    if title and notes:
        save_note(title, notes, selected_date)
        st.success("Note saved successfully!")

    else:
        st.warning("Please fill in both Title and Notes.")

# =========================
# DISPLAY NOTES
# =========================

st.divider()
st.subheader("📖 Saved Notes")

notes_docs = db.collection("notes").stream()

for note in notes_docs:

    data = note.to_dict()

    note_title = data.get("title", "No Title")
    note_content = data.get("notes", "No Notes")
    note_date = data.get("date", "No Date")

    st.markdown(f"### {note_title}")
    st.write(note_content)
    st.caption(f"📅 {note_date}")
    st.divider()
