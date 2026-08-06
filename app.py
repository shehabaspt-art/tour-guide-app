import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime
import time

# ضبط إعدادات الصفحة
st.set_page_config(
    page_title="Sun Pyramids Tours",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

SUBMISSIONS_FILE = "submissions.xlsx"
ARCHIVE_FILE = "archive.xlsx"
GUIDES_FILE = "guides.xlsx"
GUIDE_ARCHIVE_FILE = "guide_archive.xlsx"

def get_current_logo():
    fixed_logo_path = "sun_2.png"
    if os.path.exists(fixed_logo_path):
        return fixed_logo_path
    return None

def clean_acc_number(val):
    if val is None:
        return ""
    s_val = str(val).strip()
    if s_val.endswith('.0'):
        s_val = s_val[:-2]
    if s_val.startswith('0'):
        s_val = s_val[1:]
    return s_val

def load_data(file_path):
    if os.path.exists(file_path):
        try:
            df = pd.read_excel(file_path)
            if 'Guide Name' not in df.columns:
                df['Guide Name'] = 'غير معروف'
            if 'Timestamp' not in df.columns:
                df['Timestamp'] = 'غير محدد'
            if 'Account' in df.columns:
                df['Account'] = df['Account'].apply(clean_acc_number)
            return df
        except:
            return pd.DataFrame()
    return pd.DataFrame()

def save_to_file(file_path, new_data):
    df = load_data(file_path)
    new_df = pd.DataFrame([new_data])
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_excel(file_path, index=False)

def overwrite_data(file_path, df):
    df.to_excel(file_path, index=False)

def parse_items_smart(raw_text):
    if not raw_text or pd.isna(raw_text):
        return []
    text_str = str(raw_text).strip()
    if not text_str:
        return []
    
    if "|||" in text_str:
        parts = text_str.split("|||")
    elif "|" in text_str:
        parts = text_str.split("|")
    else:
        parts = [text_str]
        
    return [p.strip() for p in parts if p.strip()]

current_logo_path = get_current_logo()
if current_logo_path:
    try:
        st.logo(current_logo_path, size="large")
    except:
        pass

st.markdown("""
    <style>
    div.stFormSubmitButton > button, div.stButton > button {
        border-radius: 8px !important;
        background-color: #28a745 !important;
        color: white !important;
        border: none !important;
    }
    div.stFormSubmitButton > button:hover, div.stButton > button:hover {
        background-color: #218838 !important;
        color: white !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: transparent !important;
        border-left: none !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        background-color: #d8ebd8 !important;
        border-right: 2px solid #c2e0c2 !important;
        border-bottom: 2px solid #c2e0c2 !important;
        border-top: 2px solid #c2e0c2 !important;
        border-radius: 0 15px 15px 0 !important;
        margin-top: 0rem !important;
        padding-top: 1.5rem !important;
        height: 100vh !important;
    }
    
    [data-testid="stSidebar"] img {
        max-width: 100% !important;
        width: 260px !important;
        height: auto !important;
    }

    [data-testid="stSidebar"] .stRadio > label {
        display: none !important;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {
        background-color: #ffffff !important;
        padding: 10px 14px !important;
        border-radius: 10px !important;
        border: 1px solid #a3d9a3 !important;
        margin-bottom: 8px !important;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label p {
        font-weight: 700 !important;
        color: #1b5e20 !important;
        font-size: 0.95rem !important;
        margin: 0 !important;
    }

    .record-card {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-right: 5px solid #28a745;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        direction: rtl;
    }
    .card-header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #f0f0f0;
        padding-bottom: 8px;
        margin-bottom: 10px;
    }
    .card-id {
        background: #eef2ff;
        color: #4f46e5;
        font-weight: bold;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 13px;
    }
    .card-file {
        color: #1f2937;
        font-size: 15px;
        font-weight: bold;
    }
    .card-body-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #4b5563;
        font-size: 14px;
        flex-wrap: wrap;
        gap: 10px;
    }
    .card-guide {
        font-weight: 600;
        color: #1b5e20;
    }
    .card-time {
        direction: ltr;
        unicode-bidi: embed;
        color: #6c757d;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)
