import streamlit as st
import requests
import json
import time

# --- CONFIGURATION ---
# Pointing to the Enterprise Backend Endpoint
API_URL = "http://127.0.0.1:8000/api/v1/scan"

# --- PAGE SETUP ---
st.set_page_config(layout="wide", page_title="Ulinzi IQ Enterprise Demo", page_icon="🛡️")

# Custom CSS for that "Banking App" feel
st.markdown("""
<style>
    .reportview-container { background: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 5px; height: 50px; }
    .bank-screen { 
        background-color: white; 
        padding: 20px; 
        border-radius: 15px; 
        border: 1px solid #ddd; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("🛡️ Ulinzi IQ: Enterprise Fraud SDK")
st.markdown("##### The Intelligence Layer protecting the 'Last Mile' of Digital Finance.")
st.divider()

col1, col2 = st.columns([1, 1], gap="large")

# =========================================================
# COLUMN 1: THE FRAUDSTER SIMULATOR
# =========================================================
with col1:
    st.subheader("🕵️ Threat Simulator")
    st.info("Inject a scenario into the user's clipboard/SMS inbox.")
    
    with st.container(border=True):
        # Inputs
        sender_input = st.text_input("Sender ID (Who sent it?)", value="0722123456")
        message_input = st.text_area("Message Content", 
                                     value="M-Pesa imefungiwa. Dial *33*4# ku-reverse transaction haraka.", 
                                     height=120)
        app_source = st.selectbox("Injection Source", ["SMS", "WhatsApp", "Web Browser"])
        
        st.write("") # Spacing
        if st.button("🚀 INJECT THREAT TO DEVICE", type="primary"):
            st.session_state['attack_live'] = True
            st.session_state['payload'] = {
                "sender": sender_input,
                "message": message_input,
                "source": app_source
            }
            st.success("✅ Threat Payload Active on Device")

# =========================================================
# COLUMN 2: THE BANKING APP (PROTECTED)
# =========================================================
with col2:
    st.subheader("📱 KCB / Equity Banking App")
    
    # Simulate the Phone UI
    with st.container():
        st.markdown('<div class="bank-screen">', unsafe_allow_html=True)
        st.markdown("### 💸 Send Money")
        st.text_input("Account Number", "123-456-789")
        st.text_input("Amount (KES)", "5,000")
        
        # LOGIC: INTERCEPT THE TRANSACTION
        if 'attack_live' in st.session_state and st.session_state['attack_live']:
            
            st.write("---")
            st.caption("🔒 Ulinzi Security Layer Scanning...")
            
            # 1. SEND DATA TO BACKEND
            try:
                # We add a slight delay to simulate network reality
                with st.spinner("Analyzing Context..."):
                    response = requests.post(API_URL, json=st.session_state['payload'])
                    
                if response.status_code == 200:
                    data = response.json()
                    
                    # Extract Data
                    score = data['risk_score']
                    level = data['risk_level']
                    flags = data['flags']
                    action = data['action']
                    speed = data['analysis_time_ms']
                    
                    # 2. DISPLAY METRICS
                    c1, c2 = st.columns(2)
                    c1.metric("Risk Score", f"{score}/100", delta_color="inverse")
                    c2.metric("Analysis Speed", f"{speed} ms")
                    
                    # 3. DECISION GATES
                    if action == "BLOCK":
                        st.error(f"⛔ TRANSACTION BLOCKED ({level})")
                        st.markdown("**Security Flags Detected:**")
                        for flag in flags:
                            st.write(f"- {flag}")
                        st.button("🔒 Send Money Disabled", disabled=True)
                        
                    elif action == "WARN":
                        st.warning(f"⚠️ SECURITY WARNING ({level})")
                        st.write("This transaction looks suspicious.")
                        with st.expander("See Reasons"):
                            for flag in flags:
                                st.write(f"- {flag}")
                        
                        col_a, col_b = st.columns(2)
                        col_a.button("❌ Cancel")
                        col_b.button("Proceed (I accept risk)")
                        
                    else: # ALLOW/SAFE
                        st.success(f"✅ SECURE ({level})")
                        if flags:
                            st.info(f"Note: {flags[0]}")
                        st.button("✅ Confirm Transfer")

                else:
                    st.error(f"Server Error: {response.status_code}")
                    st.write(response.text)

            except requests.exceptions.ConnectionError:
                st.error("🚨 Backend is Offline. Run 'uvicorn app.main:app' first.")

        else:
            # Normal State (No attack injected yet)
            st.write("---")
            st.button("Send Money")
            
        st.markdown('</div>', unsafe_allow_html=True)