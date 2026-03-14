import streamlit as st
import requests
import time

st.set_page_config(
    page_title="DevAssist AI", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a modern, smooth dark-mode friendly UI
st.markdown("""
<style>
    /* Main Layout */
    .main {
        padding-top: 2rem;
    }
    
    /* Headers */
    h1 {
        font-weight: 800 !important;
        font-size: 3rem !important;
        margin-bottom: 0rem !important;
        background: -webkit-linear-gradient(45deg, #FF4B2B, #FF416C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #888;
        margin-bottom: 2rem;
    }

    /* Input Field */
    .stTextInput > div > div > input {
        border-radius: 12px;
        padding: 16px;
        font-size: 18px;
        border: 1px solid #333;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #FF416C;
        box-shadow: 0 4px 12px rgba(255, 65, 108, 0.2);
    }
    
    /* Search Button */
    .stButton > button {
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: bold;
        background: linear-gradient(45deg, #FF4B2B, #FF416C);
        border: none;
        color: white;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(255, 65, 108, 0.3);
    }

    /* Result Cards */
    .source-box {
        background: #1E1E1E;
        border-left: 4px solid #FF416C;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        font-family: 'Inter', 'Courier New', monospace;
        font-size: 16px;
        line-height: 1.6;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        transition: transform 0.2s;
    }
    
    .source-box:hover {
        transform: translateX(5px);
    }
    
    /* Emtpy State */
    .empty-state {
        text-align: center;
        padding: 40px;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.image("https://img.icons8.com/nolan/96/artificial-intelligence.png", width=60)
    st.markdown("## 🧠 DevAssist AI")
    st.markdown("Your intellgent technical companion powered by **Endee Vector Database**.")
    
    st.divider()
    
    st.markdown("### 🎯 Quick Examples")
    st.markdown("- *\"How do I manage state in React?\"*")
    st.markdown("- *\"What is FastAPI?\"*")
    st.markdown("- *\"How does binary search work?\"*")
    
    st.divider()
    
    st.markdown("### ⚙️ Architecture")
    st.caption("Engine: `all-MiniLM-L6-v2`")
    st.caption("Storage: `Endee Vector REST API` / `NumPy Fallback`")

# Main Content Area
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    st.markdown("<h1>DevAssist AI</h1>", unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Semantic codebase search built on top of Endee Vector capabilities.</p>', unsafe_allow_html=True)

    # Search Interface
    question = st.text_input("", placeholder="Ask anything, e.g., 'What are Python dictionaries?'")

    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        search_clicked = st.button("Search Knowledge Base")

    st.markdown("<br><br>", unsafe_allow_html=True)

    if search_clicked:
        if not question.strip():
            st.warning("Please enter a question to begin searching.")
        else:
            with st.spinner("Searching the knowledge base..."):
                try:
                    time.sleep(0.4) # UI polish delay
                    
                    response = requests.get(
                        "http://127.0.0.1:8000/ask",
                        params={"question": question}
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        st.markdown("### 📚 Retrieved Context")
                        if data["results"] and not data["results"][0].startswith("No relevant"):
                            for r in data["results"]:
                                st.markdown(f'<div class="source-box">{r}</div>', unsafe_allow_html=True)
                        else:
                            st.warning("No relevant context found in the database. Please try rephrasing or ask another question.")
                            
                    else:
                        st.error(f"Error: {response.status_code} - The backend returned an unexpected response.")
                        
                except requests.exceptions.ConnectionError:
                    st.error("🚨 Failed to connect to the backend. Is the FastAPI server running?")
    else:
        # Empty State
        st.markdown(
            '<div class="empty-state"><h3>Ready to help.</h3><p>Type a technical question above to search your embedded knowledge base.</p></div>', 
            unsafe_allow_html=True
        )
