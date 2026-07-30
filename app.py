import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime

st.set_page_config(page_title="Sun Pyramids Tours", page_icon="🧭", layout="wide")

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

SUBMISSIONS_FILE = "submissions.xlsx"
ARCHIVE_FILE = "archive.xlsx"
GUIDES_FILE = "guides.xlsx"
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

if os.path.exists(SUBMISSIONS_FILE):
    try:
        init_sub_df = pd.read_excel(SUBMISSIONS_FILE)
        if not init_sub_df.empty and "File No" in init_sub_df.columns:
            init_sub_df = init_sub_df[~init_sub_df["File No"].astype(str).isin(["51515", "99999"])].reset_index(drop=True)
            init_sub_df.to_excel(SUBMISSIONS_FILE, index=False)
    except:
        pass

if "last_pending_count" not in st.session_state:
    sub_df_init = load_data(SUBMISSIONS_FILE)
    st.session_state.last_pending_count = len(sub_df_init)

sub_df_initial = load_data(SUBMISSIONS_FILE)
pending_count = len(sub_df_initial)

new_order_arrived = False
if pending_count > st.session_state.last_pending_count:
    new_order_arrived = True
    st.session_state.last_pending_count = pending_count
elif pending_count < st.session_state.last_pending_count:
    st.session_state.last_pending_count = pending_count

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

alert_script = ""
if new_order_arrived:
    alert_script = """
    <script>
        document.title = "🚨 (طلب جديد!) Sun Pyramids Tours";
        var audio = new Audio('https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3');
        audio.play().catch(e => console.log("Audio play blocked"));
    </script>
    """

st.markdown(f"""
    <style>
    .stApp {{
        margin-top: 70px !important;
    }}
    .block-container {{
        padding-top: 2rem !important;
    }}
    .custom-topbar {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 65px;
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
    
    button[kind="secondary"], div.stButton > button {{
        border-radius: 8px;
    }}
    
    /* فرض خط ثقيل جداً (Bold/Heavy) على الجدول */
    [data-testid="stDataFrame"] table {{
        font-weight: 900 !important;
    }}
    [data-testid="stDataFrame"] th {{
        font-weight: 900 !important;
        font-size: 1.15rem !important;
        color: #0b3d0f !important;
    }}
    [data-testid="stDataFrame"] td {{
        font-weight: 900 !important;
        font-size: 1.1rem !important;
        color: #000000 !important;
    }}
    [data-testid="stDataFrame"] div, [data-testid="stDataFrame"] span, [data-testid="stDataFrame"] p {{
        font-weight: 900 !important;
    }}
    
    [data-testid="stSidebar"] {{
        background-color: #d8ebd8;
        border-left: 2px solid #c2e0c2;
        margin-top: 0px !important;
        padding-top: 0px !important;
        border-radius: 0px 8px 8px 0px;
    }}
    [data-testid="stSidebar"] > div:first-child {{
        padding-top: 10px !important;
    }}
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
        gap: 0rem !important;
        padding-top: 0rem !important;
    }}
    [data-testid="stSidebar"] .stRadio > label {{
        display: none !important;
    }}
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {{
        background-color: #ffffff !important;
        padding: 14px 18px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.04) !important;
        border: 1px solid #a3d9a3 !important;
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
    {alert_script}
""", unsafe_allow_html=True)

try:
    guides_df = pd.read_excel(GUIDES_FILE)
except:
    guides_df = pd.DataFrame({"Guide Name": ["أحمد", "محمود"], "Account Number": ["1805000493514500022", "1805000493514500033"]})
    guides_df.to_excel(GUIDES_FILE, index=False)

name_column = guides_df.columns[0] if len(guides_df.columns) > 0 else "Guide Name"
acc_column = guides_df.columns[1] if len(guides_df.columns) > 1 else guides_df.columns[0]

SHOPS_LIST = [
    "وجية بردى", "اخناتون سجاد", "مينا للبرديات", "رويال سجاد", 
    "اولد كايرو", "رويال للعطور", "خان الحلو للقطن", "فلور قطن", 
    "طيبة للقطن", "فيلة بازار", "جولدن بيرد", "مملوك", 
    "ريحانة توابل", "كنور توابل", "قصر العطور", "لازوريت"
]

st.sidebar.markdown("<h2 style='color: #1b5e20; margin-bottom: 5px; font-size: 1.5rem;'>🧭 القائمة الرئيسية</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='font-weight: 800; color: #1b5e20; font-size: 1.15rem; margin-top: 15px; margin-bottom: 20px;'>اختر الصفحة</p>", unsafe_allow_html=True)
page = st.sidebar.radio("اختر الصفحة", ["نموذج تصفية المرشد", "إدارة التصفيات", "الأرشيف"], label_visibility="collapsed")

if page == "نموذج تصفية المرشد":
    st.title("🧭 نظام تصفية المرشدين")
    st.markdown("---")
    
    if "option_rows_count" not in st.session_state:
        st.session_state.option_rows_count = 1

    with st.form("guide_form", clear_on_submit=True):
        st.subheader("بيانات المرشد")
        col_top1, col_top2, col_top3 = st.columns(3)
        with col_top1:
            account_options = [None] + guides_df[acc_column].astype(str).tolist()
            account_no = st.selectbox("رقم الحساب الخاص بالمرشد", options=account_options, index=0)
        with col_top2:
            file_no = st.text_input("رقم الفايل (File Number) *إلزامي*")
        with col_top3:
            advances = st.number_input("العهد (Advances)", min_value=0.0, step=10.0)
        
        st.markdown("---")
        st.subheader("التحصيل (Collection)")
        
        col_c1, col_c2 = st.columns([2, 1])
        with col_c1:
            collection_val = st.number_input("قيمة التحصيل", min_value=0.0, step=10.0)
        with col_c2:
            collection_curr = st.selectbox("عملة التحصيل", options=["جنية", "يورو", "دولار"])
        
        st.markdown("---")
        st.subheader("الأوبشن (Option)")
        
        option_data_list = []
        for i in range(st.session_state.option_rows_count):
            st.markdown(f"**أوبشن رقم ({i+1})**")
            col_opt1, col_opt2, col_opt3, col_opt4, col_opt5 = st.columns(5)
            with col_opt1:
                opt_type = st.text_input("نوع الاوبشن", key=f"opt_type_{i}")
            with col_opt2:
                opt_val = st.number_input("قيمة الاوبشن", min_value=0.0, step=10.0, key=f"opt_val_{i}")
            with col_opt3:
                opt_curr = st.selectbox("عملة الاوبشن", options=["مصري", "دولار", "يورو"], key=f"opt_curr_{i}")
            with col_opt4:
                opt_pay = st.selectbox("طريقة الدفع", options=["كاش", "لينك"], key=f"opt_pay_{i}")
            with col_opt5:
                cash_h = ""
                if opt_pay == "كاش":
                    cash_h = st.selectbox("المبلغ", options=[None, "مع المرشد", "مع السواق"], key=f"cash_h_{i}")
                else:
                    st.markdown("")
            
            option_data_list.log = {"type": opt_type, "value": opt_val, "curr": opt_curr, "pay": opt_pay, "holder": cash_h}
            if i < st.session_state.option_rows_count - 1:
                st.markdown("---")

        add_more_option = st.form_submit_button("➕ إضافة أوبشن آخر")
        
        st.markdown("---")
        
        st.subheader("مصاريف (Expenses)")
        col_tkt1, col_tkt2 = st.columns(2)
        with col_tkt1:
            ticket_value = st.number_input("قيمة التذاكر", min_value=0.0, step=10.0, key="tkt_val")
        with col_tkt2:
            ticket_type = st.text_input("نوع التذاكر")
            
        st.markdown("---")
        
        col_misc1, col_misc2, col_misc3 = st.columns(3)
        with col_misc1:
            tip = st.number_input("إكرامية", min_value=0.0, step=10.0)
        with col_misc2:
            park = st.number_input("بارك", min_value=0.0, step=10.0)
        with col_misc3:
            lunch = st.number_input("غداء", min_value=0.0, step=10.0)
            
        lunch_image = st.file_uploader("رفع صورة فاتورة الغداء", type=["png", "jpg", "jpeg"], key="lunch_img")
        
        st.markdown("---")
        st.subheader("فواتير ومحلات التسوق")
        selected_shops = st.multiselect("اسم المحل (اختر من القائمة)", options=SHOPS_LIST)
        other_shops = st.text_input("محلات أخري (اكتبها يدوياً إن وجدت)")
        shop_images = st.file_uploader("رفع صور فواتير المحلات", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="shop_imgs")
        
        submitted = st.form_submit_button("إرسال الطلب للمدير", type="primary")
        
        if add_more_option:
            st.session_state.option_rows_count += 1
            st.rerun()

        if submitted:
            # التحقق من صحة بيانات الأوبشنز المضافة
            validation_error = False
            for i in range(st.session_state.option_rows_count):
                p_val = st.session_state.get(f"opt_pay_{i}", "كاش")
                c_h = st.session_state.get(f"cash_h_{i}", None)
                if p_val == "كاش" and not c_h:
                    validation_error = True
                    break

            if not account_no:
                st.error("⚠️ عذراً، يجب اختيار (رقم الحساب) الخاص بك أولاً!")
            elif not file_no.strip():
                st.error("⚠️ عذراً، لا يمكن إرسال الطلب. يرجى إدخال (رقم الفايل) أولاً بشكل إلزامي!")
            elif validation_error:
                st.error("⚠️ عذراً، نظراً لاختيار طريقة الدفع (كاش) في أحد الأوبشنز، يجب اختيار (المبلغ) [مع المرشد / مع السواق] بشكل إلزامي لكل أوبشن كاش!")
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
                
                options_summary_list = []
                option_types_list = []
                for i in range(st.session_state.option_rows_count):
                    o_type = st.session_state.get(f"opt_type_{i}", "")
                    o_val = st.session_state.get(f"opt_val_{i}", 0.0)
                    o_curr = st.session_state.get(f"opt_curr_{i}", "مصري")
                    o_pay = st.session_state.get(f"opt_pay_{i}", "كاش")
                    o_holder = st.session_state.get(f"cash_h_{i}", "")
                    
                    if o_type.strip() or o_val > 0:
                        option_types_list.append(o_type)
                        detail_str = f"{o_val} {o_curr} ({o_pay})"
                        if o_pay == "كاش" and o_holder:
                            detail_str += f" - [{o_holder}]"
                        if o_type:
                            detail_str = f"{o_type}: " + detail_str
                        options_summary_list.append(detail_str)

                new_entry = {
                    "Timestamp": current_time_str,
                    "Guide Name": guide_name,
                    "Account": account_no,
                    "File No": file_no,
                    "Advances": advances,
                    "Collection": f"{collection_val} {collection_curr}",
                    "Option Type": ", ".join(option_types_list),
                    "Option": " | ".join(options_summary_list),
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
                
                st.session_state.option_rows_count = 1 # إعادة تعيين العداد
                st.success("✅ تم إرسال الطلب للمدير بنجاح! جاهز لتسجيل تصفية جديدة...")
                st.markdown("""
                    <script>
                        setTimeout(function() {
                            window.location.reload();
                        }, 4000);
                    </script>
                """, unsafe_allow_html=True)

elif page == "إدارة التصفيات":
    st.title("📊 إدارة التصفيات")
    st.markdown("---")
    
    password = st.text_input("أدخل كلمة المرور", type="password", key="mgr_pass")
    
    if password == "159753":
        st.success("تم تسجيل الدخول بنجاح!")
        sub_df = load_data(SUBMISSIONS_FILE)
        
        if "viewing_file" not in st.session_state:
            st.session_state.viewing_file = None
        if "confirming_del_sub" not in st.session_state:
            st.session_state.confirming_del_sub = None
        if "confirming_edit_guide" not in st.session_state:
            st.session_state.confirming_edit_guide = None
        if "confirming_del_guide" not in st.session_state:
            st.session_state.confirming_del_guide = None
        if "confirming_add_guide" not in st.session_state:
            st.session_state.confirming_add_guide = None
        if "clear_add_inputs" not in st.session_state:
            st.session_state.clear_add_inputs = False
        if "clear_edit_input" not in st.session_state:
            st.session_state.clear_edit_input = False

        if st.session_state.viewing_file is not None:
            req_idx = st.session_state.viewing_file
            if req_idx in sub_df.index:
                req_row = sub_df.loc[req_idx]
                
                if st.button("⬅️ رجوع إلى إدارة التصفيات"):
                    st.session_state.viewing_file = None
                    st.rerun()
                
                st.markdown(f"### 📄 تفاصيل تصفية الفايل: {req_row.get('File No', '')} (المرشد: {req_row.get('Guide Name', '')})")
                st.markdown(f"**التاريخ والوقت:** {req_row.get('Timestamp', '')} | **رقم الحساب:** {req_row.get('Account', '')}")
                st.markdown("---")
                
                st.write(f"**العهد (Advances):** {req_row.get('Advances', 0)}")
                st.write(f"**التحصيل (Collection):** {req_row.get('Collection', 0)}")
                st.write(f"**الأوبشن (Option):** {req_row.get('Option', '')}")
                st.write(f"**التذاكر (Tickets):** {req_row.get('Tickets', '')}")
                st.write(f"**إكرامية (Tip):** {req_row.get('Tip', 0)}")
                st.write(f"**بارك (Park):** {req_row.get('Park', 0)}")
                st.write(f"**غداء (Lunch):** {req_row.get('Lunch', 0)}")
                
                l_path = req_row.get("Lunch Receipt", "")
                if pd.notna(l_path) and str(l_path).strip() != "" and os.path.exists(str(l_path)):
                    st.image(str(l_path), caption="صورة فاتورة الغداء", use_container_width=True)
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
                            st.image(p, caption=f"صورة محلات رقم {idx+1}", use_container_width=True)
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
                        st.rerun()
                
                with col_btn2:
                    if st.button("🔄 متابعة", use_container_width=True):
                        st.session_state.viewing_file = None
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
                    cols = st.columns([1, 2, 2, 2, 1.5, 1.5])
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
                    with cols[5]:
                        if st.button("🗑️ حذف", key=f"del_sub_btn_{idx}", type="primary"):
                            st.session_state.confirming_del_sub = idx
                            st.rerun()
                    
                    if st.session_state.confirming_del_sub == idx:
                        st.warning(f"⚠️ هل أنت متأكد من رغبتك في حذف طلب الفايل رقم ({row.get('File No', '')})؟")
                        c_col1, c_col2 = st.columns(2)
                        with c_col1:
                            if st.button("✔️ تأكيد الحذف النهائي", key=f"confirm_del_sub_{idx}", type="primary"):
                                sub_df = sub_df.drop(idx).reset_index(drop=True)
                                overwrite_data(SUBMISSIONS_FILE, sub_df)
                                st.session_state.confirming_del_sub = None
                                st.rerun()
                        with c_col2:
                            if st.button("❌ رجوع (إلغاء)", key=f"cancel_del_sub_{idx}", type="primary"):
                                st.session_state.confirming_del_sub = None
                                st.rerun()
                    
                    st.markdown("---")
            else:
                st.info("لا توجد طلبات جديدة حتى الآن.")
            
            st.markdown("---")
            st.markdown("### قاعدة بيانات المرشدين (إدارة وتعديل أرقام الحسابات)")
            st.dataframe(guides_df, use_container_width=True)
            
            col_section_left, col_section_right = st.columns(2, gap="large")
            
            with col_section_left:
                st.markdown("#### تعديل أو حذف رقم حساب مرشد:")
                guide_names_list = guides_df[name_column].astype(str).tolist()
                selected_guide_to_edit = st.selectbox("اختر اسم المرشد", options=guide_names_list, key="sel_guide_edit")
                
                if st.session_state.clear_edit_input:
                    st.session_state.clear_edit_input = False
                    st.session_state.new_acc_val_input = ""

                new_acc_input = st.text_input("رقم الحساب الجديد", key="new_acc_val_input", value="")
                
                col_act1, col_act2 = st.columns(2)
                with col_act1:
                    if st.button("💾 حفظ تعديل رقم الحساب", type="primary"):
                        st.session_state.confirming_edit_guide = {
                            "name": selected_guide_to_edit,
                            "new_acc": new_acc_input
                        }
                        st.rerun()
                with col_act2:
                    if st.button("🗑️ حذف هذا المرشد", type="primary", key="del_guide_btn_main"):
                        st.session_state.confirming_del_guide = {
                            "name": selected_guide_to_edit
                        }
                        st.rerun()
                
                if st.session_state.confirming_edit_guide is not None:
                    g_to_edit = st.session_state.confirming_edit_guide["name"]
                    n_acc = st.session_state.confirming_edit_guide["new_acc"]
                    
                    if not n_acc.strip():
                        st.error("⚠️ يرجى كتابة رقم الحساب الجديد أولاً قبل الحفظ!")
                        if st.button("❌ رجوع", type="primary"):
                            st.session_state.confirming_edit_guide = None
                            st.rerun()
                    else:
                        st.warning(f"⚠️ هل أنت متأكد من رغبتك في تغيير رقم حساب المرشد (**{g_to_edit}**) إلى الرقم الجديد: **{n_acc}**؟")
                        ec1, ec2 = st.columns(2)
                        with ec1:
                            if st.button("✔️ تأكيد وحفظ التعديل", type="primary", key="confirm_save_guide_acc"):
                                guides_df.loc[guides_df[name_column].astype(str) == g_to_edit, acc_column] = n_acc
                                overwrite_data(GUIDES_FILE, guides_df)
                                st.session_state.confirming_edit_guide = None
                                st.session_state.clear_edit_input = True
                                st.rerun()
                        with ec2:
                            if st.button("❌ إلغاء", key="cancel_save_guide_acc", type="primary"):
                                st.session_state.confirming_edit_guide = None
                                st.rerun()

                if st.session_state.confirming_del_guide is not None:
                    g_to_del = st.session_state.confirming_del_guide["name"]
                    
                    st.warning(f"⚠️ هل أنت متأكد تماماً من رغبتك في حذف المرشد (**{g_to_del}**) من قاعدة البيانات؟")
                    dc1, dc2 = st.columns(2)
                    with dc1:
                        if st.button("✔️ تأكيد الحذف النهائي", type="primary", key="confirm_del_guide_btn"):
                            guides_df = guides_df[guides_df[name_column].astype(str) != g_to_del].reset_index(drop=True)
                            overwrite_data(GUIDES_FILE, guides_df)
                            st.session_state.confirming_del_guide = None
                            st.rerun()
                    with dc2:
                        if st.button("❌ إلغاء الحذف", key="cancel_del_guide_btn", type="primary"):
                            st.session_state.confirming_del_guide = None
                            st.rerun()

            with col_section_right:
                st.markdown("#### إضافة مرشد جديد لقاعدة البيانات:")
                
                if st.session_state.clear_add_inputs:
                    st.session_state.clear_add_inputs = False
                    st.session_state.new_guide_name_input = ""
                    st.session_state.new_guide_acc_input = ""

                new_guide_name_input = st.text_input("اسم المرشد الجديد", key="new_guide_name_input", value="")
                new_guide_acc_input = st.text_input("رقم الحساب الخاص بالمرشد الجديد", key="new_guide_acc_input", value="")
                
                if st.button("➕ إضافة المرشد الجديد", type="primary"):
                    st.session_state.confirming_add_guide = {
                        "name": new_guide_name_input.strip(),
                        "acc": new_guide_acc_input.strip()
                    }
                    st.rerun()
                
                if st.session_state.confirming_add_guide is not None:
                    a_name = st.session_state.confirming_add_guide["name"]
                    a_acc = st.session_state.confirming_add_guide["acc"]
                    
                    if not a_name or not a_acc:
                        st.error("⚠️ يرجى كتابة (اسم المرشد) و(رقم الحساب) بشكل صحيح قبل الحفظ!")
                        if st.button("❌ رجوع لإتمام البيانات", type="primary", key="back_add_guide_err"):
                            st.session_state.confirming_add_guide = None
                            st.rerun()
                    else:
                        st.warning(f"⚠️ هل أنت متأكد من رغبتك في إضافة المرشد الجديد (**{a_name}**) برقم حساب: **{a_acc}**؟")
                        ac1, ac2 = st.columns(2)
                        with ac1:
                            if st.button("✔️ تأكيد وإضافة المرشد", type="primary", key="confirm_add_guide_btn"):
                                new_row_df = pd.DataFrame([{name_column: a_name, acc_column: a_acc}])
                                guides_df = pd.concat([guides_df, new_row_df], ignore_index=True)
                                overwrite_data(GUIDES_FILE, guides_df)
                                st.session_state.confirming_add_guide = None
                                st.session_state.clear_add_inputs = True
                                st.rerun()
                        with ac2:
                            if st.button("❌ إلغاء الإضافة", key="cancel_add_guide_btn", type="primary"):
                                st.session_state.confirming_add_guide = None
                                st.rerun()
            
    elif password:
        st.error("كلمة المرور غير صحيحة.")
    else:
        st.info("الرجاء إدخال كلمة المرور لعرض إدارة التصفيات.")

elif page == "الأرشيف":
    st.title("📁 أرشيف التصفيات المنتهية (تم)")
    st.markdown("---")
    
    password_archive = st.text_input("أدخل كلمة المرور لعرض الأرشيف", type="password", key="arch_pass")
    
    if password_archive == "159753":
        st.success("تم تسجيل الدخول بنجاح!")
        archive_df = load_data(ARCHIVE_FILE)
        
        if "viewing_archive_file" not in st.session_state:
            st.session_state.viewing_archive_file = None
        if "confirming_del_arch" not in st.session_state:
            st.session_state.confirming_del_arch = None

        if st.session_state.viewing_archive_file is not None:
            req_idx = st.session_state.viewing_archive_file
            if req_idx in archive_df.index:
                req_row = archive_df.loc[req_idx]
                
                if st.button("⬅️ رجوع إلى الأرشيف"):
                    st.session_state.viewing_archive_file = None
                    st.rerun()
                
                st.markdown(f"### 📄 تفاصيل تصفية الأرشيف للفايل: {req_row.get('File No', '')} (المرشد: {req_row.get('Guide Name', '')})")
                st.markdown(f"**التاريخ والوقت:** {req_row.get('Timestamp', '')} | **رقم الحساب:** {req_row.get('Account', '')}")
                st.markdown("---")
                
                st.write(f"**العهد (Advances):** {req_row.get('Advances', 0)}")
                st.write(f"**التحصيل (Collection):** {req_row.get('Collection', 0)}")
                st.write(f"**الأوبشن (Option):** {req_row.get('Option', '')}")
                st.write(f"**التذاكر (Tickets):** {req_row.get('Tickets', '')}")
                st.write(f"**إكرامية (Tip):** {req_row.get('Tip', 0)}")
                st.write(f"**بارك (Park):** {req_row.get('Park', 0)}")
                st.write(f"**غداء (Lunch):** {req_row.get('Lunch', 0)}")
                
                l_path = req_row.get("Lunch Receipt", "")
                if pd.notna(l_path) and str(l_path).strip() != "" and os.path.exists(str(l_path)):
                    st.image(str(l_path), caption="صورة فاتورة الغداء", use_container_width=True)
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
                            st.image(p, caption=f"صورة محلات رقم {idx+1}", use_container_width=True)
                else:
                    st.info("لا توجد صور لفواتير المحلات.")
            else:
                st.session_state.viewing_archive_file = None
                st.rerun()
        else:
            if not archive_df.empty:
                st.markdown("### 🔍 فلترة وعرض التصفيات المؤرشفة")
                
                all_guides_in_arch = archive_df["Guide Name"].dropna().unique().tolist()
                selected_arch_guide_filter = st.selectbox("اختر اسم المرشد لعرض جميع تصفياته المؤرشفة", options=["الكل (جميع المرشدين)"] + all_guides_in_arch, key="arch_guide_filter")
                
                if selected_arch_guide_filter != "الكل (جميع المرشدين)":
                    filtered_arch_df = archive_df[archive_df["Guide Name"] == selected_arch_guide_filter]
                    st.info(f"عرض التصفيات المؤرشفة الخاصة بالمرشد: **{selected_arch_guide_filter}** (عدد الطلبات: {len(filtered_arch_df)})")
                else:
                    filtered_arch_df = archive_df
                
                st.markdown("### التصفيات المنتهية")
                
                for idx, row in filtered_arch_df.iterrows():
                    cols = st.columns([1, 2, 2, 2, 1.5, 1.5])
                    with cols[0]:
                        st.write(f"**#{idx+1}**")
                    with cols[1]:
                        st.write(f"الفايل: {row.get('File No', '')}")
                    with cols[2]:
                        st.write(f"المرشد: {row.get('Guide Name', '')}")
                    with cols[3]:
                        st.write(f"الوقت: {row.get('Timestamp', '')}")
                    with cols[4]:
                        if st.button("عرض", key=f"view_arch_btn_{idx}", type="primary"):
                            st.session_state.viewing_archive_file = idx
                            st.rerun()
                    with cols[5]:
                        if st.button("🗑️ حذف", key=f"del_arch_btn_{idx}", type="primary"):
                            st.session_state.confirming_del_arch = idx
                            st.rerun()
                    
                    if st.session_state.confirming_del_arch == idx:
                        st.warning(f"⚠️ هل أنت متأكد من رغبتك في حذف تصفية الأرشيف للفايل رقم ({row.get('File No', '')})؟")
                        ca_col1, ca_col2 = st.columns(2)
                        with ca_col1:
                            if st.button("✔️ تأكيد الحذف النهائي", key=f"confirm_del_arch_{idx}", type="primary"):
                                archive_df = archive_df.drop(idx).reset_index(drop=True)
                                overwrite_data(ARCHIVE_FILE, archive_df)
                                st.session_state.confirming_del_arch = None
                                st.rerun()
                        with ca_col2:
                            if st.button("❌ رجوع (إلغاء)", key=f"cancel_del_arch_{idx}", type="primary"):
                                st.session_state.confirming_del_arch = None
                                st.rerun()
                    
                    st.markdown("---")
            else:
                st.info("لا توجد تصفيات مؤرشفة حتى الآن.")

    elif password_archive:
        st.error("كلمة المرور غير صحيحة.")
    else:
        st.info("الرجاء إدخال كلمة المرور لعرض صفحة الأرشيف.")
