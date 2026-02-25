import streamlit as st
import time
import os
import sys
import json
import websocket # websocket-client

# Allow importing from the root directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="Vishwas Raksha Hospital", page_icon="🏥", layout="wide")

# Modern, Calm Design System
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    
    .stApp {
        background-color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 600;
        color: #0F172A;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .stChatFloatingInputContainer {
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🏥 Vishwas Raksha Hospital</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748B;'>The Multi-Agent AI Hospital Orchestrator.</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Layout: Two columns
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📋 Patient Overview")
    with st.container(border=True):
        st.write("**Name:** John Doe")
        st.write("**Status:** Active Triage")
        st.progress(40, text="System Readiness")
        
    st.markdown("### �️ Agent Status")
    st.success("Receptionist: ACTIVE")
    st.success("Specialists: ONLINE")
    st.warning("Admin: AWAITING HITL")

with col2:
    st.markdown("### 💬 Live Chat (via FastAPI)")
    
    # Message Display
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("How can we help you today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            
            try:
                # Connect to FastAPI WebSocket
                ws = websocket.create_connection("ws://localhost:8000/chat")
                ws.send(json.dumps({"message": prompt, "patient_id": "jdoe_123"}))
                
                while True:
                    result = ws.recv()
                    data = json.loads(result)
                    
                    if "error" in data:
                        st.error(f"Backend Error: {data['error']}")
                        break
                    
                    if data.get("status") == "done":
                        break
                    
                    # Accumulate and display content
                    content = data.get("content", "")
                    node = data.get("node", "System")
                    
                    if content:
                        full_response += f"**[{node}]** {content}\n\n"
                        response_placeholder.markdown(full_response)
                
                ws.close()
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error(f"Could not connect to FastAPI backend at localhost:8000. Ensure 'python -m backend.main' is running. Error: {e}")
