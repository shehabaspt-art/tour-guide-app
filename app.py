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

    rc = st.session_state.form_reset_counter

    with st.form("guide_form", clear_on_submit=False):
        st.subheader("بيانات المرشد")
        
        col_top1, col_top2 = st.columns(2)
        with col_top1:
            account_options = [None] + guides_df[acc_column].apply(clean_acc_number).tolist()
            account_no = st.selectbox("رقم الحساب", options=account_options, index=0, key=f"form_account_no_{rc}")
        with col_top2:
            file_no = st.text_input("رقم الفايل (File Number) *إلزامي*", key=f"form_file_no_{rc}")

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
                cash_h = st.selectbox("المبلغ", options=[None, "مع المرشد", "مع السواق"], key=f"cash_h_{rc}_{i}")
            
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
                st.error("⚠️ عذراً، يجب اختيار (رقم الحساب) أولاً!")
            elif not file_no.strip():
                st.error("⚠️ عذراً، لا يمكن إرسال الطلب. يرجى إدخال (رقم الفايل) أولاً بشكل إلزامي!")
            elif validation_pay_error:
                st.error("⚠️ عذراً، نظراً لإدخال قيمة أو نوع في أحد الأوبشنالز، يجب اختيار (طريقة الدفع) [كاش / لينك] بشكل إلزامي!")
            elif validation_error:
                st.error("⚠️ عذراً، نظراً لاختيار طريقة الدفع (كاش)، يجب اختيار (المبلغ) [مع المرشد / مع السواق] بشكل إلزامي!")
            else:
                clean_acc_selected = clean_acc_number(account_no)
                guide_name = get_guide_name_by_account(clean_acc_selected)
                
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
                    "Guide Name": guide_name,
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

    if "viewing_guide_archive_file" not in st.session_state:
        st.session_state.viewing_guide_archive_file = None

    if "guide_login_acc" not in st.session_state:
        st.session_state.guide_login_acc = ""

    if st.session_state.viewing_guide_archive_file is not None:
        g_arch_df = load_data(GUIDE_ARCHIVE_FILE)
        req_idx = st.session_state.viewing_guide_archive_file
        if req_idx in g_arch_df.index:
            req_row = g_arch_df.loc[req_idx]
            
            if st.button("رجوع"):
                st.session_state.guide_login_acc = str(req_row.get('Account', ''))
                st.session_state.viewing_guide_archive_file = None
                st.rerun()

            st.markdown(f"### 📄 تفاصيل التصفية المؤرشفة للفايل: {req_row.get('File No', '')}")
            row_acc = req_row.get('Account', '')
            row_gname = get_guide_name_by_account(row_acc)
            st.markdown(f"**التاريخ:** {req_row.get('Timestamp', '')} | **رقم الحساب:** {row_acc}")
            st.markdown("---")

            st.markdown("#### صور أمر الشغل:")
            wo_paths = req_row.get('Work Order Images', '')
            if pd.notna(wo_paths) and str(wo_paths).strip() != "":
                wo_list = str(wo_paths).split(",")
                wo_cols = st.columns(min(len(wo_list), 3))
                for idx, p in enumerate(wo_list):
                    if os.path.exists(p):
                        with wo_cols[idx % 3]:
                            st.image(p, caption=f"صورة أمر الشغل رقم {idx+1}", width=220)
            else:
                st.info("لا توجد صور لأمر الشغل.")

            st.markdown("---")
            
            st.markdown("""
                <style>
                .report-card {
                    background-color: #f8f9fa;
                    border: 1px solid #e9ecef;
                    border-right: 4px solid #28a745;
                    padding: 15px;
                    border-radius: 8px;
                    margin-bottom: 12px;
                }
                .report-title {
                    font-weight: bold;
                    color: #1b5e20;
                    margin-bottom: 5px;
                    font-size: 1.05rem;
                }
                .report-value {
                    color: #333333;
                    font-size: 1.1rem;
                    font-weight: 500;
                }
                .sub-item-card {
                    background-color: #ffffff;
                    border: 1px solid #d4edda;
                    border-left: 4px solid #28a745;
                    padding: 8px 12px;
                    border-radius: 6px;
                    margin-top: 6px;
                    font-size: 1.05rem;
                    color: #155724;
                    font-weight: 600;
                }
                </style>
            """, unsafe_allow_html=True)

            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.markdown(f"""
                    <div class="report-card">
                        <div class="report-title">💰 العهد (Advances)</div>
                        <div class="report-value">{req_row.get('Advances', 0)}</div>
                    </div>
                """, unsafe_allow_html=True)
            with col_m2:
                st.markdown(f"""
                    <div class="report-card">
                        <div class="report-title">📥 التحصيل (Collection)</div>
                        <div class="report-value">{req_row.get('Collection', 0)}</div>
                    </div>
                """, unsafe_allow_html=True)
            with col_m3:
                st.markdown(f"""
                    <div class="report-card">
                        <div class="report-title">🎁 إكرامية (Tip)</div>
                        <div class="report-value">{req_row.get('Tip', 0)}</div>
                    </div>
                """, unsafe_allow_html=True)

            col_m4, col_m5, col_m6 = st.columns(3)
            with col_m4:
                st.markdown(f"""
                    <div class="report-card">
                        <div class="report-title">🅿️ بارك (Park)</div>
                        <div class="report-value">{req_row.get('Park', 0)}</div>
                    </div>
                """, unsafe_allow_html=True)
            with col_m5:
                st.markdown(f"""
                    <div class="report-card">
                        <div class="report-title">🍽️ غداء (Lunch)</div>
                        <div class="report-value">{req_row.get('Lunch', 0)}</div>
                    </div>
                """, unsafe_allow_html=True)
            with col_m6:
                st.markdown(f"""
                    <div class="report-card">
                        <div class="report-title">🎟️ التذاكر (Tickets)</div>
                        <div class="report-value">{req_row.get('Tickets', 'لا يوجد')}</div>
                    </div>
                """, unsafe_allow_html=True)

            opt_items = parse_items_smart(req_row.get('Option', ''))
            opt_inner_html = ""
            if opt_items:
                for item in opt_items:
                    opt_inner_html += f'<div class="sub-item-card">✨ {item}</div>'
            else:
                opt_inner_html = '<div class="report-value" style="color: #6c757d; font-size: 0.95rem;">لا يوجد</div>'

            st.markdown(f"""
                <div class="report-card" style="border-right-color: #007bff;">
                    <div class="report-title">✨ الأوبشنال (Optional)</div>
                    {opt_inner_html}
                </div>
            """, unsafe_allow_html=True)

            shop_raw = req_row.get('Shops Details', req_row.get('Shop Names', ''))
            shop_items = parse_items_smart(shop_raw)
            shop_inner_html = ""
            if shop_items:
                for item in shop_items:
                    clean_item_text = item.split("[IMG:")[0].strip()
                    shop_inner_html += f'<div class="sub-item-card" style="border-left-color: #ffc107; color: #856404;">🛍️ {clean_item_text}</div>'
            else:
                shop_inner_html = '<div class="report-value" style="color: #6c757d; font-size: 0.95rem;">لا يوجد</div>'

            st.markdown(f"""
                <div class="report-card" style="border-right-color: #ffc107;">
                    <div class="report-title">🛍️ تفاصيل المحلات</div>
                    {shop_inner_html}
                </div>
            """, unsafe_allow_html=True)

            if pd.notna(req_row.get('Other Shops', '')) and str(req_row.get('Other Shops', '')).strip() != "":
                st.markdown(f"""
                    <div class="report-card" style="border-right-color: #17a2b8;">
                        <div class="report-title">🏪 محلات خارجية</div>
                        <div class="report-value">{req_row.get('Other Shops', '')}</div>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("#### صور فواتير الغداء:")
            l_paths = req_row.get('Lunch Receipt', '')
            if pd.notna(l_paths) and str(l_paths).strip() != "":
                l_list = str(l_paths).split(",")
                l_cols = st.columns(min(len(l_list), 3))
                for idx, p in enumerate(l_list):
                    if os.path.exists(p):
                        with l_cols[idx % 3]:
                            st.image(p, caption=f"صورة فاتورة الغداء رقم {idx+1}", width=220)
            else:
                st.info("لا توجد صور لفواتير الغداء.")

            st.markdown("---")
            s_paths = req_row.get('Shop Images', '')
            st.markdown("#### صور فواتير المحلات:")
            if pd.notna(s_paths) and str(s_paths).strip() != "":
                paths_list = str(s_paths).split(",")
                s_cols = st.columns(min(len(paths_list), 3))
                for idx, p in enumerate(paths_list):
                    if os.path.exists(p):
                        with s_cols[idx % 3]:
                            st.image(p, caption=f"صورة محلات رقم {idx+1}", width=220)
            else:
                st.info("لا توجد صور لفواتير المحلات.")
        else:
            st.session_state.viewing_guide_archive_file = None
            st.rerun()
    else:
        st.markdown("### 🔑 أدخل رقم الحساب للاطلاع على سجلاتك (خاص بالمرشد)")
        
        account_dropdown_options = [None] + guides_df[acc_column].apply(clean_acc_number).tolist()
        entered_acc = st.selectbox(
            "اختر رقم الحساب الخاص بك",
            options=account_dropdown_options,
            index=0,
            key="guide_login_acc_select"
        )
        if entered_acc:
            entered_acc = str(entered_acc)

        if entered_acc and entered_acc.strip():
            g_arch_df = load_data(GUIDE_ARCHIVE_FILE)
            if not g_arch_df.empty:
                clean_entered_acc = clean_acc_number(entered_acc)
                g_arch_df['Account'] = g_arch_df['Account'].apply(clean_acc_number)
                
                matched_guide_records = g_arch_df[g_arch_df['Account'] == clean_entered_acc]
                
                if not matched_guide_records.empty:
                    st.success(f"تم العثور على ({len(matched_guide_records)}) تصفية مسجلة برقم حسابك.")
                    st.markdown("### 📋 سجلات الأرشيف الخاصة بك")

                    for idx, row in matched_guide_records.iterrows():
                        r_acc = row.get('Account', '')
                        st.markdown(f"""
                            <div class="record-card">
                                <div class="card-header-row">
                                    <span class="card-id">#{idx+1}</span>
                                    <span class="card-file">الفايل: {row.get('File No', '')}</span>
                                </div>
                                <div class="card-body-row">
                                    <div class="card-guide">رقم الحساب: {r_acc}</div>
                                    <div class="card-time">التاريخ: {row.get('Timestamp', '')}</div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        col_vw = st.columns([6, 1])
                        with col_vw[1]:
                            if st.button("عرض التفاصيل", key=f"view_g_arch_{idx}", type="primary"):
                                st.session_state.viewing_guide_archive_file = idx
                                st.rerun()
                        st.markdown("---")
                else:
                    st.warning("⚠️ لا توجد أي تصفيات مسجلة أو منتهية لهذا الرقم في سجلات المرشدين.")
            else:
                st.info("لا توجد سجلات مؤرشفة للمرشدين حتى الآن.")

elif page == "إدارة التصفيات":
    st.title("📊 إدارة التصفيات")
    st.markdown("---")

    password = st.text_input("أدخل كلمة المرور لعرض لوحة الإدارة", type="password", key="mgr_pass")

    if password == "159753":
        st.success("تم تسجيل الدخول للاستعراض بنجاح.")
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
                    st.session_state.show_liquidation_cards = False
                    st.rerun()

                cur_acc = req_row.get('Account', '')
                cur_gname = get_guide_name_by_account(cur_acc)
                st.markdown(f"### 📄 تفاصيل تصفية الفايل: {req_row.get('File No', '')} (المرشد: {cur_gname})")
                st.markdown(f"**التاريخ:** {req_row.get('Timestamp', '')} | **رقم الحساب:** {cur_acc} | **اسم المرشد:** {cur_gname}")
                st.markdown("---")

                if st.session_state.get("show_liquidation_cards", False):
                    st.markdown("## 🧮 شاشة التصفية الذكية والكروت الحسابية")
                    
                    def parse_val(val_str):
                        try:
                            return float(str(val_str).split()[0])
                        except:
                            try:
                                return float(val_str)
                            except:
                                return 0.0

                    default_guide_name = cur_gname
                    default_file_no = req_row.get('File No', '')
                    default_park = float(req_row.get('Park', 0.0))
                    default_tip = float(req_row.get('Tip', 0.0))
                    default_lunch = float(req_row.get('Lunch', 0.0))
                    
                    tkt_raw = str(req_row.get('Tickets', '0'))
                    default_tickets = parse_val(tkt_raw.split('-')[0]) if '-' in tkt_raw else parse_val(tkt_raw)
                    
                    advances_val = float(req_row.get('Advances', 0.0))
                    collection_raw = str(req_row.get('Collection', '0'))
                    default_collection_str = str(parse_val(collection_raw))

                    opt_raw_str = str(req_row.get('Option', ''))
                    default_opt_collection = 0.0
                    parsed_opts = parse_items_smart(opt_raw_str)
                    for opt_item in parsed_opts:
                        import re
                        numbers_found = re.findall(r"[-+]?\d*\.\d+|\d+", opt_item)
                        if numbers_found:
                            default_opt_collection += float(numbers_found[0])
                    default_opt_collection_str = str(default_opt_collection)

                    st.markdown("### 📋 كروت البيانات الأساسية")
                    c_k1, c_k2, c_k3, c_k4 = st.columns(4)
                    with c_k1:
                        card_guide_name = st.text_input("اسم المرشد", value=default_guide_name, key=f"lk_gname_{req_idx}")
                    with c_k2:
                        card_file_no = st.text_input("رقم الفايل", value=default_file_no, key=f"lk_fno_{req_idx}")
                    with c_k3:
                        card_guidance_val = st.number_input("قيمة الارشاد", min_value=0.0, value=0.0, step=10.0, key=f"lk_guidance_{req_idx}")
                    with c_k4:
                        card_park = st.number_input("باركات", min_value=0.0, value=default_park, step=10.0, key=f"lk_park_{req_idx}")

                    c_k5, c_k6, c_k7, c_k8 = st.columns(4)
                    with c_k5:
                        card_tip = st.number_input("إكراميات", min_value=0.0, value=default_tip, step=10.0, key=f"lk_tip_{req_idx}")
                    with c_k6:
                        card_lunch = st.number_input("غداء", min_value=0.0, value=default_lunch, step=10.0, key=f"lk_lunch_{req_idx}")
                    with c_k7:
                        card_tickets = st.number_input("تذاكر", min_value=0.0, value=default_tickets, step=10.0, key=f"lk_tickets_{req_idx}")
                    with c_k8:
                        card_guide_commission = st.number_input("عمولة المرشد", min_value=0.0, value=0.0, step=10.0, key=f"lk_guide_comm_{req_idx}")

                    st.markdown("---")

                    st.markdown("### 🛍️ بند عمولة المحلات")
                    if f"shop_rows_{req_idx}" not in st.session_state:
                        st.session_state[f"shop_rows_{req_idx}"] = 1

                    total_shop_comm_guide = 0.0
                    total_shop_comm_company = 0.0

                    for s_i in range(st.session_state[f"shop_rows_{req_idx}"]):
                        cols_sh = st.columns([2, 2, 2, 2])
                        with cols_sh[0]:
                            shop_sel_name = st.selectbox(f"اسم المحل ({s_i+1})", options=SHOPS_LIST, key=f"sh_name_{req_idx}_{s_i}")
                        with cols_sh[1]:
                            shop_tot_inv = st.number_input(f"إجمالي الفاتورة ({s_i+1})", min_value=0.0, value=0.0, step=10.0, key=f"sh_inv_{req_idx}_{s_i}")
                        with cols_sh[2]:
                            shop_comm_comp = st.number_input(f"عمولة الشركة ({s_i+1})", min_value=0.0, value=0.0, step=10.0, key=f"sh_ccomp_{req_idx}_{s_i}")
                        with cols_sh[3]:
                            shop_comm_guid = st.number_input(f"عمولة المرشد ({s_i+1})", min_value=0.0, value=0.0, step=10.0, key=f"sh_cguid_{req_idx}_{s_i}")
                        
                        if shop_tot_inv > 0 or shop_comm_comp > 0 or shop_comm_guid > 0:
                            with st.expander(f"🔍 تفاصيل ومعادلة المحل ({s_i+1})"):
                                st.write(f"إجمالي الفاتورة = {shop_tot_inv} -> عمولة الشركة ({shop_comm_comp}) + عمولة المرشد ({shop_comm_guid})")

                        total_shop_comm_guide += shop_comm_guid
                        total_shop_comm_company += shop_comm_comp

                    if st.button("➕ إضافة محل آخر", key=f"add_shop_row_btn_{req_idx}"):
                        st.session_state[f"shop_rows_{req_idx}"] += 1
                        st.rerun()

                    st.markdown("---")

                    st.markdown("### ✨ بند عمولة الأوبشنال")
                    if f"opt_rows_{req_idx}" not in st.session_state:
                        st.session_state[f"opt_rows_{req_idx}"] = 1

                    total_opt_comm_guide = 0.0

                    for o_i in range(st.session_state[f"opt_rows_{req_idx}"]):
                        cols_op = st.columns([3, 2, 2])
                        with cols_op[0]:
                            opt_type_name = st.text_input(f"نوع الأوبشنال ({o_i+1})", key=f"op_type_{req_idx}_{o_i}")
                        with cols_op[1]:
                            opt_val_item = st.number_input(f"قيمة الأوبشنال ({o_i+1})", min_value=0.0, value=0.0, step=10.0, key=f"op_val_{req_idx}_{o_i}")
                        with cols_op[2]:
                            opt_comm_guid = st.number_input(f"عمولة المرشد ({o_i+1})", min_value=0.0, value=0.0, step=10.0, key=f"op_cguid_{req_idx}_{o_i}")

                        if opt_val_item > 0 or opt_comm_guid > 0:
                            with st.expander(f"🔍 تفاصيل ومعادلة الأوبشنال ({o_i+1})"):
                                st.write(f"قيمة الأوبشنال = {opt_val_item} -> عمولة المرشد = {opt_comm_guid}")

                        total_opt_comm_guide += opt_comm_guid

                    if st.button("➕ إضافة أوبشنال آخر", key=f"add_opt_row_btn_{req_idx}"):
                        st.session_state[f"opt_rows_{req_idx}"] += 1
                        st.rerun()

                    st.markdown("---")

                    total_revenue = card_guidance_val + card_park + card_tip + card_lunch + card_tickets + card_guide_commission + total_shop_comm_company + total_opt_comm_guide

                    st.markdown("### 💰 كروت العهد والتحصيلات")
                    cc_col1, cc_col2, cc_col3 = st.columns(3)
                    with cc_col1:
                        card_advances = st.number_input("عهدة", min_value=0.0, value=advances_val, step=10.0, key=f"lk_adv_{req_idx}")
                    with cc_col2:
                        collec_expr = st.text_input("تحصيلات", value=default_collection_str, key=f"lk_collec_{req_idx}")
                        card_collections = evaluate_expression(collec_expr)
                    with cc_col3:
                        opt_collec_expr = st.text_input("تحصيلات الأوبشنال", value=default_opt_collection_str, key=f"lk_opt_collec_{req_idx}")
                        card_opt_collections = evaluate_expression(opt_collec_expr)

                    total_dues = card_advances + card_collections + card_opt_collections
                    net_balance = total_revenue - total_dues

                    st.markdown("---")
                    st.markdown("### 📊 الملخص النهائي للكروت الحسابية")
                    res_c1, res_c2, res_c3 = st.columns(3)
                    with res_c1:
                        st.metric(label="📈 إجمالي الإيراد", value=f"{total_revenue:,.2f}")
                    with res_c2:
                        st.metric(label="📉 إجمالي المستحقات", value=f"{total_dues:,.2f}")
                    with res_c3:
                        st.metric(label="💎 الصافي النهائي", value=f"{net_balance:,.2f}", delta=f"{net_balance:,.2f}")
                    st.markdown("---")
                
                else:
                    st.markdown("#### صور أمر الشغل:")
                    wo_paths = req_row.get('Work Order Images', '')
                    if pd.notna(wo_paths) and str(wo_paths).strip() != "":
                        wo_list = str(wo_paths).split(",")
                        wo_cols = st.columns(min(len(wo_list), 3))
                        for idx, p in enumerate(wo_list):
                            if os.path.exists(p):
                                with wo_cols[idx % 3]:
                                    st.image(p, caption=f"صورة أمر الشغل رقم {idx+1}", width=220)
                    else:
                        st.info("لا توجد صور لأمر الشغل.")

                    st.markdown("---")
                    
                    st.markdown("""
                        <style>
                        .report-card {
                            background-color: #f8f9fa;
                            border: 1px solid #e9ecef;
                            border-right: 4px solid #28a745;
                            padding: 15px;
                            border-radius: 8px;
                            margin-bottom: 12px;
                        }
                        .report-title {
                            font-weight: bold;
                            color: #1b5e20;
                            margin-bottom: 5px;
                            font-size: 1.05rem;
                        }
                        .report-value {
                            color: #333333;
                            font-size: 1.1rem;
                            font-weight: 500;
                        }
                        .sub-item-card {
                            background-color: #ffffff;
                            border: 1px solid #d4edda;
                            border-left: 4px solid #28a745;
                            padding: 8px 12px;
                            border-radius: 6px;
                            margin-top: 6px;
                            font-size: 1.05rem;
                            color: #155724;
                            font-weight: 600;
                        }
                        </style>
                    """, unsafe_allow_html=True)

                    col_m1, col_m2, col_m3 = st.columns(3)
                    with col_m1:
                        st.markdown(f"""
                            <div class="report-card">
                                <div class="report-title">💰 العهد (Advances)</div>
                                <div class="report-value">{req_row.get('Advances', 0)}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    with col_m2:
                        st.markdown(f"""
                            <div class="report-card">
                                <div class="report-title">📥 التحصيل (Collection)</div>
                                <div class="report-value">{req_row.get('Collection', 0)}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    with col_m3:
                        st.markdown(f"""
                            <div class="report-card">
                                <div class="report-title">🎁 إكرامية (Tip)</div>
                                <div class="report-value">{req_row.get('Tip', 0)}</div>
                            </div>
                        """, unsafe_allow_html=True)

                    col_m4, col_m5, col_m6 = st.columns(3)
                    with col_m4:
                        st.markdown(f"""
                            <div class="report-card">
                                <div class="report-title">🅿️ بارك (Park)</div>
                                <div class="report-value">{req_row.get('Park', 0)}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    with col_m5:
                        st.markdown(f"""
                            <div class="report-card">
                                <div class="report-title">🍽️ غداء (Lunch)</div>
                                <div class="report-value">{req_row.get('Lunch', 0)}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    with col_m6:
                        st.markdown(f"""
                            <div class="report-card">
                                <div class="report-title">🎟️ التذاكر (Tickets)</div>
                                <div class="report-value">{req_row.get('Tickets', 'لا يوجد')}</div>
                            </div>
                        """, unsafe_allow_html=True)

                    opt_items = parse_items_smart(req_row.get('Option', ''))
                    opt_inner_html = ""
                    if opt_items:
                        for item in opt_items:
                            opt_inner_html += f'<div class="sub-item-card">✨ {item}</div>'
                    else:
                        opt_inner_html = '<div class="report-value" style="color: #6c757d; font-size: 0.95rem;">لا يوجد</div>'

                    st.markdown(f"""
                        <div class="report-card" style="border-right-color: #007bff;">
                            <div class="report-title">✨ الأوبشنال (Optional)</div>
                            {opt_inner_html}
                        </div>
                    """, unsafe_allow_html=True)

                    shop_raw = req_row.get('Shops Details', req_row.get('Shop Names', ''))
                    shop_items = parse_items_smart(shop_raw)
                    shop_inner_html = ""
                    if shop_items:
                        for item in shop_items:
                            clean_item_text = item.split("[IMG:")[0].strip()
                            shop_inner_html += f'<div class="sub-item-card" style="border-left-color: #ffc107; color: #856404;">🛍️ {clean_item_text}</div>'
                    else:
                        shop_inner_html = '<div class="report-value" style="color: #6c757d; font-size: 0.95rem;">لا يوجد</div>'

                    st.markdown(f"""
                        <div class="report-card" style="border-right-color: #ffc107;">
                            <div class="report-title">🛍️ تفاصيل المحلات</div>
                            {shop_inner_html}
                        </div>
                    """, unsafe_allow_html=True)

                    if pd.notna(req_row.get('Other Shops', '')) and str(req_row.get('Other Shops', '')).strip() != "":
                        st.markdown(f"""
                            <div class="report-card" style="border-right-color: #17a2b8;">
                                <div class="report-title">🏪 محلات خارجية</div>
                                <div class="report-value">{req_row.get('Other Shops', '')}</div>
                            </div>
                        """, unsafe_allow_html=True)

                    st.markdown("---")
                    st.markdown("#### صور فواتير الغداء:")
                    l_paths = req_row.get('Lunch Receipt', '')
                    if pd.notna(l_paths) and str(l_paths).strip() != "":
                        l_list = str(l_paths).split(",")
                        l_cols = st.columns(min(len(l_list), 3))
                        for idx, p in enumerate(l_list):
                            if os.path.exists(p):
                                with l_cols[idx % 3]:
                                    st.image(p, caption=f"صورة فاتورة الغداء رقم {idx+1}", width=220)
                    else:
                        st.info("لا توجد صور لفواتير الغداء.")

                    st.markdown("---")
                    s_paths = req_row.get('Shop Images', '')
                    st.markdown("#### صور فواتير المحلات:")
                    if pd.notna(s_paths) and str(s_paths).strip() != "":
                        paths_list = str(s_paths).split(",")
                        s_cols = st.columns(min(len(paths_list), 3))
                        for idx, p in enumerate(paths_list):
                            if os.path.exists(p):
                                with s_cols[idx % 3]:
                                    st.image(p, caption=f"صورة محلات رقم {idx+1}", width=220)
                    else:
                        st.info("لا توجد صور لفواتير المحلات.")

                st.markdown("---")
                st.markdown("### اتخاذ القرار بشأن الطلب:")
                
                col_btn1, col_btn2 = st.columns(2)
                
                with col_btn1:
                    if st.button("✅ تم الأرشفة", type="primary", use_container_width=True):
                        archive_entry = req_row.to_dict()
                        save_to_file(ARCHIVE_FILE, archive_entry)
                        
                        sub_df = sub_df.drop(req_idx).reset_index(drop=True)
                        overwrite_data(SUBMISSIONS_FILE, sub_df)
                        
                        st.session_state.viewing_file = None
                        st.session_state.show_liquidation_cards = False
                        st.success("✅ تم نقل الطلب للأرشيف بنجاح!")
                        st.rerun()

                with col_btn2:
                    if st.button("🔄 متابعة", use_container_width=True):
                        st.session_state.viewing_file = None
                        st.session_state.show_liquidation_cards = False
                        st.rerun()
            else:
                st.session_state.viewing_file = None
                st.rerun()

        else:
            if not sub_df.empty:
                st.markdown("### 🔍 فلترة وعرض تصفيات المرشدين حسب باسم المرشد")
                
                unique_accs_in_subs = sub_df['Account'].dropna().unique().tolist()
                guide_name_options_map = {}
                for acc in unique_accs_in_subs:
                    clean_acc = clean_acc_number(acc)
                    g_name = get_guide_name_by_account(clean_acc)
                    guide_name_options_map[g_name] = clean_acc

                guide_names_list = sorted(list(guide_name_options_map.keys()))

                selected_guide_filter = st.selectbox(
                    "اختر اسم المرشد لعرض جميع تصفياته وسجلاته",
                    options=["الكل (جميع المرشدين)"] + guide_names_list
                )

                if selected_guide_filter != "الكل (جميع المرشدين)":
                    target_acc = guide_name_options_map.get(selected_guide_filter)
                    filtered_sub_df = sub_df[sub_df['Account'].astype(str) == str(target_acc)]
                    st.info(f"عرض التصفيات الخاصة بالمرشد: **{selected_guide_filter}** (رقم الحساب: {target_acc}) - عدد الطلبات: {len(filtered_sub_df)}")
                else:
                    filtered_sub_df = sub_df

                st.markdown("### الطلبات الواردة")

                for idx, row in filtered_sub_df.iterrows():
                    r_acc = row.get('Account', '')
                    r_gname = get_guide_name_by_account(r_acc)
                    st.markdown(f"""
                        <div class="record-card">
                            <div class="card-header-row">
                                <span class="card-id">#{idx+1}</span>
                                <span class="card-file">الفايل: {row.get('File No', '')}</span>
                            </div>
                            <div class="card-body-row">
                                <div class="card-guide">رقم الحساب: {r_acc} | اسم المرشد: {r_gname}</div>
                                <div class="card-time">التاريخ: {row.get('Timestamp', '')}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    col_actions = st.columns([3, 1, 1, 1])
                    with col_actions[1]:
                        if st.button("عرض", key=f"view_btn_{idx}", type="primary"):
                            st.session_state.viewing_file = idx
                            st.session_state.show_liquidation_cards = False
                            st.rerun()
                    with col_actions[2]:
                        if st.button("بدء التصفية", key=f"start_liq_list_btn_{idx}", type="primary"):
                            st.session_state.viewing_file = idx
                            st.session_state.show_liquidation_cards = True
                            st.rerun()
                    with col_actions[3]:
                        if st.button("🗑️ حذف", key=f"del_sub_btn_{idx}", type="primary"):
                            st.session_state.confirming_del_sub = idx
                            st.rerun()

                    if st.session_state.confirming_del_sub == idx:
                        st.warning(f"⚠️ تأكيد حذف طلب الفايل رقم ({row.get('File No', '')})؟")
                        c_col1, c_col2 = st.columns(2)
                        with c_col1:
                            if st.button("✔️ تأكيد الحذف النهائي", key=f"confirm_del_sub_{idx}", type="primary"):
                                sub_df = sub_df.drop(idx).reset_index(drop=True)
                                overwrite_data(SUBMISSIONS_FILE, sub_df)
                                st.session_state.confirming_del_sub = None
                                st.success("تم الحذف بنجاح.")
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
                    if st.button("💾 حفظ التعديل", type="primary"):
                        st.session_state.confirming_edit_guide = {
                            "name": selected_guide_to_edit,
                            "new_acc": clean_acc_number(new_acc_input)
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
                        st.error("⚠️ يرجى كتابة الرقم الجديد أولاً!")
                        if st.button("❌ رجوع", type="primary"):
                            st.session_state.confirming_edit_guide = None
                            st.rerun()
                    else:
                        st.warning(f"⚠️ تأكيد تعديل رقم المرشد (**{g_to_edit}**) إلى: **{n_acc}**")
                        ec1, ec2 = st.columns(2)
                        with ec1:
                            if st.button("✔️ تأكيد وحفظ التعديل", type="primary"):
                                guides_df.loc[guides_df[name_column].astype(str) == str(g_to_edit), acc_column] = str(n_acc).strip()
                                guides_df.to_excel(GUIDES_FILE, index=False)
                                st.session_state.confirming_edit_guide = None
                                st.session_state.clear_edit_input = True
                                st.success("✅ تم التعديل بنجاح!")
                                st.rerun()
                        with ec2:
                            if st.button("❌ إلغاء", type="primary"):
                                st.session_state.confirming_edit_guide = None
                                st.rerun()

                if st.session_state.confirming_del_guide is not None:
                    g_to_del = st.session_state.confirming_del_guide["name"]
                    st.warning(f"⚠️ تأكيد حذف المرشد (**{g_to_del}**) نهائياً من قاعدة البيانات؟")
                    dc1, dc2 = st.columns(2)
                    with dc1:
                        if st.button("✔️ تأكيد الحذف النهائي للمرشد", type="primary"):
                            guides_df = guides_df[guides_df[name_column].astype(str) != str(g_to_del)].reset_index(drop=True)
                            guides_df.to_excel(GUIDES_FILE, index=False)
                            st.session_state.confirming_del_guide = None
                            st.success("✅ تم حذف المرشد بنجاح!")
                            st.rerun()
                    with dc2:
                        if st.button("❌ إلغاء الحذف", type="primary"):
                            st.session_state.confirming_del_guide = None
                            st.rerun()

            with col_section_right:
                st.markdown("#### إضافة مرشد جديد:")
                if st.session_state.clear_add_inputs:
                    st.session_state.clear_add_inputs = False
                    st.session_state.new_guide_name_input = ""
                    st.session_state.new_guide_acc_input = ""

                new_g_name = st.text_input("اسم المرشد الجديد", key="new_guide_name_input", value="")
                new_g_acc = st.text_input("رقم الحساب الجديد", key="new_guide_acc_input", value="")

                if st.button("➕ إضافة المرشد للقاعدة", type="primary"):
                    st.session_state.confirming_add_guide = {
                        "name": new_g_name,
                        "acc": clean_acc_number(new_g_acc)
                    }
                    st.rerun()

                if st.session_state.confirming_add_guide is not None:
                    add_g_name = st.session_state.confirming_add_guide["name"]
                    add_g_acc = st.session_state.confirming_add_guide["acc"]

                    if not add_g_name.strip() or not add_g_acc.strip():
                        st.error("⚠️ يرجى إدخال (اسم المرشد) و(الرقم) بشكل كامل!")
                        if st.button("❌ رجوع للقاعدة", type="primary"):
                            st.session_state.confirming_add_guide = None
                            st.rerun()
                    else:
                        st.warning(f"⚠️ تأكيد إضافة المرشد (**{add_g_name}**) برقم (**{add_g_acc}**)؟")
                        ac1, ac2 = st.columns(2)
                        with ac1:
                            if st.button("✔️ تأكيد وإضافة نهائية", type="primary"):
                                new_row = pd.DataFrame({
                                    name_column: [add_g_name],
                                    acc_column: [str(add_g_acc).strip()]
                                })
                                guides_df = pd.concat([guides_df, new_row], ignore_index=True)
                                guides_df.to_excel(GUIDES_FILE, index=False)
                                st.session_state.confirming_add_guide = None
                                st.session_state.clear_add_inputs = True
                                st.success("✅ تمت إضافة المرشد بنجاح!")
                                st.rerun()
                        with ac2:
                            if st.button("❌ إلغاء الإضافة", type="primary"):
                                st.session_state.confirming_add_guide = None
                                st.rerun()
    else:
        if password != "":
            st.error("❌ كلمة المرور غير صحيحة!")

elif page == "الأرشيف":
    st.title("📁 أرشيف التصفيات المنتهية")
    st.markdown("---")

    password_arch = st.text_input("أدخل كلمة المرور لعرض الأرشيف", type="password", key="arch_pass")

    if password_arch == "159753":
        st.success("تم تسجيل الدخول للأرشيف بنجاح.")
        archive_df = load_data(ARCHIVE_FILE)

        if "viewing_archive_file" not in st.session_state:
            st.session_state.viewing_archive_file = None
        if "confirming_del_archive" not in st.session_state:
            st.session_state.confirming_del_archive = None

        if st.session_state.viewing_archive_file is not None:
            req_idx = st.session_state.viewing_archive_file
            if req_idx in archive_df.index:
                req_row = archive_df.loc[req_idx]
                
                if st.button("⬅️ رجوع إلى قائمة الأرشيف", key="back_to_arch_list"):
                    st.session_state.viewing_archive_file = None
                    st.session_state.show_archive_liquidation_cards = False
                    st.rerun()

                r_acc = req_row.get('Account', '')
                r_gname = get_guide_name_by_account(r_acc)
                st.markdown(f"### 📄 تفاصيل الأرشيف للفايل: {req_row.get('File No', '')}")
                st.markdown(f"**التاريخ:** {req_row.get('Timestamp', '')} | **رقم الحساب:** {r_acc} | **اسم المرشد:** {r_gname}")
                st.markdown("---")

                if st.button("🚀 بدء التصفية (عرض تفاصيل الحسابات والكروت)", type="primary", key="start_arch_liquidation_btn"):
                    st.session_state.show_archive_liquidation_cards = True
                
                if st.session_state.get("show_archive_liquidation_cards", False):
                    st.markdown("---")
                    st.markdown("## 🧮 شاشة التصفية الذكية والكروت الحسابية (الأرشيف)")
                    
                    def parse_val(val_str):
                        try:
                            return float(str(val_str).split()[0])
                        except:
                            try:
                                return float(val_str)
                            except:
                                return 0.0

                    default_guide_name = r_gname
                    default_file_no = req_row.get('File No', '')
                    default_park = float(req_row.get('Park', 0.0))
                    default_tip = float(req_row.get('Tip', 0.0))
                    default_lunch = float(req_row.get('Lunch', 0.0))
                    
                    tkt_raw = str(req_row.get('Tickets', '0'))
                    default_tickets = parse_val(tkt_raw.split('-')[0]) if '-' in tkt_raw else parse_val(tkt_raw)
                    
                    advances_val = float(req_row.get('Advances', 0.0))
                    collection_raw = str(req_row.get('Collection', '0'))
                    default_collection_str = str(parse_val(collection_raw))

                    opt_raw_str = str(req_row.get('Option', ''))
                    default_opt_collection = 0.0
                    parsed_opts = parse_items_smart(opt_raw_str)
                    for opt_item in parsed_opts:
                        import re
                        numbers_found = re.findall(r"[-+]?\d*\.\d+|\d+", opt_item)
                        if numbers_found:
                            default_opt_collection += float(numbers_found[0])
                    default_opt_collection_str = str(default_opt_collection)

                    st.markdown("### 📋 كروت البيانات الأساسية")
                    c_k1, c_k2, c_k3, c_k4 = st.columns(4)
                    with c_k1:
                        card_guide_name = st.text_input("اسم المرشد", value=default_guide_name, key=f"arch_lk_gname_{req_idx}")
                    with c_k2:
                        card_file_no = st.text_input("رقم الفايل", value=default_file_no, key=f"arch_lk_fno_{req_idx}")
                    with c_k3:
                        card_guidance_val = st.number_input("قيمة الارشاد", min_value=0.0, value=0.0, step=10.0, key=f"arch_lk_guidance_{req_idx}")
                    with c_k4:
                        card_park = st.number_input("باركات", min_value=0.0, value=default_park, step=10.0, key=f"arch_lk_park_{req_idx}")

                    c_k5, c_k6, c_k7, c_k8 = st.columns(4)
                    with c_k5:
                        card_tip = st.number_input("إكراميات", min_value=0.0, value=default_tip, step=10.0, key=f"arch_lk_tip_{req_idx}")
                    with c_k6:
                        card_lunch = st.number_input("غداء", min_value=0.0, value=default_lunch, step=10.0, key=f"arch_lk_lunch_{req_idx}")
                    with c_k7:
                        card_tickets = st.number_input("تذاكر", min_value=0.0, value=default_tickets, step=10.0, key=f"arch_lk_tickets_{req_idx}")
                    with c_k8:
                        card_guide_commission = st.number_input("عمولة المرشد", min_value=0.0, value=0.0, step=10.0, key=f"arch_lk_guide_comm_{req_idx}")

                    st.markdown("---")
                    total_revenue = card_guidance_val + card_park + card_tip + card_lunch + card_tickets + card_guide_commission

                    st.markdown("### 💰 كروت العهد والتحصيلات")
                    cc_col1, cc_col2, cc_col3 = st.columns(3)
                    with cc_col1:
                        card_advances = st.number_input("عهدة", min_value=0.0, value=advances_val, step=10.0, key=f"arch_lk_adv_{req_idx}")
                    with cc_col2:
                        collec_expr = st.text_input("تحصيلات", value=default_collection_str, key=f"arch_lk_collec_{req_idx}")
                        card_collections = evaluate_expression(collec_expr)
                    with cc_col3:
                        opt_collec_expr = st.text_input("تحصيلات الأوبشنال", value=default_opt_collection_str, key=f"arch_lk_opt_collec_{req_idx}")
                        card_opt_collections = evaluate_expression(opt_collec_expr)

                    total_dues = card_advances + card_collections + card_opt_collections
                    net_balance = total_revenue - total_dues

                    st.markdown("---")
                    st.markdown("### 📊 الملخص النهائي للكروت الحسابية")
                    res_c1, res_c2, res_c3 = st.columns(3)
                    with res_c1:
                        st.metric(label="📈 إجمالي الإيراد", value=f"{total_revenue:,.2f}")
                    with res_c2:
                        st.metric(label="📉 إجمالي المستحقات", value=f"{total_dues:,.2f}")
                    with res_c3:
                        st.metric(label="💎 الصافي النهائي", value=f"{net_balance:,.2f}", delta=f"{net_balance:,.2f}")

                st.markdown("---")

                st.markdown("#### صور أمر الشغل:")
                wo_paths = req_row.get('Work Order Images', '')
                if pd.notna(wo_paths) and str(wo_paths).strip() != "":
                    wo_list = str(wo_paths).split(",")
                    wo_cols = st.columns(min(len(wo_list), 3))
                    for idx, p in enumerate(wo_list):
                        if os.path.exists(p):
                            with wo_cols[idx % 3]:
                                st.image(p, caption=f"صورة أمر الشغل رقم {idx+1}", width=220)
                else:
                    st.info("لا توجد صور لأمر الشغل.")

                st.markdown("---")
                
                st.markdown("""
                    <style>
                    .report-card {
                        background-color: #f8f9fa;
                        border: 1px solid #e9ecef;
                        border-right: 4px solid #28a745;
                        padding: 15px;
                        border-radius: 8px;
                        margin-bottom: 12px;
                    }
                    .report-title {
                        font-weight: bold;
                        color: #1b5e20;
                        margin-bottom: 5px;
                        font-size: 1.05rem;
                    }
                    .report-value {
                        color: #333333;
                        font-size: 1.1rem;
                        font-weight: 500;
                    }
                    .sub-item-card {
                        background-color: #ffffff;
                        border: 1px solid #d4edda;
                        border-left: 4px solid #28a745;
                        padding: 8px 12px;
                        border-radius: 6px;
                        margin-top: 6px;
                        font-size: 1.05rem;
                        color: #155724;
                        font-weight: 600;
                    }
                    </style>
                """, unsafe_allow_html=True)

                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.markdown(f"""
                        <div class="report-card">
                            <div class="report-title">💰 العهد (Advances)</div>
                            <div class="report-value">{req_row.get('Advances', 0)}</div>
                        </div>
                    """, unsafe_allow_html=True)
                with col_m2:
                    st.markdown(f"""
                        <div class="report-card">
                            <div class="report-title">📥 التحصيل (Collection)</div>
                            <div class="report-value">{req_row.get('Collection', 0)}</div>
                        </div>
                    """, unsafe_allow_html=True)
                with col_m3:
                    st.markdown(f"""
                        <div class="report-card">
                            <div class="report-title">🎁 إكرامية (Tip)</div>
                            <div class="report-value">{req_row.get('Tip', 0)}</div>
                        </div>
                    """, unsafe_allow_html=True)

                col_m4, col_m5, col_m6 = st.columns(3)
                with col_m4:
                    st.markdown(f"""
                        <div class="report-card">
                            <div class="report-title">🅿️ بارك (Park)</div>
                            <div class="report-value">{req_row.get('Park', 0)}</div>
                        </div>
                    """, unsafe_allow_html=True)
                with col_m5:
                    st.markdown(f"""
                        <div class="report-card">
                            <div class="report-title">🍽️ غداء (Lunch)</div>
                            <div class="report-value">{req_row.get('Lunch', 0)}</div>
                        </div>
                    """, unsafe_allow_html=True)
                with col_m6:
                    st.markdown(f"""
                        <div class="report-card">
                            <div class="report-title">🎟️ التذاكر (Tickets)</div>
                            <div class="report-value">{req_row.get('Tickets', 'لا يوجد')}</div>
                        </div>
                    """, unsafe_allow_html=True)

                opt_items = parse_items_smart(req_row.get('Option', ''))
                opt_inner_html = ""
                if opt_items:
                    for item in opt_items:
                        opt_inner_html += f'<div class="sub-item-card">✨ {item}</div>'
                else:
                    opt_inner_html = '<div class="report-value" style="color: #6c757d; font-size: 0.95rem;">لا يوجد</div>'

                st.markdown(f"""
                    <div class="report-card" style="border-right-color: #007bff;">
                        <div class="report-title">✨ الأوبشنال (Optional)</div>
                        {opt_inner_html}
                    </div>
                """, unsafe_allow_html=True)

                shop_raw = req_row.get('Shops Details', req_row.get('Shop Names', ''))
                shop_items = parse_items_smart(shop_raw)
                shop_inner_html = ""
                if shop_items:
                    for item in shop_items:
                        clean_item_text = item.split("[IMG:")[0].strip()
                        shop_inner_html += f'<div class="sub-item-card" style="border-left-color: #ffc107; color: #856404;">🛍️ {clean_item_text}</div>'
                else:
                    shop_inner_html = '<div class="report-value" style="color: #6c757d; font-size: 0.95rem;">لا يوجد</div>'

                st.markdown(f"""
                    <div class="report-card" style="border-right-color: #ffc107;">
                        <div class="report-title">🛍️ تفاصيل المحلات</div>
                        {shop_inner_html}
                    </div>
                """, unsafe_allow_html=True)

                if pd.notna(req_row.get('Other Shops', '')) and str(req_row.get('Other Shops', '')).strip() != "":
                    st.markdown(f"""
                        <div class="report-card" style="border-right-color: #17a2b8;">
                            <div class="report-title">🏪 محلات خارجية</div>
                            <div class="report-value">{req_row.get('Other Shops', '')}</div>
                        </div>
                    """, unsafe_allow_html=True)

                st.markdown("---")
                st.markdown("#### صور فواتير الغداء:")
                l_paths = req_row.get('Lunch Receipt', '')
                if pd.notna(l_paths) and str(l_paths).strip() != "":
                    l_list = str(l_paths).split(",")
                    l_cols = st.columns(min(len(l_list), 3))
                    for idx, p in enumerate(l_list):
                        if os.path.exists(p):
                            with l_cols[idx % 3]:
                                st.image(p, caption=f"صورة فاتورة الغداء رقم {idx+1}", width=220)
                else:
                    st.info("لا توجد صور لفواتير الغداء.")

                st.markdown("---")
                s_paths = req_row.get('Shop Images', '')
                st.markdown("#### صور فواتير المحلات:")
                if pd.notna(s_paths) and str(s_paths).strip() != "":
                    paths_list = str(s_paths).split(",")
                    s_cols = st.columns(min(len(paths_list), 3))
                    for idx, p in enumerate(paths_list):
                        if os.path.exists(p):
                            with s_cols[idx % 3]:
                                st.image(p, caption=f"صورة محلات رقم {idx+1}", width=220)
            else:
                st.session_state.viewing_archive_file = None
                st.rerun()
        else:
            if not archive_df.empty:
                st.markdown("### 🛍️ فلترة الأرشيف حسب المحل (معرفة المبيعات والفواتير للمرشدين)")
                
                selected_shop_filter = st.selectbox(
                    "اختر المحل للفلترة",
                    options=["الكل (جميع المحلات)"] + SHOPS_LIST
                )

                if selected_shop_filter != "الكل (جميع المحلات)":
                    matched_arch_df = archive_df[
                        archive_df['Shops Details'].astype(str).str.contains(selected_shop_filter, na=False) | 
                        archive_df['Shop Names'].astype(str).str.contains(selected_shop_filter, na=False) |
                        archive_df['Other Shops'].astype(str).str.contains(selected_shop_filter, na=False)
                    ]
                    
                    st.info(f"نتائج البحث للمحل: **{selected_shop_filter}** (عدد العمليات: {len(matched_arch_df)})")
                    
                    if not matched_arch_df.empty:
                        for idx, row in matched_arch_df.iterrows():
                            r_acc = row.get('Account', '')
                            r_gname = get_guide_name_by_account(r_acc)
                            shop_detail_raw = str(row.get('Shops Details', ''))
                            shop_items_list = parse_items_smart(shop_detail_raw)
                            
                            matched_entries_for_shop = []
                            for s_item in shop_items_list:
                                if selected_shop_filter in s_item:
                                    target_shop_text = "لا توجد تفاصيل مسجلة"
                                    specific_img_paths = []
                                    if "[IMG:" in s_item:
                                        parts_img = s_item.split("[IMG:")
                                        target_shop_text = parts_img[0].strip()
                                        img_part = parts_img[1].replace("]", "").strip()
                                        if img_part:
                                            specific_img_paths = [p.strip() for p in img_part.split(",") if p.strip()]
                                    else:
                                        target_shop_text = s_item.strip()
                                    matched_entries_for_shop.append({
                                        "text": target_shop_text,
                                        "images": specific_img_paths
                                    })
                            
                            other_shops_val_str = str(row.get('Other Shops', ''))
                            if selected_shop_filter in other_shops_val_str and not matched_entries_for_shop:
                                matched_entries_for_shop.append({
                                    "text": other_shops_val_str,
                                    "images": []
                                })

                            st.markdown(f"""
                                <div class="record-card" style="margin-bottom: 6px;">
                                    <div class="card-header-row">
                                        <span class="card-id">#{idx+1}</span>
                                        <span class="card-file">الفايل: {row.get('File No', '')}</span>
                                    </div>
                                    <div class="card-body-row">
                                        <div class="card-guide">رقم الحساب: {r_acc} | اسم المرشد: {r_gname}</div>
                                        <div class="card-time">التاريخ: {row.get('Timestamp', '')}</div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)

                            if matched_entries_for_shop:
                                entry_cols = st.columns(min(len(matched_entries_for_shop), 3))
                                for col_idx, entry in enumerate(matched_entries_for_shop):
                                    with entry_cols[col_idx % 3]:
                                        st.markdown(f"""
                                            <style>
                                            .shop-inv-card {
                                                background-color: #fdfefe;
                                                border: 1px solid #d4edda;
                                                border-right: 5px solid #28a745;
                                                padding: 10px 14px;
                                                border-radius: 8px;
                                                margin-bottom: 8px;
                                                box-shadow: 0 1px 3px rgba(0,0,0,0.04);
                                            }
                                            </style>
                                            <div class="shop-inv-card">
                                                <div style="font-size: 0.95rem; font-weight: bold; color: #333333;">
                                                    🛍️ الفاتورة: <span style="color: #28a745;">{entry['text']}</span>
                                                </div>
                                            </div>
                                        """, unsafe_allow_html=True)

                                        if entry['images']:
                                            st.markdown("<div style='font-size: 0.9rem;'>📷 <strong>صورة الفاتورة:</strong></div>", unsafe_allow_html=True)
                                            for i, p in enumerate(entry['images']):
                                                if os.path.exists(p):
                                                    st.image(p, caption=f"صورة الفاتورة {i+1}", width=200)
                                        else:
                                            st.markdown("<div style='color: #6c757d; font-size: 0.85rem;'>ℹ️ لم يتم رفع صورة.</div>", unsafe_allow_html=True)

                            st.markdown("---")
                    else:
                        st.warning("⚠️ لا توجد أي عمليات تسجيل أو مبيعات لهذا المحل في الأرشيف حتى الآن.")
                else:
                    st.markdown("### 🔍 فلترة وعرض الأرشيف حسب اسم المرشد")
                    
                    unique_accs_in_arch = archive_df['Account'].dropna().unique().tolist()
                    guide_name_options_arch_map = {}
                    for acc in unique_accs_in_arch:
                        clean_acc = clean_acc_number(acc)
                        g_name = get_guide_name_by_account(clean_acc)
                        guide_name_options_arch_map[g_name] = clean_acc

                    guide_names_arch_list = sorted(list(guide_name_options_arch_map.keys()))

                    selected_guide_arch_filter = st.selectbox(
                        "اختر اسم المرشد لعرض جميع أرشيفه",
                        options=["الكل (جميع المرشدين)"] + guide_names_arch_list,
                        key="arch_guide_filter"
                    )

                    if selected_guide_arch_filter != "الكل (جميع المرشدين)":
                        target_arch_acc = guide_name_options_arch_map.get(selected_guide_arch_filter)
                        filtered_arch_df = archive_df[archive_df['Account'].astype(str) == str(target_arch_acc)]
                        st.info(f"عرض الأرشيف الخاص بالمرشد: **{selected_guide_arch_filter}** (رقم الحساب: {target_arch_acc}) - عدد الطلبات: {len(filtered_arch_df)}")
                    else:
                        filtered_arch_df = archive_df

                    st.markdown(f"إجمالي الطلبات المؤرشفة: {len(archive_df)}")
                    st.markdown("### سجلات الأرشيف")

                    for idx, row in filtered_arch_df.iterrows():
                        r_acc = row.get('Account', '')
                        r_gname = get_guide_name_by_account(r_acc)
                        st.markdown(f"""
                            <div class="record-card">
                                <div class="card-header-row">
                                    <span class="card-id">#{idx+1}</span>
                                    <span class="card-file">الفايل: {row.get('File No', '')}</span>
                                </div>
                                <div class="card-body-row">
                                    <div class="card-guide">رقم الحساب: {r_acc} | اسم المرشد: {r_gname}</div>
                                    <div class="card-time">التاريخ: {row.get('Timestamp', '')}</div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # تم إضافة زر "تم" / "تم النقل" بجانب زر التصفية
                        cols = st.columns([1, 1, 1, 1, 1])
                        with cols[1]:
                            if st.button("عرض", key=f"view_arch_btn_{idx}", type="primary"):
                                st.session_state.viewing_archive_file = idx
                                st.session_state.show_archive_liquidation_cards = False
                                st.rerun()
                        with cols[2]:
                            if st.button("بدء التصفية", key=f"start_arch_liq_list_btn_{idx}", type="primary"):
                                st.session_state.viewing_archive_file = idx
                                st.session_state.show_archive_liquidation_cards = True
                                st.rerun()
                        with cols[3]:
                            transferred_key = f"transferred_status_{idx}"
                            if transferred_key not in st.session_state:
                                st.session_state[transferred_key] = False
                            
                            btn_label = "تم النقل" if st.session_state[transferred_key] else "تم"
                            if st.button(btn_label, key=f"btn_done_trans_{idx}", type="primary"):
                                st.session_state[transferred_key] = True
                                
                                # نقل التصفية المؤرشفة إلى سجلات المرشد (GUIDE_ARCHIVE_FILE)
                                guide_arch_data = row.to_dict()
                                save_to_file(GUIDE_ARCHIVE_FILE, guide_arch_data)
                                st.success("✅ تمت تصفية ونقل بيانات الفايل لتظهر في صفحة سجلات المرشد بنجاح!")
                                st.rerun()
                        with cols[4]:
                            if st.button("🗑️ حذف", key=f"del_arch_btn_{idx}", type="primary"):
                                st.session_state.confirming_del_archive = idx
                                st.rerun()

                        if st.session_state.confirming_del_archive == idx:
                            st.warning(f"⚠️ تأكيد حذف طلب الأرشيف للفايل رقم ({row.get('File No', '')})؟")
                            ac_col1, ac_col2 = st.columns(2)
                            with ac_col1:
                                if st.button("✔️ تأكيد الحذف النهائي", key=f"confirm_del_arch_{idx}", type="primary"):
                                    archive_df = archive_df.drop(idx).reset_index(drop=True)
                                    overwrite_data(ARCHIVE_FILE, archive_df)
                                    st.session_state.confirming_del_archive = None
                                    st.success("تم الحذف من الأرشيف بنجاح.")
                                    st.rerun()
                            with ac_col2:
                                if st.button("❌ رجوع (إلغاء)", key=f"cancel_del_arch_{idx}", type="primary"):
                                    st.session_state.confirming_del_archive = None
                                    st.rerun()

                        st.markdown("---")

                if st.button("🗑️ تفريغ الأرشيف بالكامل", type="primary"):
                    if os.path.exists(ARCHIVE_FILE):
                        os.remove(ARCHIVE_FILE)
                    st.success("✅ تم تفريغ الأرشيف بالكامل!")
                    st.rerun()
            else:
                st.info("لا توجد طلبات في الأرشيف حالياً.")
    else:
        if password_arch != "":
            st.error("❌ كلمة المرور غير صحيحة!")
