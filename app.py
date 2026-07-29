import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime

st.set_page_config(page_title="نظام تصفية المرشدين", page_icon="🧭", layout="wide")

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

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

name_column = guides_df.columns[0] if len(guides_df.columns) > 0 else "Guide Name"
acc_column = guides_df.columns[1] if len(guides_df.columns) > 1 else guides_df.columns[0]

SUBMISSIONS_FILE = "submissions.xlsx"

def load_submissions():
    if os.path.exists(SUBMISSIONS_FILE):
        try:
            df = pd.read_excel(SUBMISSIONS_FILE)
            # التأكد من وجود الأعمدة الأساسية لمنع أي خطأ KeyError
            if "Guide Name" not in df.columns:
                df["Guide Name"] = "غير معروف"
            if "Timestamp" not in df.columns:
                df["Timestamp"] = "غير محدد"
            return df
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
        account_options = [None] + guides_df[acc_column].astype(str).tolist()
        account_no = st.selectbox("رقم الحساب الخاص بالمرشد", options=account_options, index=0)
        
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
            if not account_no:
                st.error("⚠️ عذراً، يجب اختيار (رقم الحساب) الخاص بك أولاً!")
            elif not file_no.strip():
                st.error("⚠️ عذراً، لا يمكن إرسال الطلب. يرجى إدخال (رقم الفايل) أولاً بشكل إلزامي!")
            else:
                matched_guide = guides_df[guides_df[acc_column].astype(str) == str(account_no)]
                guide_name = matched_guide[name_column].values[0] if not matched_guide.empty else "غير معروف"
                
                current_time_str = datetime.now().strftime("%Y-%m-%d %I:%M %p")
                
                lunch_path = ""
                if lunch_image is not None:
                    lunch_path = os.path.join(UPLOAD_DIR, f"{time.time()}_{lunch_image.name}")
                    with open(lunch_path, "wb") as f:
                        f.write(lunch_image.getbuffer())
                
                shop_paths = []
                if shop_images:
                    for img in shop_images:
                        s_path = os.path.join(UPLOAD_DIR, f"{time.time()}_{img.name}")
                        with open(s_path, "wb") as f:
                            f.write(img.getbuffer())
                        shop_paths.append(s_path)
                
                new_entry = {
                    "Timestamp": current_time_str,
                    "Guide Name": guide_name,
                    "Account": account_no,
                    "File No": file_no,
                    "Advances": advances,
                    "Collection": collection,
                    "Option": option_item,
                    "Tip": tip,
                    "Tickets": tickets,
                    "Park": park,
                    "Lunch": lunch,
                    "Lunch Receipt": lunch_path,
                    "Shop Bills": shop_bills_amount,
                    "Shop Images": ",".join(shop_paths) if shop_paths else ""
                }
                save_submission(new_entry)
                
                st.success("✅ تم إرسال الطلب للمدير بنجاح! جاهز لتسجيل تصفية جديدة...")
                time.sleep(5)
                st.rerun()

elif page == "لوحة تحكم المدير":
    st.title("📊 لوحة تحكم المدير")
    st.markdown("---")
    
    password = st.text_input("أدخل كلمة المرور", type="password")
    
    if password == "159753":
        st.success("تم تسجيل الدخول بنجاح!")
        sub_df = load_submissions()
        if not sub_df.empty:
            st.markdown("### 🔍 فلترة وعرض تصفيات المرشدين")
            
            all_guides_in_subs = sub_df["Guide Name"].dropna().unique().tolist()
            selected_guide_filter = st.selectbox("اختر اسم المرشد لعرض جميع تصفياته وسجلاته", options=["الكل (جميع المرشدين)"] + all_guides_in_subs)
            
            if selected_guide_filter != "الكل (جميع المرشدين)":
                filtered_sub_df = sub_df[sub_df["Guide Name"] == selected_guide_filter]
                st.info(f"عرض التصفيات الخاصة بالمرشد: **{selected_guide_filter}** (عدد الطلبات: {len(filtered_sub_df)})")
            else:
                filtered_sub_df = sub_df
            
            st.markdown("### الطلبات الواردة")
            cols_to_show = [c for c in filtered_sub_df.columns if c not in ["Lunch Receipt", "Shop Images"]]
            st.dataframe(filtered_sub_df[cols_to_show], use_container_width=True)
            
            st.markdown("---")
            st.markdown("### 🔍 مراجعة فواتير وصور الطلبات")
            
            file_options = filtered_sub_df["File No"].astype(str).tolist() if not filtered_sub_df.empty else []
            if file_options:
                selected_file = st.selectbox("اختر رقم الفايل لعرض الفواتير والصور الخاصة به", options=file_options)
                
                if selected_file:
                    req_row = filtered_sub_df[filtered_sub_df["File No"].astype(str) == selected_file].iloc[0]
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### 🥗 صورة فاتورة الغداء")
                        l_path = req_row.get("Lunch Receipt", "")
                        if pd.notna(l_path) and str(l_path).strip() != "" and os.path.exists(str(l_path)):
                            st.image(str(l_path), caption=f"فاتورة غداء - فايل: {selected_file}", use_container_width=True)
                        else:
                            st.info("لا توجد صورة لفاتورة الغداء لهذا الطلب.")
                    
                    with col2:
                        st.markdown("#### 🛍️ صور فواتير المحلات")
                        s_paths = req_row.get("Shop Images", "")
                        if pd.notna(s_paths) and str(s_paths).strip() != "":
                            paths_list = str(s_paths).split(",")
                            for idx, p in enumerate(paths_list):
                                if os.path.exists(p):
                                    st.image(p, caption=f"صورة محلات رقم {idx+1} - فايل: {selected_file}", use_container_width=True)
                        else:
                            st.info("لا توجد صور لفواتير المحلات لهذا الطلب.")
            else:
                st.warning("لا توجد فايلات متاحة للفلترة الحالية.")
        else:
            st.info("لا توجد طلبات جديدة حتى الآن.")
        
        st.markdown("---")
        st.markdown("### قاعدة بيانات المرشدين")
        st.dataframe(guides_df, use_container_width=True)
    elif password:
        st.error("كلمة المرور غير صحيحة.")
    else:
        st.info("الرجاء إدخال كلمة المرور لعرض لوحة التحكم.")
