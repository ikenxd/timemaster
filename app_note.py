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

# BG COLOR
st.markdown(
    """
    <style>
    .stApp {
        background-color: #5E3939;  /* light blue, change to any color */
    }
    </style>
    """,
    unsafe_allow_html=True
)



# TITLE/heading
st.title(
    "TimeMaster",
    text_alignment="center",
)

# Input field for note title
title = st.text_input("Name your schedule"),

# Text area for note content
notes = st.text_area("Desc/Notes")

dInput = st.date_input("Select a date",
                        value=date(2026,3,16),
                        min_value=date(2026,3,16),
                        max_value=date(2026,12,31)) 

st.write(f"You selected: {dInput}")

t = st.time_input ('Set an alarm for ', value=None)


# - - - - - - - - - - SIDEBAR - - - - - - - -
menu = st.sidebar.radio(
    "Menu",
    ["Add Schedule", "View Notes", "About"],
    key="main_menu"
)

if menu == "Add Schedule":

    st.title("TimeMaster")

    title = st.text_input(
        "Name your schedule",
        key="schedule_title_input"
    )

    notes = st.text_area(
        "Desc/Notes",
        key="schedule_notes_input"
    )

elif menu == "View Notes":

    st.subheader("Saved Notes")

    notes_docs = db.collection("notes").stream()

    for note in notes_docs:
        data = note.to_dict()

        st.write(data.get("title"))
        st.write(data.get("notes"))
        st.write(data.get("date"))

        st.divider()

elif menu == "About":

    st.write("TimeMaster")
    st.write("Simple scheduling app")


# ==============================
# FUNCTION: SAVE NOTE TO FIRESTORE
# ==============================

def save_note(title, notes, dInput):
    """
    Saves a note to the Firestore 'notes' collection
    """

    # Access (or create) the 'notes' collection
    db.collection("notes").add({
        "title": title,                     # Store title
        "notes": notes,                     # Store notes content
        "date": str(dInput)              # Convert date to string
    })

# ==============================
# SAVE BUTTON LOGIC
# ==============================

# Display Save button
if st.button("💾 Save Note"):
    
    # Validate input fields
    if title and notes:
        
        # Call function to save data
        save_note(title, notes, dInput)
        
        # Success message
        st.success("Note saved successfully!")
    
    else:
        # Warning if fields are empty
        st.warning("Please fill in both Title and Notes.")

# ==============================
# DISPLAY SAVED NOTES
# ==============================

st.divider()
st.subheader("📖 Saved Notes")

# Get all documents from the 'notes' collection
notes_docs = db.collection("notes").stream()

# Loop through each document
for note in notes_docs:
    
    # Convert Firestore document to Python dictionary
    data = note.to_dict()
    
    # Safely extract fields using .get()
    note_title = data.get("title", "No Title")
    note_content = data.get("notes", "No Notes")
    note_date = data.get("date", "No Date")

    # Display note data in Streamlit
    st.markdown(f"### {note_title}")
    st.write(note_content)
    st.caption(f"📅 {note_date}")
    st.divider()
