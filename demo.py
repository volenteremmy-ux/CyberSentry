import streamlit as st
import requests
import json
import time

# --- CONFIGURATION ---
# Pointing to the Enterprise Backend Endpoint
API_URL = "http://127.0.0.1:8000/api/v1/scan"

# --- PAGE SETUP ---
st.set_page_config(layout="wide", page_title="Ulinzi Enterprise Demo", page_icon="🛡️")

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
st.title("🛡️ Ulinzi: Enterprise Fraud SDK")
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
                                     value="M-Pesa imefungwa. Dial *33*4# ku-reverse action haraka.", 
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

import streamlit as st
import requests
import pandas as pd
import numpy as np
import time

# CONFIGURATION
API_BASE = "http://127.0.0.1:8000/api/v1"

st.set_page_config(layout="wide", page_title="Ulinzi IQ Enterprise", page_icon="🛡️")

# CSS for Dashboard Cards
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        border: 1px solid #ddd;
    }
    .big-number { font-size: 2em; font-weight: bold; color: #ff4b4b; }
</style>
""", unsafe_allow_html=True)

# TABS
tab1, tab2, tab3 = st.tabs(["📱 Simulation Demo", "🏦 Bank CISO Dashboard", "📢 User Reporting"])

# ==========================================
# TAB 1: THE SIMULATOR (Existing Logic)
# ==========================================
with tab1:
    st.header("Real-Time Transaction Defense")
    
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.subheader("Attacker Console")
        with st.container(border=True):
            sender_input = st.text_input("Sender ID", "0722123456")
            message_input = st.text_area("Message", "M-Pesa imefungiwa. Dial *33*4#.")
            if st.button("🚀 Inject Threat"):
                st.session_state['payload'] = {"sender": sender_input, "message": message_input, "source": "SMS"}
                st.session_state['attack_live'] = True
                st.success("Threat Injected")

    with c2:
        st.subheader("Client Device (Protected)")
        if 'attack_live' in st.session_state:
            if st.button("Simulate 'Send Money'"):
                with st.spinner("Ulinzi SDK Scanning..."):
                    try:
                        res = requests.post(f"{API_BASE}/scan", json=st.session_state['payload'])
                        data = res.json()
                        if data['action'] == "BLOCK":
                            st.error(f"⛔ BLOCKED: {data['risk_level']} (Score: {data['risk_score']})")
                            st.write(f"Flags: {data['flags']}")
                        else:
                            st.success("✅ Safe to Process")
                    except:
                        st.error("Backend Offline")

# ==========================================
# TAB 2: THE BANK DASHBOARD (New Feature)
# ==========================================
with tab2:
    st.header("🛡️ Ulinzi Threat Intelligence Center")
    st.markdown("Live view of fraud attempts across the network.")
    
    # Refresh Button
    if st.button("🔄 Refresh Live Data"):
        st.rerun()

    # Fetch Data
    try:
        res = requests.get(f"{API_BASE}/stats")
        stats = res.json()
        
        # 1. TOP METRICS
        m1, m2, m3 = st.columns(3)
        with m1: st.metric("Total Scans Today", stats['total_scans'], "+12%")
        with m2: st.metric("Threats Blocked", stats['threats_blocked'], "+5%", delta_color="inverse")
        with m3: st.metric("System Latency", "42ms", "-5ms")
        
        st.divider()
        
        # 2. HEATMAP & TRENDS
        d1, d2 = st.columns([2, 1])
        
        with d1:
            st.subheader("📍 Attack Origin Heatmap")
            map_data = pd.DataFrame(stats['heatmap'])
            st.map(map_data, zoom=6)
            
        with d2:
            st.subheader("🔥 Active Campaigns")
            for campaign in stats['active_campaigns']:
                st.error(f"⚠️ {campaign}")
                
            st.subheader("📝 Recent Reports")
            if stats['recent_reports']:
                for report in stats['recent_reports']:
                    st.caption(f"From: {report['sender']}")
                    st.text(f"Msg: {report['message'][:30]}...")
            else:
                st.info("No manual reports yet.")

    except:
        st.warning("Start the backend to see live data.")

# ==========================================
# TAB 3: USER REPORTING (Crowdsourcing)
# ==========================================
with tab3:
    st.header("📢 Report a Scam")
    st.markdown("Help protect the Ulinzi Network by reporting new scams.")
    
    with st.form("report_form"):
        r_sender = st.text_input("Scammer Number")
        r_msg = st.text_area("Message Received")
        r_cat = st.selectbox("Category", ["Phishing", "Extortion", "Fake Reward", "Job Scam"])
        
        submitted = st.form_submit_button("Submit Report")
        if submitted:
            payload = {"sender": r_sender, "message": r_msg, "category": r_cat}
            requests.post(f"{API_BASE}/report", json=payload)
            st.success("Report Submitted! The database has been updated.")