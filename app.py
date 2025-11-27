import streamlit as st
import time

# 1. THE AI BRAIN (Simulated for speed, or plug in Hugging Face here)
def scan_message(text):
    # List of danger words for the demo (Sheng/Swahili/English)
    danger_words = ["blocked", "fungwa", "tuma", "refund", "kra", "suspended", "urgent", "click here"]
    
    text_lower = text.lower()
    
    # Simple Keyword Logic (Fast & Reliable for Demo)
    for word in danger_words:
        if word in text_lower:
            return True, "High Risk", f"Detected Keyword: '{word}' indicating urgency or fraud."
            
    return False, "Safe", "No threats detected."

# 2. THE UI (Streamlit)
st.set_page_config(layout="wide", page_title="CyberSentry Demo")

# Custom CSS to make the right column look like a phone
st.markdown("""
<style>
    .phone-screen {
        border: 10px solid #333;
        border-radius: 20px;
        padding: 20px;
        background-color: #f0f2f6;
        height: 500px;
    }
    .alert-box {
        background-color: #ff4b4b;
        color: white;
        padding: 15px;
        border-radius: 10px;
        font-weight: bold;
        animation: blink 1s infinite;
    }
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

# COLUMN 1: THE SCAMMER (You controlling the demo)
with col1:
    st.header("🕵️ The Attacker")
    st.write("Simulate an incoming SMS or WhatsApp message.")
    
    scam_text = st.text_area("Type a message here:", 
                             "KRA: Your PIN has been suspended. Click bit.ly/kra-login to update immediately.")
    
    if st.button("Send Message"):
        st.session_state['incoming_msg'] = scam_text
        st.session_state['scanning'] = True

# COLUMN 2: THE VICTIM (The Phone Screen)
with col2:
    st.header("📱 User's Phone")
    
    # Create a container that looks like a phone
    with st.container():
        st.markdown('<div class="phone-screen">', unsafe_allow_html=True)
        st.subheader("WhatsApp")
        
        # Check if message exists
        if 'incoming_msg' in st.session_state:
            # Display the message
            st.chat_message("user").write(st.session_state['incoming_msg'])
            
            # Run the Scan
            is_scam, status, reason = scan_message(st.session_state['incoming_msg'])
            
            if is_scam:
                # Show the CYBERSENTRY OVERLAY
                st.markdown(f"""
                <div class="alert-box">
                    CYBERSENTRY ALERT <br>
                    {status}: {reason} <br>
                    DO NOT CLICK
                </div>
                """, unsafe_allow_html=True)
            else:
                st.success("CyberSentry Scanned: Safe")
                
        st.markdown('</div>', unsafe_allow_html=True)