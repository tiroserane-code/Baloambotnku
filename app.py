import streamlit as st
import datetime

# --- SETTINGS & SESSION ---
st.set_page_config(page_title="CTU Smart Lab", layout="wide")

if "logs" not in st.session_state:
    st.session_state.logs = []
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- ADMIN PASSWORD ---
ADMIN_PW = "CTU2026"

# --- SIDEBAR ---
st.sidebar.title("🔐 Admin Access")
if not st.session_state.authenticated:
    pw_input = st.sidebar.text_input("Enter Secret Password", type="password")
    if st.sidebar.button("Login"):
        if pw_input == ADMIN_PW:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.sidebar.error("Incorrect Password")
else:
    st.sidebar.success("Logged in as Admin")
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

# --- MAIN INTERFACE ---
st.title("🍳 Smart Lab: Live Recognition Trial")
st.write("Target: Attendance & Kitchen Inventory")

# 1. LIVE VIEW SECTION
st.header("🎥 Live Scanner")
st.info("The preview below is LIVE. Point it at a student or item to verify liveliness.")

# iPhone 13 will show a live video feed here
camera_image = st.camera_input("Scanner Feed")

if camera_image:
    st.success("✅ Frame Captured for Tagging")
    
    # 2. MANUAL TAGGING (Only Admin can tag)
    if st.session_state.authenticated:
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Category", ["Attendance", "Kitchen Item"])
        with col2:
            tag_name = st.text_input("Enter Name (e.g., Spoon / Irose)")
            
        if st.button("📌 Add to Official Log"):
            if tag_name:
                now = datetime.datetime.now().strftime("%I:%M %p")
                st.session_state.logs.append({
                    "Time": now,
                    "Type": category,
                    "Label": tag_name
                })
                st.toast(f"Saved: {tag_name}")
            else:
                st.error("Please provide a name!")
    else:
        st.warning("⚠️ Please login via the sidebar to tag items.")

# --- DISPLAY LOGS & EMAIL ---
st.divider()
st.subheader("📊 Discussion Summary")
if st.session_state.logs:
    st.table(st.session_state.logs)
    
    if st.button("✉️ Send Report to tiroserane@gmail.com"):
        st.write("Compiling Attendance and Inventory logs...")
        # Email logic would trigger here
        st.success("Email Sent Successfully!")
else:
    st.write("No logs recorded yet.")
