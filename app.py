import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="تصفية مرشدين السياحة", page_icon="🧭", layout="wide")

# Custom CSS for professional styling (Green Sidebar & Clean Cards)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    [data-testid="stSidebar"] {
        background-color: #113f36;
        color: white;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    .stButton>button {
        background-color: #113f36;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #1b5e52;
    }
    </style>
""", unsafe_allow_html=True)

# Load guide data from Excel mapping
@st.cache_data
def load_guides():
    df = pd.read_excel('guides.xlsx', sheet_name=0)   
    return df
guides_df = load_guides()

# Sidebar Navigation
st.sidebar.markdown("## 🧭 نظام تصفية المرشدين")
st.sidebar.markdown("---")
menu = st.sidebar.radio("القائمة الرئيسية", ["نموذج تصفية المرشد", "لوحة تحكم المدير (الإشعارات والطلبات)"])

if menu == "نموذج تصفية المرشد":
    st.markdown("## 📋 نموذج تصفية رحلة مرشد سياحي")
    st.markdown("يرجى ملء الحقول المالية بدقة ورفع الفواتير المطلوبة.")
    
    with st.form("liquidation_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Account number dropdown (Hidden guide names for privacy)
            account_list = guides_df['رقم الحساب'].astype(str).tolist()
            selected_account = st.selectbox("رقم الحساب الخاص بالمرشد", options=account_list)
            
            # File Number
            file_number = st.text_input("رقم الفايل (File Number)")
            
            # Numeric strict columns
            st.markdown("### الحقول المالية (أرقام فقط)")
            ticket = st.number_input("تذاكر (Tickets)", min_value=0.0, step=1.0, format="%.2f")
            park = st.number_input("بارك (Park)", min_value=0.0, step=1.0, format="%.2f")
            lunch = st.number_input("غداء (Lunch)", min_value=0.0, step=1.0, format="%.2f")
            
        with col2:
            tip = st.number_input("إكرامية (Tip)", min_value=0.0, step=1.0, format="%.2f")
            guide_daily_rate = st.number_input("يومية الإرشاد (Guide Daily Rate)", min_value=0.0, step=1.0, format="%.2f")
            advances = st.number_input("عهد (Advances)", min_value=0.0, step=1.0, format="%.2f")
            
            # Flexible columns (Text and numbers)
            st.markdown("### البيانات النصية والإضافية")
            option = st.text_input("أوبشن (Option)")
            collection = st.text_input("تحصيل (Collection)")
            
        st.markdown("---")
        st.markdown("### 📎 مرفقات الفواتير")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            shops_file = st.file_uploader("فواتير المحلات (Shops)", type=["pdf", "png", "jpg", "jpeg"])
        with col_f2:
            restaurants_file = st.file_uploader("فواتير المطاعم (Restaurants)", type=["pdf", "png", "jpg", "jpeg"])
            
        submit_btn = st.form_submit_button("إرسال التصفية")
        
        if submit_btn:
            if not file_number:
                st.error("برجاء إدخال رقم الفايل!")
            else:
                # Map account number to guide name securely
                matched_row = guides_df[guides_df['رقم الحساب'].astype(str) == str(selected_account)]
                guide_name = matched_row['اسم المرشد '].values[0] if not matched_row.empty else "مرشد غير معروف"
                
                if 'submissions' not in st.session_state:
                    st.session_state['submissions'] = []
                
                submission_data = {
                    "وقت الإرسال": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "اسم المرشد (لإدارة)": guide_name,
                    "رقم الحساب": selected_account,
                    "رقم الفايل": file_number,
                    "تذاكر": ticket,
                    "بارك": park,
                    "غداء": lunch,
                    "إكرامية": tip,
                    "يومية الإرشاد": guide_daily_rate,
                    "عهد": advances,
                    "أوبشن": option,
                    "تحصيل": collection,
                    "الحالة": "جديد 🔔"
                }
                st.session_state['submissions'].append(submission_data)
st.success("Done successfully!")
st.rerun()
if menu == "Admin Dashboard":
    st.title("Admin Login 🔒")
    password = st.text_input("Enter Admin Password", type="password", key="admin_pass")

if password == "159753":
        st.success("Login Successful!")
        st.markdown("---")
        st.title("📊 Admin Dashboard & Notifications")
        
if password == "159753":
        st.success("Login Successful!")
        st.markdown("---")
        st.title("📊 Admin Dashboard & Notifications")
        
if "submissions" in st.session_state and len(st.session_state["submissions"]) > 0:
        sub_df = pd.DataFrame(st.session_state["submissions"])
        edited_sub_df = st.data_editor(
            sub_df,
            num_rows="dynamic",
            key="manager_submissions_editor",
            use_container_width=True,
        )
        
        if st.button("Save Changes and Delete Selected Records"):
            st.session_state["submissions"] = edited_sub_df.to_dict("records")
            st.success("Records updated successfully!")
            st.rerun()
else:
        st.info("No new pending clearance requests at the moment.")
st.markdown("---")
st.markdown("### 📁 Guides Database & Associated Account Numbers")
      st.dataframe(guides_df, use_container_width=True)

  elif password:
    st.error("كلمة السر غير صحيحة، يرجى المحاولة مرة أخرى.")
  else:
    st.info("الرجاء إدخال كلمة السر لعرض لوحة التحكم وإدارة الطلبات.")
