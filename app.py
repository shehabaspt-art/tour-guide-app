import streamlit as st
import pandas as pd
import os
import time
import base64
from datetime import datetime

st.set_page_config(page_title="Sun Pyramids Tours", page_icon="🧭", layout="wide")

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

SUBMISSIONS_FILE = "submissions.xlsx"
ARCHIVE_FILE = "archive.xlsx"
SAVED_LOGO_PATH = os.path.join(UPLOAD_DIR, "custom_saved_logo.png")

def load_data(file_path):
    if os.path.exists(file_path):
        try:
            df = pd.read_excel(file_path)
            if "Guide Name" not in df.columns:
                df["Guide Name"] = "غير معروف"
            if "Timestamp" not in df.columns:
                df["Timestamp"] = "غير محدد"
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

# حساب عدد الطلبات المعلقة للإشعارات
sub_df_initial = load_data(SUBMISSIONS_FILE)
pending_count = len(sub_df_initial)

# التحقق من وجود لوجو محفوظ مسبقاً، وإلا استخدام اللوجو المتاح في المجلد أو الافتراضي
active_logo_to_show = None
if os.path.exists(SAVED_LOGO_PATH):
    active_logo_to_show = SAVED_LOGO_PATH
else:
    for f in os.listdir("."):
        if f.startswith("image_") and f.endswith(('.png', '.jpg', '.jpeg', '.webp')):
            active_logo_to_show = f
            break

logo_html = ""
if active_logo_to_show and os.path.exists(active_logo_to_show):
    with open(active_logo_to_show, "rb") as img_file:
        encoded_img = base64.b64encode(img_file.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{encoded_img}" style="height: 48px; object-fit: contain;" />'
else:
    logo_html = '<span style="color: #1b5e20; font-weight: bold; font-size: 1.1rem;">Sun Pyramids Tours</span>'

# تصميم الشريط العلوي الثابت
st.markdown(f"""
    <style>
    header {{visibility: hidden;}}
    .stApp {{
        margin-top: 65px;
    }}
    .custom-topbar {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 60px;
        background-color: #ffffff;
        border-bottom: 1px solid #e0e0e0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 25px;
        z-index: 99999;
        box-shadow: 0 1px 4px rgba(0,0,0,0.03);
    }}
    .topbar-left-group {{
        display: flex;
        align-items: center;
        gap: 15px;
    }}
    .sidebar-arrow-icon {{
        font-size: 1.3rem;
        color: #888888;
        font-weight: bold;
        cursor: pointer;
    }}
    .topbar-right-group {{
        display: flex;
        align-items: center;
        gap: 22px;
    }}
    .notification-container {{
        position: relative;
        display: inline-flex;
        align-items: center;
        cursor: pointer;
    }}
    .notification-badge {{
        position: absolute;
        top: -8px;
        right: -15px;
        background-color: #e8f5e9;
        color: #2e7d32;
        border: 1px solid #a5d6a7;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 1px 6px;
        border-radius: 12px;
    }}
    .user-profile-badge {{
        width: 36px;
        height: 36px;
        background-color: #111111;
        color: #ffffff;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 0.9rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    [data-testid="stSidebar"] {{
        background-color: #f4f9f4;
        border-left: 2px solid #e0e0e0;
        padding-top: 1rem;
        margin-top: 60px;
        border-radius: 8px;
    }}
    [data-testid="stSidebar"] .stRadio > label {{
        display: none !important;
    }}
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {{
        background-color: #ffffff !important;
        padding: 14px 18px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.04) !important;
        border: 1px solid #c8e6c9 !important;
        margin-bottom: 12px !important;
        transition: all 0.3s ease-in-out !important;
        display: flex !important;
        align-items: center !important;
    }}
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {{
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 20px rgba(27, 94, 32, 0.15) !important;
        border-color: #2e7d32 !important;
        background-color: #f1f8f1 !important;
    }}
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label p {{
        font-weight: 700 !important;
        color: #1b5e20 !important;
        font-size: 1.05rem !important;
        margin: 0 !important;
    }}
    </style>

    <div class="custom-topbar">
        <div class="topbar-left-group">
            {logo_html}
            <span class="sidebar-arrow-icon" title="القائمة الجانبية">‹</span>
        </div>
        <div class="topbar-right-group">
            <div class="notification-container" title="عدد التصفيات والطلبات المعلقة">
                <span style="font-size: 1.3rem;">🔔</span>
                <span class="notification-badge">{pending_count}</span>
            </div>
            <div class="user-profile-badge" title="حساب المدير">
                SA
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

try:
    guides_df = pd.read_excel("guides.xlsx")
except:
    guides_df = pd.DataFrame({"Guide Name": ["أحمد", "محمود"], "Account Number": ["1805000493514500022", "1805000493514500033"]})

name_column = guides_df.columns[0] if len(guides_df.columns) > 0 else "Guide Name"
acc_column = guides_df.columns[1] if len(guides_df.columns) > 1 else guides_df.columns[0]

SHOPS_LIST = [
    "وجية بردى", "اخناتون سجاد", "مينا للبرديات", "رويال سجاد", 
    "اولد كايرو", "رويال للعطور", "خان الحلو للقطن", "فلور قطن", 
    "طيبة للقطن", "فيلة بازار", "جولدن بيرد", "مملوك", 
    "ريحانة توابل", "كنور توابل", "سقاره سجاد", "قصر العطور", "لازوريت"
]

st.sidebar.title("🧭 القائمة الرئيسية")
st.sidebar.markdown("<p style='font-weight: 800; color: #1b5e20; font-size: 1.15rem; margin-bottom: 10px;'>اختر الصفحة</p>", unsafe_allow_html=True)
page = st.sidebar.radio("اختر الصفحة", ["نموذج تصفية المرشد", "لوحة تحكم المدير", "التصفيات (الأرشيف)", "إدارة اللوجو 🖼️"], label_visibility="collapsed")

if page == "إدارة اللوجو 🖼️":
    st.title("🖼️ لوحة التحكم في شعار الموقع (Logo)")
    st.markdown("---")
    
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        st.subheader("الشعار الحالي المعروض:")
        if os.path.exists(SAVED_LOGO_PATH):
            st.image(SAVED_LOGO_PATH, width=250, caption="الشعار المستخدم حالياً")
            if st.button("🗑️ حذف الشعار الحالي العودة للافتراضي", type="secondary"):
                os.remove(SAVED_LOGO_PATH)
                st.success("تم حذف الشعار بنجاح!")
                time.sleep(1)
                st.rerun()
        else:
            st.info("لا يوجد شعار مخصص محفوظ حالياً، يتم استخدام الشعار الافتراضي.")

    with col_l2:
        st.subheader("رفع وتحديث الشعار:")
        uploaded_new_logo = st.file_uploader("اختر صورة الشعار الجديدة (PNG / JPG)", type=["png", "jpg", "jpeg"])
        
        if uploaded_new_logo is not None:
            st.image(uploaded_new_logo, width=200, caption="معاينة الشعار الجديد")
            if st.button("💾 Save (حفظ الشعار)", type="primary"):
                with open(SAVED_LOGO_PATH, "wb") as f:
                    f.write(uploaded_new_logo.getbuffer())
                st.success("✅ تم حفظ الشعار الجديد بنجاح وتحديثه في الموقع!")
                time.sleep(1.5)
                st.rerun()

elif page == "نموذج تصفية المرشد":
    st.title("🧭 نظام تصفية المرشدين")
    st.markdown("---")
    
    with st.form("guide_form", clear_on_submit=True):
        account_options = [None] + guides_df[acc_column].astype(str).tolist()
        account_no = st.selectbox("رقم الحساب الخاص بالمرشد", options=account_options, index=0)
        
        file_no = st.text_input("رقم الفايل (File Number) *إلزامي*")
        
        st.markdown("---")
        st.subheader("الحقول المالية والبنود")
        
        advances = st.number_input("العهد (Advances)", min_value=0.0, step=10.0)
        
        col_c1, col_c2 = st.columns([2, 1])
        with col_c1:
            collection_val = st.number_input("التحصيل (Collection)", min_value=0.0, step=10.0)
        with col_c2:
            collection_curr = st.selectbox("عملة التحصيل", options=["جنية", "يورو", "دولار"])
        
        st.markdown("---")
        st.subheader("الأوبشن (Option)")
        col_opt1, col_opt2, col_opt3, col_opt4 = st.columns(4)
        with col_opt1:
            option_type = st.text_input("نوع الاوبشن")
        with col_opt2:
            option_value = st.number_input("قيمة الاوبشن", min_value=0.0, step=10.0, key="opt_val")
        with col_opt3:
            option_curr = st.selectbox("عملة الاوبشن", options=["مصري", "دولار", "يورو"], key="opt_curr")
        with col_opt4:
            option_pay = st.selectbox("طريقة الدفع", options=["كاش", "لينك"])
        
        st.markdown("---")
        
        st.subheader("التذاكر (Tickets)")
        col_tkt1, col_tkt2 = st.columns(2)
        with col_tkt1:
            ticket_value = st.number_input("قيمة التذاكر", min_value=0.0, step=10.0, key="tkt_val")
        with col_tkt2:
            ticket_type = st.text_input("نوع التذاكر")
            
        st.markdown("---")
        tip = st.number_input("إكرامية (Tip)", min_value=0.0, step=10.0)
        park = st.number_input("بارك (Park)", min_value=0.0, step=10.0)
        
        lunch = st.number_input("غداء (Lunch)", min_value=0.0, step=10.0)
        lunch_image = st.file_uploader("رفع صورة فاتورة الغداء", type=["png", "jpg", "jpeg"], key="lunch_img")
        
        st.markdown("---")
        st.subheader("فواتير ومحلات التسوق")
        selected_shops = st.multiselect("اسم المحل (اختر من القائمة)", options=SHOPS_LIST)
        other_shops = st.text_input("محلات أخري (اكتبها يدوياً إن وجدت)")
        shop_images = st.file_uploader("رفع صور فواتير المحلات", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="shop_imgs")
        
        submitted = st.form_submit_button("إرسال الطلب للمدير", type="primary")
        
        if submitted:
            if not account_no:
                st.error("⚠️ عذراً، يجب اختيار (رقم الحساب) الخاص بك أولاً!")
            elif not file_no.strip():
                st.error("⚠️ عذراً، لا يمكن إرسال الطلب. يرجى إدخال (رقم الفايل) أولاً بشكل إلزامي!")
            elif shop_images and not selected_shops and not other_shops.strip():
                st.error("⚠️ عذراً، نظراً لرفع صور فواتير المحلات، يجب اختيار (اسم المحل) من القائمة أو كتابته في (محلات أخري) بشكل إلزامي!")
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
                    "Collection": f"{collection_val} {collection_curr}",
                    "Option Type": option_type,
                    "Option": f"{option_value} {option_curr} ({option_pay})",
                    "Tickets": f"{ticket_value} - {ticket_type}",
                    "Tip": tip,
                    "Park": park,
                    "Lunch": lunch,
                    "Lunch Receipt": lunch_path,
                    "Shop Names": ", ".join(selected_shops),
                    "Other Shops": other_shops,
                    "Shop Images": ",".join(shop_paths) if shop_paths else ""
                }
                save_to_file(SUBMISSIONS_FILE, new_entry)
                
                st.success("✅ تم إرسال الطلب للمدير بنجاح! جاهز لتسجيل تصفية جديدة...")
                time.sleep(5)
                st.rerun()

elif page == "لوحة تحكم المدير":
    st.title("📊 لوحة تحكم المدير")
    st.markdown("---")
    
    password = st.text_input("أدخل كلمة المرور", type="password", key="mgr_pass")
    
    if password == "159753":
        st.success("تم تسجيل الدخول بنجاح!")
        sub_df = load_data(SUBMISSIONS_FILE)
        
        if "viewing_file" not in st.session_state:
            st.session_state.viewing_file = None

        if st.session_state.viewing_file is not None:
            req_idx = st.session_state.viewing_file
            if req_idx in sub_df.index:
                req_row = sub_df.loc[req_idx]
                
                if st.button("⬅️ رجوع إلى لوحة التحكم"):
                    st.session_state.viewing_file = None
                    st.rerun()
                
                st.markdown(f"### 📄 تفاصيل تصفية الفايل: {req_row.get('File No', '')} (المرشد: {req_row.get('Guide Name', '')})")
                st.markdown(f"**التاريخ والوقت:** {req_row.get('Timestamp', '')} | **رقم الحساب:** {req_row.get('Account', '')}")
                st.markdown("---")
                
                st.write(f"**العهد (Advances):** {req_row.get('Advances', 0)}")
                st.write(f"**التحصيل (Collection):** {req_row.get('Collection', 0)}")
                st.write(f"**الأوبشن (Option):** {req_row.get('Option', '')} | **النوع:** {req_row.get('Option Type', '')}")
                st.write(f"**تذاكر (Tickets):** {req_row.get('Tickets', '')}")
                st.write(f"**إكرامية (Tip):** {req_row.get('Tip', 0)}")
                st.write(f"**بارك (Park):** {req_row.get('Park', 0)}")
                st.write(f"**غداء (Lunch):** {req_row.get('Lunch', 0)}")
                
                l_path = req_row.get("Lunch Receipt", "")
                if pd.notna(l_path) and str(l_path).strip() != "" and os.path.exists(str(l_path)):
                    st.image(str(l_path), caption="صورة فاتورة الغداء", width=300)
                else:
                    st.info("لا توجد صورة لفاتورة الغداء.")
                
                st.markdown("---")
                st.write(f"**أسماء المحلات المختارة:** {req_row.get('Shop Names', 'لا يوجد')}")
                st.write(f"**محلات أخري:** {req_row.get('Other Shops', 'لا يوجد')}")
                
                s_paths = req_row.get("Shop Images", "")
                if pd.notna(s_paths) and str(s_paths).strip() != "":
                    paths_list = str(s_paths).split(",")
                    for idx, p in enumerate(paths_list):
                        if os.path.exists(p):
                            st.image(p, caption=f"صورة محلات رقم {idx+1}", width=300)
                else:
                    st.info("لا توجد صور لفواتير المحلات.")
                
                st.markdown("---")
                st.markdown("### اتخاذ القرار بشأن الطلب:")
                col_btn1, col_btn2 = st.columns(2)
                
                with col_btn1:
                    if st.button("✅ تم", type="primary", use_container_width=True):
                        archive_entry = req_row.to_dict()
                        save_to_file(ARCHIVE_FILE, archive_entry)
                        
                        sub_df = sub_df.drop(req_idx).reset_index(drop=True)
                        overwrite_data(SUBMISSIONS_FILE, sub_df)
                        
                        st.session_state.viewing_file = None
                        st.success("تم نقل الطلب إلى صفحة التصفيات (الأرشيف) بنجاح!")
                        time.sleep(1)
                        st.rerun()
                
                with col_btn2:
                    if st.button("🔄 متابعة", use_container_width=True):
                        st.session_state.viewing_file = None
                        st.info("تم إبقاء الطلب في لوحة التحكم لمتابعة الإجراءات.")
                        time.sleep(1)
                        st.rerun()
            else:
                st.session_state.viewing_file = None
                st.rerun()
        
        else:
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
                
                for idx, row in filtered_sub_df.iterrows():
                    cols = st.columns([1, 2, 2, 2, 1.5])
                    with cols[0]:
                        st.write(f"**#{idx+1}**")
                    with cols[1]:
                        st.write(f"الفايل: {row.get('File No', '')}")
                    with cols[2]:
                        st.write(f"المرشد: {row.get('Guide Name', '')}")
                    with cols[3]:
                        st.write(f"الوقت: {row.get('Timestamp', '')}")
                    with cols[4]:
                        if st.button("عرض", key=f"view_btn_{idx}", type="primary"):
                            st.session_state.viewing_file = idx
                            st.rerun()
                    st.markdown("---")
            else:
                st.info("لا توجد طلبات جديدة حتى الآن.")
            
            st.markdown("---")
            st.markdown("### قاعدة بيانات المرشدين")
            st.dataframe(guides_df, use_container_width=`True`)
            
    elif password:
        st.error("كلمة المرور غير صحيحة.")
    else:
        st.info("الرجاء إدخال كلمة المرور لعرض لوحة التحكم.")

elif page == "التصفيات (الأرشيف)":
    st.title("📁 أرشيف التصفيات المنتهية (تم)")
    st.markdown("---")
    
    password_archive = st.text_input("أدخل كلمة المرور لعرض الأرشيف", type="password", key="arch_pass")
    
    if password_archive == "159753":
        st.success("تم تسجيل الدخول بنجاح!")
        archive_df = load_data(ARCHIVE_FILE)
        if not archive_df.empty:
            cols_to_show = [c for c in archive_df.columns if c not in ["Lunch Receipt", "Shop Images"]]
            st.dataframe(archive_df[cols_to_show], use_container_width=True)
        else:
            st.info("لا توجد تصفيات مؤرشفة حتى الآن.")

        st.markdown("---")
        st.markdown("### قاعدة بيانات المرشدين")
        st.dataframe(guides_df, use_container_width=True)
    elif password_archive:
        st.error("كلمة المرور غير صحيحة.")
    else:
        st.info("الرجاء إدخال كلمة المرور لعرض صفحة التصفيات (الأرشيف).")
