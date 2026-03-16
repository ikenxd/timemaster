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



# userinftrerface

# Set background color
st.markdown(
    """
    <style>
    .stApp {
        background-color: #D1A292;  /* light blue, change to any color */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App title
st.title(
    "TimeMaster",
    text_alignment="center",
)
       


# Input field for note title
title = st.text_input("Name your schedule")

# Text area for note content
notes = st.text_area("Desc/Notes")

x = st.date_input("Select a date",
                        value=date(2026,3,16),
                        min_value=date(2026,3,16),
                        max_value=date(2026,12,31)) 

st.write(f"You selected: {x}")

t = st.time_input ('Set an alarm for ', value=None)









# ==============================
# FUNCTION: SAVE NOTE TO FIRESTORE
# ==============================

def save_note(title, notes, note_date):
    """
    Saves a note to the Firestore 'notes' collection
    """

    # Access (or create) the 'notes' collection
    db.collection("notes").add({
        "title": title,                     # Store title
        "notes": notes,                     # Store notes content
        "date": str(note_date)              # Convert date to string
    })

# ==============================
# SAVE BUTTON LOGIC
# ==============================

# Display Save button
if st.button("💾 Save Note"):
    
    # Validate input fields
    if title and notes:
        
        # Call function to save data
        save_note(title, notes, note_date)
        
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
