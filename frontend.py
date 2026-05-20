import streamlit as st
import requests
from PIL import Image

# 1. PAGE CONFIGURATION (Must be absolute first command)
# Using logo.png for the browser tab / app icon
try:
    icon_img = Image.open("logo.png")
    st.set_page_config(page_title="Ustad.ai", page_icon=icon_img, layout="centered", initial_sidebar_state="collapsed")
except FileNotFoundError:
    st.set_page_config(page_title="Ustad.ai", page_icon="✨", layout="centered", initial_sidebar_state="collapsed")

# 2. SESSION STATE MANAGEMENT (The Engine)
# This acts as our app's memory for navigation and user profiles
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'login'
if 'role' not in st.session_state:
    st.session_state.role = None
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}

def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()

def logout():
    st.session_state.current_page = 'login'
    st.session_state.role = None
    st.session_state.user_profile = {}
    st.rerun()

# 3. GLOBAL CSS FOR PREMIUM UI
st.markdown("""
<style>
    #MainMenu, header, footer {visibility: hidden;}
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    
    .card {
        background-color: #1E1E24;
        border: 1px solid #333333;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    
    .stButton > button {
        width: 100%;
        background-color: #00FFCC !important;
        color: #0A0A0A !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        transition: 0.2s;
    }
    .stButton > button:hover {
        background-color: #00E6B8 !important;
        transform: translateY(-2px);
    }
    .secondary-btn > button {
        background-color: #2b2b36 !important;
        color: #FAFAFA !important;
        border: 1px solid #444 !important;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to load Logo2.png inside the app
def display_app_header():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            main_logo = Image.open("Logo2.png")
            st.image(main_logo, use_container_width=True)
        except FileNotFoundError:
            st.markdown("<h2 style='text-align: center; color: #00FFCC;'>Ustad.ai Logo2 Missing</h2>", unsafe_allow_html=True)
    st.markdown("---")

# ==========================================
# PAGE VIEWS
# ==========================================

# --- PAGE 1: LOGIN INTERFACE ---
if st.session_state.current_page == 'login':
    display_app_header()
    st.markdown("<h2 style='text-align: center;'>Welcome to Ustad.ai</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8892B0;'>Select your portal to continue.</p>", unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='card' style='text-align: center;'><h3>Looking for a Service?</h3><br>Find verified local experts instantly.</div>", unsafe_allow_html=True)
        if st.button("Login as Customer"):
            st.session_state.role = "Customer"
            navigate_to("setup_profile")
            
    with col2:
        st.markdown("<div class='card' style='text-align: center;'><h3>Are you a Provider?</h3><br>Connect with local leads and grow.</div>", unsafe_allow_html=True)
        if st.button("Login as Provider"):
            st.session_state.role = "Provider"
            navigate_to("setup_profile")

# --- PAGE 2: PROFILE SETUP ---
elif st.session_state.current_page == 'setup_profile':
    st.button("← Back to Login", on_click=logout, key="back_btn")
    
    st.markdown(f"<h2>{st.session_state.role} Profile Setup</h2>", unsafe_allow_html=True)
    st.markdown("Please complete your registration to access the dashboard.")
    
    with st.form("profile_form"):
        name = st.text_input("Full Name")
        phone = st.text_input("Phone Number")
        city = st.selectbox("City", ["Rawalpindi", "Islamabad", "Lahore", "Karachi"])
        
        # Provider-specific fields
        if st.session_state.role == "Provider":
            trade = st.selectbox("Primary Trade", ["Electrician", "Plumber", "HVAC Technician", "Carpenter", "Painter"])
            experience = st.slider("Years of Experience", 1, 30, 5)
        
        submit = st.form_submit_button("Complete Setup & Enter App")
        
        if submit:
            if name and phone:
                st.session_state.user_profile['name'] = name
                st.session_state.user_profile['city'] = city
                if st.session_state.role == "Provider":
                    st.session_state.user_profile['trade'] = trade
                navigate_to("dashboard")
            else:
                st.error("Name and Phone Number are required.")

# --- PAGE 3: MAIN DASHBOARD (Customer or Provider) ---
elif st.session_state.current_page == 'dashboard':
    
    # Top Navigation Bar
    col_nav1, col_nav2 = st.columns([4, 1])
    with col_nav1:
        st.markdown(f"**Welcome, {st.session_state.user_profile.get('name', 'User')}!** | {st.session_state.user_profile.get('city', 'Location')}")
    with col_nav2:
        st.button("Log Out", on_click=logout, key="logout_btn")
        
    display_app_header()

    # --- CUSTOMER VIEW ---
    if st.session_state.role == "Customer":
        st.markdown("<h3>Request an On-Demand Expert</h3>", unsafe_allow_html=True)
        
        query = st.text_area(
            "Describe your need:",
            placeholder="e.g., I need a plumber near 22 no. Chungi...",
            label_visibility="collapsed",
            height=120
        )

        if st.button("Find Provider"):
            if query.strip() == "":
                st.warning("Please describe your requirement first.")
            else:
                with st.spinner("Analyzing request via AI Orchestrator..."):
                    try:
                        response = requests.post(
                            "http://127.0.0.1:8000/orchestrate",
                            json={"user_id": "test_user_001", "query": query}
                        )
                        if response.status_code == 200:
                            # The AI matched successfully, now render the beautiful UI Card
                            st.markdown("---")
                            st.markdown("<h3 style='color: #00FFCC;'>✅ Optimal Provider Matched</h3>", unsafe_allow_html=True)
                            
                            # Using an expander/container to act as a sleek profile card
                            with st.container(border=True):
                                col_avatar, col_info, col_actions = st.columns([1, 2.5, 1.5])
                                
                                with col_avatar:
                                    # A clean, modern avatar placeholder
                                    st.markdown(
                                        """
                                        <div style='font-size: 65px; text-align: center; background-color: #2b2b36; border-radius: 50%; height: 100px; width: 100px; line-height: 100px; margin: auto;'>
                                        👨‍🔧
                                        </div>
                                        """, 
                                        unsafe_allow_html=True
                                    )
                                    
                                with col_info:
                                    st.markdown("<h4 style='margin-bottom: 0px;'>Amjad Khan</h4>", unsafe_allow_html=True)
                                    st.markdown("<p style='color: #8892B0; font-size: 14px; margin-top: 0px;'>Master Plumber • Background Verified</p>", unsafe_allow_html=True)
                                    st.markdown("**⭐ 4.9/5** (142 Reviews)")
                                    st.markdown("📍 *2.4 km away (Est. arrival: 15 mins)*")
                                    
                                with col_actions:
                                    st.write("") # Spacer to vertically align buttons
                                    st.button("📞 Call Now", use_container_width=True)
                                    st.button("📅 Book Visit", type="primary", use_container_width=True)
                                    
                            st.caption("*AI Communication Note: Provider interface automatically localized to Roman Urdu based on your profile.*")

                        else:
                            st.error(f"Backend Error: {response.status_code}")
                    except Exception:
                        st.error("Server unreachable. Ensure your FastAPI backend is running.")

    # --- PROVIDER VIEW ---
    elif st.session_state.role == "Provider":
        trade = st.session_state.user_profile.get('trade', 'Expert')
        st.markdown(f"<h3>Your Lead Marketplace ({trade})</h3>", unsafe_allow_html=True)
        
        # Mock active leads
        st.markdown("""
        <div class='card'>
            <h4 style='color: #00FFCC;'>Urgent Lead: Pipe Leak</h4>
            <p><b>Location:</b> Chungi no. 22, Rawalpindi<br><b>Distance:</b> 2.4 km away.</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("Accept Lead", key="accept_1")
        
        st.markdown("""
        <div class='card'>
            <h4 style='color: #8892B0;'>Standard Lead: Mixer Installation</h4>
            <p><b>Location:</b> Saddar, Rawalpindi<br><b>Distance:</b> 5.1 km away.</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("Accept Lead", key="accept_2")