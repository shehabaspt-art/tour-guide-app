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

if os.path.exists(GUIDE_ARCHIVE_FILE):
    try:
        df_temp = pd.read_excel(GUIDE_ARCHIVE_FILE)
        empty_df = pd.DataFrame(columns=df_temp.columns)
        empty_df.to_excel(GUIDE_ARCHIVE_FILE, index=False)
    except:
        os.remove(GUIDE_ARCHIVE_FILE)

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

acc_column = guides_df.columns[1] if len(guides_df.columns) > 1 else guides_df.columns[0]

SHOPS_LIST = [
    "وجية بردى", "اخناتون سجاد", "مينا للبرديات", "رويال سجاد", "اولد كايرو",
    "رويال للعطور", "خان الحلو للقطن", "فلور قطن", "طيبة للقطن", "فيلة بازار",
    "جولدن بيرد", "مملوك", "ريحانة توابل", "كنور توابل", "قصر العطور", "لازوريت", "محلات اخري"
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

# تشغيل القائمة الجانبية بشكل دائم دون زر إخفاء
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

    rc = st.session_state.form_reset_counter

    with st.form("guide_form", clear_on_submit=False):
        st.subheader("بيانات المرشد")
        
        col_top1, col_top2, col_top3 = st.columns(3)
        with col_top1:
            raw_accs = guides_df[acc_column].apply(clean_acc_number).dropna().unique().tolist()
            account_options = [None] + [str(acc) for acc in raw_accs if str(acc).strip() != ""]
            account_no = st.selectbox("رقم الحساب أو رقم التليفون الخاص بالتحويل", options=account_options, index=0, key=f"form_account_no_{rc}")
        with col_top2:
            file_no = st.text_input("رقم الفايل (File Number) *إلزامي*", key=f"form_file_no_{rc}")
        with col_top3:
            advances = st.number_input("العهد (Advances)", min_value=0.0, step=10.0, key=f"form_advances_{rc}")

        work_order_image = st.file_uploader("رفع صور أمر الشغل", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key=f"work_order_imgs_{rc}")

        st.markdown("---")
        st.subheader("التحصيل (Collection)")
        
        col_c1, col_c2 = st.columns([2, 1])
        with col_c1:
            collection_val = st.number_input("قيمة التحصيل", min_value=0.0, step=10.0, key=f"form_collection_val_{rc}")
        with col_c2:
            collection_curr = st.selectbox("عملة التحصيل", options=["جنية", "يورو", "دولار"], key=f"form_collection_curr_{rc}")

        st.markdown("---")
        st.subheader("أوبشنال (Optional)")
        
        option_data_list = []
        for i in range(st.session_state.option_rows_count):
            st.markdown(f"**أوبشنال رقم ({i+1})**")
            col_opt1, col_opt2, col_opt3, col_opt4, col_opt5 = st.columns(5)
            with col_opt1:
                opt_type = st.text_input("نوع الأوبشنال", key=f"opt_type_{rc}_{i}")
            with col_opt2:
                opt_val = st.number_input("قيمة الأوبشنال", min_value=0.0, step=10.0, key=f"opt_val_{rc}_{i}")
            with col_opt3:
                opt_curr = st.selectbox("عملة الأوبشنال", options=["مصري", "دولار", "يورو"], key=f"opt_curr_{rc}_{i}")
            with col_opt4:
                opt_pay = st.selectbox("طريقة الدفع", options=[None, "كاش", "لينك"], key=f"opt_pay_{rc}_{i}")
            with col_opt5:
                cash_h = st.selectbox("الفلوس مع مين؟", options=[None, "مع المرشد", "مع السواق"], key=f"cash_h_{rc}_{i}")
            
            option_data_list.append({
                "type": opt_type, "value": opt_val, "curr": opt_curr, "pay": opt_pay, "holder": cash_h
            })
            if i < st.session_state.option_rows_count - 1:
                st.markdown("---")

        add_more_option = st.form_submit_button("➕ إضافة أوبشنال آخر")

        st.markdown("---")
        st.subheader("مصاريف (Expenses)")
        col_tkt1, col_tkt2 = st.columns(2)
        with col_tkt1:
            ticket_value = st.number_input("قيمة التذاكر", min_value=0.0, step=10.0, key=f"form_tkt_val_{rc}")
        with col_tkt2:
            ticket_type = st.text_input("نوع التذاكر", key=f"form_tkt_type_{rc}")

        st.markdown("---")
        col_misc1, col_misc2, col_misc3 = st.columns(3)
        with col_misc1:
            tip = st.number_input("إكرامية", min_value=0.0, step=10.0, key=f"form_tip_{rc}")
        with col_misc2:
            park = st.number_input("بارك", min_value=0.0, step=10.0, key=f"form_park_{rc}")
        with col_misc3:
            lunch = st.number_input("غداء", min_value=0.0, step=10.0, key=f"form_lunch_{rc}")

        lunch_images = st.file_uploader("رفع صور فواتير الغداء", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key=f"lunch_imgs_{rc}")

        st.markdown("---")
        st.subheader("فواتير ومحلات التسوق")
        
        shop_data_list = []
        for j in range(st.session_state.shop_rows_count):
            st.markdown(f"**المحل رقم ({j+1})**")
            col_s1, col_s2, col_s3, col_s4 = st.columns([2, 1, 1, 2])
            with col_s1:
                shop_name_choice = st.selectbox("اسم المحل", options=[None] + SHOPS_LIST, key=f"shop_name_{rc}_{j}")
            with col_s2:
                shop_val = st.number_input("القيمة", min_value=0.0, step=10.0, key=f"shop_val_{rc}_{j}")
            with col_s3:
                shop_curr = st.selectbox("العملة", options=["مصري", "يورو", "دولار"], key=f"shop_curr_{rc}_{j}")
            with col_s4:
                shop_file_img = st.file_uploader("رفع فاتورة المحل", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key=f"shop_img_{rc}_{j}")
            
            shop_data_list.append({
                "name": shop_name_choice, "value": shop_val, "curr": shop_curr, "images": shop_file_img
            })
            if j < st.session_state.shop_rows_count - 1:
                st.markdown("---")

        add_more_shop = st.form_submit_button("➕ إضافة محل")

        st.markdown("---")
        st.subheader("محلات خارجية")
        
        col_oth1, col_oth2, col_oth3, col_oth4 = st.columns([2, 1, 1, 2])
        with col_oth1:
            other_shops = st.text_input("اسم المحل", key=f"other_shops_name_{rc}")
        with col_oth2:
            other_shops_val = st.number_input("القيمة", min_value=0.0, step=10.0, key=f"other_shops_val_{rc}")
        with col_oth3:
            other_shops_curr = st.selectbox("العملة", options=["مصري", "دولار", "يورو"], key=f"other_shops_curr_{rc}")
        with col_oth4:
            other_shops_images = st.file_uploader("رفع فاتورة المحل", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key=f"other_shops_imgs_{rc}")

        submitted = st.form_submit_button("إرسال الطلب للمدير", type="primary")

        if add_more_option:
            st.session_state.option_rows_count += 1
            st.rerun()

        if add_more_shop:
            st.session_state.shop_rows_count += 1
            st.rerun()

        if submitted:
            validation_error = False
            validation_pay_error = False

            for i in range(st.session_state.option_rows_count):
                o_val = st.session_state.get(f"opt_val_{rc}_{i}", 0.0)
                p_val = st.session_state.get(f"opt_pay_{rc}_{i}", None)
                c_h = st.session_state.get(f"cash_h_{rc}_{i}", None)
                o_type = st.session_state.get(f"opt_type_{rc}_{i}", "")
                if (o_val > 0 or o_type.strip()) and not p_val:
                    validation_pay_error = True
                    break
                if p_val == "كاش" and not c_h:
                    validation_error = True
                    break

            if not account_no:
                st.error("⚠️ عذراً، يجب اختيار (رقم الحساب أو رقم التليفون) أولاً!")
            elif not file_no.strip():
                st.error("⚠️ عذراً، لا يمكن إرسال الطلب. يرجى إدخال (رقم الفايل) أولاً بشكل إلزامي!")
            elif validation_pay_error:
                st.error("⚠️ عذراً، نظراً لإدخال قيمة أو نوع في أحد الأوبشنالز، يجب اختيار (طريقة الدفع) [كاش / لينك] بشكل إلزامي!")
            elif validation_error:
                st.error("⚠️ عذراً، نظراً لاختيار طريقة الدفع (كاش)، يجب تحديد ما إذا كانت الأموال [مع المرشد / مع السواق] بشكل إلزامي!")
            else:
                clean_acc_selected = clean_acc_number(account_no)
                
                cairo_dt = datetime.now(ZoneInfo("Africa/Cairo"))
                current_time_str = cairo_dt.strftime('%Y-%m-%d %I:%M %p')
                
                work_order_paths = []
                if work_order_image:
                    for img in work_order_image:
                        wo_path = os.path.join(UPLOAD_DIR, f"wo_{time.time()}_{img.name}")
                        with open(wo_path, "wb") as f:
                            f.write(img.getbuffer())
                        work_order_paths.append(wo_path)

                lunch_paths = []
                if lunch_images:
                    for img in lunch_images:
                        l_path = os.path.join(UPLOAD_DIR, f"lunch_{time.time()}_{img.name}")
                        with open(l_path, "wb") as f:
                            f.write(img.getbuffer())
                        lunch_paths.append(l_path)

                other_shops_paths = []
                if other_shops_images:
                    for img in other_shops_images:
                        os_path = os.path.join(UPLOAD_DIR, f"othershops_{time.time()}_{img.name}")
                        with open(os_path, "wb") as f:
                            f.write(img.getbuffer())
                        other_shops_paths.append(os_path)

                all_shop_paths = []
                shops_summary_list = []
                shops_names_only = []
                for j in range(st.session_state.shop_rows_count):
                    s_name = st.session_state.get(f"shop_name_{rc}_{j}", None)
                    s_val = st.session_state.get(f"shop_val_{rc}_{j}", 0.0)
                    s_curr = st.session_state.get(f"shop_curr_{rc}_{j}", "مصري")
                    s_imgs = st.session_state.get(f"shop_img_{rc}_{j}", [])
                    
                    shop_img_paths_str = ""
                    if s_imgs:
                        paths_single_shop = []
                        for img in s_imgs:
                            s_path = os.path.join(UPLOAD_DIR, f"shop_{time.time()}_{img.name}")
                            with open(s_path, "wb") as f:
                                f.write(img.getbuffer())
                            paths_single_shop.append(s_path)
                            all_shop_paths.append(s_path)
                        shop_img_paths_str = ",".join(paths_single_shop)

                    if s_name:
                        shops_names_only.append(s_name)
                        shops_summary_list.append(f"{s_name}: {s_val} {s_curr} [IMG:{shop_img_paths_str}]")

                if other_shops.strip():
                    shops_summary_list.append(f"{other_shops} (خارجي): {other_shops_val} {other_shops_curr} [IMG:{','.join(other_shops_paths)}]")

                all_shop_paths.extend(other_shops_paths)

                options_summary_list = []
                option_types_list = []
                for i in range(st.session_state.option_rows_count):
                    o_type = st.session_state.get(f"opt_type_{rc}_{i}", "")
                    o_val = st.session_state.get(f"opt_val_{rc}_{i}", 0.0)
                    o_curr = st.session_state.get(f"opt_curr_{rc}_{i}", "مصري")
                    o_pay = st.session_state.get(f"opt_pay_{rc}_{i}", None)
                    o_holder = st.session_state.get(f"cash_h_{rc}_{i}", "")
                    
                    if o_type.strip() or o_val > 0:
                        option_types_list.append(o_type)
                        pay_str = f"({o_pay})" if o_pay else ""
                        detail_str = f"{o_val} {o_curr} {pay_str}".strip()
                        if o_pay == "كاش" and o_holder:
                            detail_str += f" - [{o_holder}]"
                        if o_type:
                            detail_str = f"{o_type}: " + detail_str
                        options_summary_list.append(detail_str)

                new_entry = {
                    "Timestamp": current_time_str,
                    "Guide Name": "",
                    "Account": clean_acc_selected,
                    "File No": file_no,
                    "Work Order Images": ",".join(work_order_paths) if work_order_paths else "",
                    "Advances": advances,
                    "Collection": f"{collection_val} {collection_curr}",
                    "Option Type": ", ".join(option_types_list),
                    "Option": "|||".join(options_summary_list),
                    "Tickets": f"{ticket_value} - {ticket_type}",
                    "Tip": tip,
                    "Park": park,
                    "Lunch": lunch,
                    "Lunch Receipt": ",".join(lunch_paths) if lunch_paths else "",
                    "Shop Names": ", ".join(shops_names_only),
                    "Other Shops": f"{other_shops} : {other_shops_val} {other_shops_curr}" if other_shops.strip() else "",
                    "Shops Details": "|||".join(shops_summary_list),
                    "Shop Images": ",".join(all_shop_paths) if all_shop_paths else ""
                }
                save_to_file(SUBMISSIONS_FILE, new_entry)
                
                st.success("✅ تم إرسال الطلب للمدير بنجاح!")
                time.sleep(3)
                
                st.session_state.option_rows_count = 1
                st.session_state.shop_rows_count = 1
                st.session_state.form_reset_counter += 1
                st.rerun()

elif page == "سجلات المرشد":
    st.title("👤 سجلات المرشد")
    st.markdown("---")
    entered_acc = st.text_input("رقم الحساب أو رقم التليفون الخاص بالتحويل", key="guide_login_acc")
    if entered_acc.strip():
        g_arch_df = load_data(GUIDE_ARCHIVE_FILE)
        if not g_arch_df.empty:
            clean_entered_acc = clean_acc_number(entered_acc)
            g_arch_df['Account'] = g_arch_df['Account'].apply(clean_acc_number)
            matched_guide_records = g_arch_df[g_arch_df['Account'] == clean_entered_acc]
            if not matched_guide_records.empty:
                for idx, row in matched_guide_records.iterrows():
                    st.markdown(f"فايل: {row.get('File No', '')} - التاريخ: {row.get('Timestamp', '')}")
            else:
                st.warning("⚠️ لا توجد تصفيات مسجلة لهذا الرقم.")

elif page == "إدارة التصفيات":
    st.title("📊 إدارة التصفيات")
    st.markdown("---")
    password = st.text_input("أدخل كلمة المرور لعرض لوحة الإدارة", type="password", key="mgr_pass")
    if password == "159753":
        st.success("تم تسجيل الدخول بنجاح.")

elif page == "الأرشيف":
    st.title("📁 أرشيف التصفيات المنتهية")
    st.markdown("---")
    password_arch = st.text_input("أدخل كلمة المرور لعرض الأرشيف", type="password", key="arch_pass")
    if password_arch == "159753":
        st.success("تم تسجيل الدخول للأرشيف بنجاح.")
