import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime
from zoneinfo import ZoneInfo
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

def evaluate_expression(expr_str):
    if not expr_str or pd.isna(expr_str):
        return 0.0
    cleaned = str(expr_str).strip()
    if not cleaned:
        return 0.0
    try:
        allowed_chars = set("0123456789+-*/(). ")
        if all(c in allowed_chars for c in cleaned):
            result = float(eval(cleaned))
            return result
        else:
            import re
            nums = re.findall(r"[-+]?\d*\.\d+|\d+", cleaned)
            if nums:
                return float(nums[0])
    except:
        pass
    return 0.0

current_logo_path = get_current_logo()
if current_logo_path:
    try:
        st.logo(current_logo_path, size="large")
    except:
        pass

st.markdown("""
    <style>
    /* إخفاء شريط الأدوات العلوي بالكامل (Header Toolbar) */
    header {visibility: hidden !important;}
    
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

try:
    guides_df = pd.read_excel(GUIDES_FILE)
    if 'Account' in guides_df.columns:
        guides_df['Account'] = guides_df['Account'].apply(clean_acc_number)
except:
    guides_df = pd.DataFrame({
        "Guide Name": ["أحمد", "محمود"],
        "Account Number": ["1805000493514500022", "1805000493514500033"]
    })
    guides_df.to_excel(GUIDES_FILE, index=False)

name_column = guides_df.columns[0] if len(guides_df.columns) > 0 else "Guide Name"
acc_column = guides_df.columns[1] if len(guides_df.columns) > 1 else guides_df.columns[0]

def get_guide_name_by_account(acc_val):
    if not acc_val:
        return "غير معروف"
    clean_acc = clean_acc_number(acc_val)
    matched = guides_df[guides_df[acc_column].apply(clean_acc_number) == clean_acc]
    if not matched.empty:
        return str(matched[name_column].values[0])
    return "غير معروف"

SHOPS_LIST = [
    "وجية بردى", "اخناتون سجاد", "مينا للبرديات", "رويال سجاد", "اولد كايرو",
    "رويال للعطور", "خان الحلو للقطن", "فلور قطن", "طيبة للقطن", "فيلة بازار",
    "جولدن بيرد", "mملوك", "ريحانة توابل", "كنور توابل", "قصر العطور", "لازوريت", "محلات اخري"
]

current_subs_df = load_data(SUBMISSIONS_FILE)
pending_count = len(current_subs_df)

cols_badge = st.columns([4, 1])
with cols_badge[1]:
    st.markdown(f"""
        <div style="background-color: #d8ebd8; border: 2px solid #28a745; padding: 8px 12px; border-radius: 10px; text-align: center; margin-bottom: 15px;">
            <span style="color: #1b5e20; font-weight: bold; font-size: 0.95rem;">🔔 الطلبات الجديدة: <span style="color: #d9534f; font-size: 1.1rem;">{pending_count}</span></span>
        </div>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; margin-top: 10px; margin-bottom: 5px;">
            <h2 style='color: #1b5e20; margin: 0; font-size: 1.2rem;'>🧭 القائمة الرئيسية</h2>
        </div>
        """, unsafe_allow_html=True)
    
    page = st.radio(
        "اختر الصفحة",
        ["نموذج تصفية المرشد", "سجلات المرشد", "إدارة التصفيات", "الأرشيف"],
        label_visibility="collapsed"
    )

if page == "نموذج تصفية المرشد":
    st.title("🧭 نموذج تصفية المرشدين")
    st.markdown("---")

    if "option_rows_count" not in st.session_state:
        st.session_state.option_rows_count = 1
    if "shop_rows_count" not in st.session_state:
        st.session_state.shop_rows_count = 1
    if "form_reset_counter" not in st.session_state:
        st.session_state.form_reset_counter = 0

    rc =
