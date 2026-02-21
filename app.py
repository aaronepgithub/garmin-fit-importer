import streamlit as st
import os
import tempfile
from garminconnect import Garmin
import logging

# Page configuration
st.set_page_config(
    page_title="Garmin FIT Importer",
    page_icon="⌚",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Custom CSS for a premium look
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        border-color: #0056b3;
    }
    .upload-section {
        padding: 2rem;
        border-radius: 10px;
        background-color: #1e2130;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

SESSION_DIR = os.path.expanduser("~/.garmin_session")

def login(email, password):
    """Log in to Garmin Connect with session persistence."""
    client = Garmin(email, password)
    
    try:
        if os.path.exists(SESSION_DIR):
            client.login(SESSION_DIR)
        else:
            client.login()
            os.makedirs(SESSION_DIR, exist_ok=True)
            client.garth.dump(SESSION_DIR)
        return client
    except Exception as e:
        # Try fresh login if session fails
        if os.path.exists(SESSION_DIR):
            try:
                client = Garmin(email, password)
                client.login()
                client.garth.dump(SESSION_DIR)
                return client
            except Exception as e2:
                raise Exception(f"Login failed: {e2}")
        else:
            raise Exception(f"Login failed: {e}")

def main():
    st.markdown("<h1 style='text-align: center;'>⌚ Garmin Connect FIT Importer</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>Seamlessly sync your training data from external platforms to Garmin.</p>", unsafe_allow_html=True)
    st.divider()

    # Sidebar for Credentials and Info
    with st.sidebar:
        st.header("🔑 Authentication")
        email = st.text_input("Garmin Email", value=os.environ.get("GARMIN_EMAIL", ""), placeholder="example@email.com")
        password = st.text_input("Garmin Password", value=os.environ.get("GARMIN_PASSWORD", ""), type="password")
        
        if st.button("Test Connection"):
            if not email or not password:
                st.error("Please enter both email and password.")
            else:
                with st.spinner("Connecting to Garmin..."):
                    try:
                        client = login(email, password)
                        st.success("Connected successfully!")
                        st.session_state['client'] = client
                    except Exception as e:
                        st.error(str(e))
        
        st.divider()
        st.header("ℹ️ Instructions")
        st.markdown("""
        1. **Login**: Enter your Garmin Connect credentials.
        2. **Select Files**: Drag and drop your `.fit` files.
        3. **Upload**: Click 'Start Upload' to sync them.
        
        *Commonly used for MyWhoosh, Zwift, or other raw FIT exports.*
        """)

    # Main area for file upload
    col1, col2 = st.columns([1, 4])
    with col1:
        st.subheader("📂 Files")
    with col2:
        uploaded_files = st.file_uploader("Drop your FIT files here", type=["fit"], accept_multiple_files=True, label_visibility="collapsed")

    if uploaded_files:
        st.info(f"📌 {len(uploaded_files)} file(s) ready for upload.")
        
        if st.button("🚀 Start Sync to Garmin"):
            if 'client' not in st.session_state:
                if not email or not password:
                    st.error("Missing credentials. Please check the sidebar.")
                else:
                    with st.spinner("Authenticating..."):
                        try:
                            st.session_state['client'] = login(email, password)
                        except Exception as e:
                            st.error(str(e))
                            return

            client = st.session_state['client']
            
            progress_container = st.container()
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
                results_log = st.expander("Detailed Upload Log", expanded=True)
            
            success_count = 0
            for i, uploaded_file in enumerate(uploaded_files):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".fit") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name

                try:
                    status_text.text(f"Syncing: {uploaded_file.name}...")
                    client.upload_activity(tmp_path)
                    success_count += 1
                    results_log.success(f"✅ {uploaded_file.name}: Uploaded")
                except Exception as e:
                    if "409" in str(e) or "Conflict" in str(e):
                        results_log.warning(f"🟡 {uploaded_file.name}: Already exists in Garmin")
                    else:
                        results_log.error(f"❌ {uploaded_file.name}: {str(e)}")
                finally:
                    os.remove(tmp_path)
                
                progress_bar.progress((i + 1) / len(uploaded_files))

            status_text.text("Sync complete!")
            st.success(f"🎉 Successfully synced {success_count} out of {len(uploaded_files)} files.")
            st.balloons()

if __name__ == "__main__":
    main()
