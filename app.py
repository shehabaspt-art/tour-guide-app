import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="نظام تصفية المرشدين", page_icon="🧭", layout="wide")

st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #f4f9f4;
        border-left: 2px solid #e0e0e0;
    }
    [data-testid="stSidebar"] h1 {
        color: #1b5e20;
        font-weight: 800;
        font-size: 1.6rem;
        margin-bottom: 15px;
    }
    [data-testid="stSidebar"] .stRadio > label {
        display: none !important;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {
        background-color: #ffffff !important;
        padding: 14px 18px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.04) !important;
        border: 1px solid #c8e6c9 !important;
        margin-bottom: 12px !important;
        transition: all 0.3s ease-in-out !important;
        display: flex !important;
        align-items: center !important;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 20px rgba(27, 94, 32, 0.15) !important;
        border-color: #2e7d32 !important;
        background-color: #f1f8f1 !important;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label p {
        font-weight: 700 !important;
        color: #1b5e20 !important;
        font-size: 1.05rem !important;
        margin: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

try:
    guides_df = pd.read_excel("guides.xlsx")
except:
    guides_df = pd.DataFrame({"Guide Name": ["أحمد", "محمود"], "Account Number": ["1805000493514500022", "1805000493514500033"]})

acc_column = guides_df.columns[1] if len(guides_df.columns) > 1 else guides_df.columns[0]

# ملف حفظ الطلبات بشكل دائم
SUBMISSIONS_FILE = "submissions.xlsx"

def load_submissions():
    if os.path.exists(SUBMISSIONS_FILE):
        try:
            return pd.read_excel(SUBMISSIONS_FILE)
        except:
            return pd.DataFrame()
    return pd.DataFrame()

def save_submission(new_data):
    df = load_submissions()
    new_df = pd.DataFrame([new_data])
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_excel(SUBMISSIONS_FILE, index=False)

st.sidebar.title("🧭 القائمة الرئيسية")
st.sidebar.markdown("<p style='font-weight: 800; color: #1b5e20; font-size: 1.15rem; margin-bottom: 10px;'>اختر الصفحة</p>", unsafe_allow_html=True)
page = st.sidebar.radio("اختر الصفحة", ["نموذج تصفية المرشد", "لوحة تحكم المدير"], label_visibility="collapsed")

if page == "نموذج تصفية المرشد":
    st.title("🧭 نظام تصفية المرشدين")
    st.markdown("---")
    
    with st.form("guide_form", clear_on_submit=True):
        account_no = st.selectbox("رقم الحساب الخاص بالمرشد", options=guides_df[acc_column].astype(str).tolist())
        file_no = st.text_input("رقم الفايل (File Number) *إلزامي*")
        
        st.markdown("---")
        st.subheader("الحقول المالية والبنود")
        
        advances = st.number_input("العهد (Advances)", min_value=0.0, step=10.0)
        collection = st.number_input("التحصيل (Collection)", min_value=0.0, step=10.0)
        option_item = st.number_input("الأوبشن (Option)", min_value=0.0, step=10.0)
        
        tip = st.number_input("إكرامية (Tip)", min_value=0.0, step=10.0)
        tickets = st.number_input("تذاكر (Tickets)", min_value=0.0, step=10.0)
        park = st.number_input("بارك (Park)", min_value=0.0, step=10.0)
        
        lunch = st.number_input("غداء (Lunch)", min_value=0.0, step=10.0)
        lunch_image = st.file_uploader("رفع صورة فاتورة الغداء", type=["png", "jpg", "jpeg"], key="lunch_img")
        
        st.markdown("---")
        shop_bills_amount = st.number_input("فواتير المحلات", min_value=0.0, step=10.0)
        shop_images = st.file_uploader("رفع صور فواتير المحلات", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="shop_imgs")
        
        submitted = st.form_submit_button("إرسال الطلب للمدير", type="primary")
        
        if submitted:
            if not file_no.strip():
                st.error("⚠️ عذراً، لا يمكن إرسال الطلب. يرجى إدخال (رقم الفايل) أولاً بشكل إلزامي!")
            else:
                new_entry = {
                    "Account": account_no,
                    "File No": file_no,
                    "Advances": advances,
                    "Collection": collection,
                    "Option": option_item,
                    "Tip": tip,
                    "Tickets": tickets,
                    "Park": park,
                    "Lunch": lunch,
                    "Lunch Receipt": lunch_image.name if lunch_image else "لا توجد صورة",
                    "Shop Bills": shop_bills_amount,
                    "Shop Images Count": len(shop_images) if shop_images else 0
                }
                save_submission(new_entry)
                st.success("تم إرسال الطلب للمدير بنجاح، وتفريغ الحقول لطلب جديد!")

elif page == "لوحة تحكم المدير":
    st.title("📊 لوحة تحكم المدير")
    st.markdown("---")
    
    password = st.text_input("أدخل كلمة المرور", type="password")
    
    if password == "159753":
        st.success("تم تسجيل الدخول بنجاح!")
        sub_df = load_submissions()
        if not sub_df.empty:
            st.markdown("### الطلبات الواردة")
            st.data_editor(sub_df, use_container_width=True)
        else:
            st.info("لا توجد طلبات جديدة حتى الآن.")
        
        st.markdown("### قاعدة بيانات المرشدين")
        st.dataframe(guides_df, use_container_width=True)
    elif password:
        st.error("كلمة المرور غير صحيحة.")
    else:
        st.info("الرجاء إدخال كلمة المرور لعرض لوحة التحكم.")
