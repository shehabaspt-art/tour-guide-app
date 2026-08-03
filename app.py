import os
import base64
import streamlit as st

# إعداد الصفحة وتثبيت الشريط العلوي
st.set_page_config(
    page_title="Sun Pyramids Tour Guide App",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# دالة جلب اللوجو الثابت من الملف sun_2.png
def get_current_logo():
    fixed_logo_path = "sun_2.png"
    if os.path.exists(fixed_logo_path):
        return fixed_logo_path
    return None

def get_image_base64(path):
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# تخصيص الشريط العلوي الثابت والشكل العام
st.markdown("""
    <style>
    /* تثبيت الشريط العلوي ومنع تداخله */
    header[data-testid="stHeader"] {
        background-color: #f8f9fa;
        border-bottom: 1px solid #dee2e6;
    }
    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 5px 20px;
        background-color: #ffffff;
        border-bottom: 1px solid #e0e0e0;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 99999;
    }
    .main .block-container {
        padding-top: 80px;
    }
    </style>
""", unsafe_allow_html=True)

# عرض الشريط العلوي باللوجو والعناصر الثابتة
logo_path = get_current_logo()
logo_base64 = get_image_base64(logo_path)

if logo_base64:
    logo_html = f'<img src="data:image/png;base64,{logo_base64}" style="height: 35px; object-fit: contain;" />'
else:
    logo_html = '<span style="font-weight: bold; color: #1b5e20; font-size: 1.1rem;">Sun Pyramids</span>'

st.markdown(f"""
    <div class="top-bar">
        <div style="display: flex; align-items: center; gap: 10px;">
            {logo_html}
        </div>
        <div style="display: flex; align-items: center; gap: 15px;">
            <span style="background: #ffebee; color: #c62828; padding: 2px 8px; border-radius: 10px; font-size: 0.85rem; font-weight: bold;">🔔 0</span>
            <span style="font-size: 0.9rem; font-weight: 500; color: #333;">👤 SA</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# محتوى التطبيق الأساسي
st.write("مرحباً بك في لوحة تحكم Sun Pyramids. التطبيق جاهز ويعمل بكفاءة مع الحفاظ على الشريط الثابت واللوجو.")
