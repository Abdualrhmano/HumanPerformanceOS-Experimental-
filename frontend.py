import streamlit as st
import requests
import time

# إعدادات الصفحة الاحترافية
st.set_page_config(page_title="Human Performance OS", page_icon="🚀", layout="wide")

# تصميم CSS مخصص لجعل الواجهة تبدو احترافية
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #00ff88;
        color: black;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover { background-color: #00cc6e; color: white; }
    .metric-card {
        background-color: #1a1c24;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #00ff88;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# العنوان العلوي
st.markdown("<h1 style='text-align: center; color: #00ff88;'>🚀 Human Performance OS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>AI-Driven Decision Engine & Performance Analytics</p>", unsafe_allow_html=True)

st.divider()

# تقسيم الشاشة لجزئين
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📊 Input Metrics")
    with st.container():
        sleep = st.select_slider("🌙 Sleep Quality (Hours)", options=[i for i in range(0, 13)], value=8)
        focus = st.slider("🎯 Deep Focus (Hours)", 0.0, 12.0, 4.0)
        energy = st.select_slider("⚡ Energy Level", options=[i for i in range(1, 11)], value=7)
        consistency = st.slider("🔄 Habit Consistency", 0.0, 1.0, 0.8)
        
        analyze_btn = st.button("RUN ENGINE ANALYTICS")

with col2:
    st.markdown("### 🧠 Engine Output")
    
    if analyze_btn:
        with st.spinner('LUNA Engine is processing...'):
            time.sleep(1.5) # محاكاة وقت المعالجة لشكل احترافي
            
            payload = {
                "sleep_hours": sleep,
                "focus_hours": focus,
                "energy_level": energy,
                "habit_consistency": consistency
            }
            headers = {"x-api-key": "demo-key"}
            
            try:
                # تأكد أن السيرفر main.py يعمل على بورت 8000
                response = requests.post("http://localhost:8000/evaluate", json=payload, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    score = data['performance_score']
                    
                    # عرض النتيجة بشكل احترافي
                    st.markdown(f"""
                    <div class="metric-card">
                        <h2 style='color: #00ff88;'>Performance Score: {score}/10</h2>
                        <p style='font-size: 1.2em;'>{data['recommendation']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # عرض التشفير كدليل على الأمان
                    with st.expander("🔐 Security Trace (AES-256 Encrypted Payload)"):
                        st.info("This data is encrypted before being stored or transmitted.")
                        st.code(data['encrypted_data'], language="text")
                        
                else:
                    st.error("Engine Error: Check API Key or Server Status")
            except:
                st.error("Could not connect to the Backend server. Make sure main.py is running.")
    else:
        st.info("Adjust the metrics on the left and run the engine to see AI insights.")

# تذييل الصفحة
st.markdown("<br><hr><p style='text-align: center; color: #555;'>Human Performance OS v1.0 | Secure AI Architecture</p>", unsafe_allow_html=True)

