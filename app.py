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

def get_current_logo():
    fixed_logo_path = "sun_2.png"
    if os.path.exists(fixed_logo_path):
        return fixed_logo_path
    return None

def load_data(file_path):
    if os.path.exists(file_path):
        try:
            df = pd.read_excel(file_path)
            if 'Guide Name' not in df.columns:
                df['Guide Name'] = 'غير معروف'
            if 'Timestamp' not in df.columns:
                df['Timestamp'] = 'غير محدد'
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

# تنسيق CSS للسايدبار والأزرار
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
    </style>
""", unsafe_allow_html=True)

try:
    guides_df = pd.read_excel(GUIDES_FILE)
except:
    guides_df = pd.DataFrame({
        "Guide Name": ["أحمد", "محمود"],
        "Account Number": ["1805000493514500022", "1805000493514500033"]
    })
    guides_df.to_excel(GUIDES_FILE, index=False)

name_column = guides_df.columns[0] if len(guides_df.columns) > 0 else "Guide Name"
acc_column = guides_df.columns[1] if len(guides_df.columns) > 1 else guides_df.columns[0]

SHOPS_LIST = [
    "وجية بردى", "اخناتون سجاد", "مينا للبرديات", "رويال سجاد", "اولد كايرو",
    "رويال للعطور", "خان الحلو للقطن", "فلور قطن", "طيبة للقطن", "فيلة بازار",
    "جولدن بيرد", "مملوك", "ريحانة توابل", "كنور توابل", "قصر العطور", "لازوريت"
]

current_subs_df = load_data(SUBMISSIONS_FILE)
pending_count = len(current_subs_df)

col_spacer, col_badge = [st.columns([4, 1])[0], st.columns([4, 1])[1]] if hasattr(st, 'columns') else (None, None)
with col_badge:
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
        ["نموذج تصفية المرشد", "إدارة التصفيات", "الأرشيف"],
        label_visibility="collapsed"
    )

if page == "نموذج تصفية المرشد":
    st.title("🧭 نموذج تصفية المرشدين")
    st.markdown("---")

    if "option_rows_count" not in st.session_state:
        st.session_state.option_rows_count = 1
    if "shop_rows_count" not in st.session_state:
        st.session_state.shop_rows_count = 1

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

        work_order_image = st.file_uploader("رفع صور أمر الشغل", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="work_order_imgs")

        st.markdown("---")
        st.subheader("التحصيل (Collection)")
        
        col_c1, col_c2 = st.columns([2, 1])
        with col_c1:
            collection_val = st.number_input("قيمة التحصيل", min_value=0.0, step=10.0)
        with col_c2:
            collection_curr = st.selectbox("عملة التحصيل", options=["جنية", "يورو", "دولار"])

        st.markdown("---")
        st.subheader("أوبشنال (Optional)")
        
        option_data_list = []
        for i in range(st.session_state.option_rows_count):
            st.markdown(f"**أوبشنال رقم ({i+1})**")
            col_opt1, col_opt2, col_opt3, col_opt4, col_opt5 = st.columns(5)
            with col_opt1:
                opt_type = st.text_input("نوع الأوبشنال", key=f"opt_type_{i}")
            with col_opt2:
                opt_val = st.number_input("قيمة الأوبشنال", min_value=0.0, step=10.0, key=f"opt_val_{i}")
            with col_opt3:
                opt_curr = st.selectbox("عملة الأوبشنال", options=["مصري", "دولار", "يورو"], key=f"opt_curr_{i}")
            with col_opt4:
                opt_pay = st.selectbox("طريقة الدفع", options=[None, "كاش", "لينك"], key=f"opt_pay_{i}")
            with col_opt5:
                cash_h = st.selectbox("المبلغ", options=[None, "مع المرشد", "مع السواق"], key=f"cash_h_{i}")
            
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

        lunch_images = st.file_uploader("رفع صور فواتير الغداء", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="lunch_imgs")

        st.markdown("---")
        st.subheader("فواتير ومحلات التسوق")
        
        shop_data_list = []
        for j in range(st.session_state.shop_rows_count):
            st.markdown(f"**المحل رقم ({j+1})**")
            col_s1, col_s2, col_s3, col_s4 = st.columns([2, 1, 1, 2])
            with col_s1:
                shop_name_choice = st.selectbox("اسم المحل", options=[None] + SHOPS_LIST, key=f"shop_name_{j}")
            with col_s2:
                shop_val = st.number_input("القيمة", min_value=0.0, step=10.0, key=f"shop_val_{j}")
            with col_s3:
                shop_curr = st.selectbox("العملة", options=["مصري", "يورو", "دولار"], key=f"shop_curr_{j}")
            with col_s4:
                shop_file_img = st.file_uploader("رفع فاتورة المحل", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key=f"shop_img_{j}")
            
            shop_data_list.append({
                "name": shop_name_choice, "value": shop_val, "curr": shop_curr, "images": shop_file_img
            })
            if j < st.session_state.shop_rows_count - 1:
                st.markdown("---")

        add_more_shop = st.form_submit_button("➕ إضافة محل")

        st.markdown("---")
        st.subheader("اسم المحل")
        
        col_oth1, col_oth2 = st.columns([2, 1])
        with col_oth1:
            other_shops = st.text_input("أدخل المحلات الأخرى هنا", label_visibility="collapsed")
        with col_oth2:
            other_shops_images = st.file_uploader("رفع فاتورة المحل", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="other_shops_imgs")

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
                o_val = st.session_state.get(f"opt_val_{i}", 0.0)
                p_val = st.session_state.get(f"opt_pay_{i}", None)
                c_h = st.session_state.get(f"cash_h_{i}", None)
                o_type = st.session_state.get(f"opt_type_{i}", "")
                if (o_val > 0 or o_type.strip()) and not p_val:
                    validation_pay_error = True
                    break
                if p_val == "كاش" and not c_h:
                    validation_error = True
                    break

            if not account_no:
                st.error("⚠️ عذراً، يجب اختيار (رقم الحساب) الخاص بك أولاً!")
            elif not file_no.strip():
                st.error("⚠️ عذراً، لا يمكن إرسال الطلب. يرجى إدخال (رقم الفايل) أولاً بشكل إلزامي!")
            elif validation_pay_error:
                st.error("⚠️ عذراً، نظراً لإدخال قيمة أو نوع في أحد الأوبشنالز، يجب اختيار (طريقة الدفع) [كاش / لينك] بشكل إلزامي!")
            elif validation_error:
                st.error("⚠️ عذراً، نظراً لاختيار طريقة الدفع (كاش)، يجب اختيار (المبلغ) [مع المرشد / مع السواق] بشكل إلزامي!")
            else:
                matched_guide = guides_df[guides_df[acc_column].astype(str) == str(account_no)]
                guide_name = matched_guide[name_column].values[0] if not matched_guide.empty else "غير معروف"
                
                current_time_str = datetime.now().strftime("%Y-%m-%d %I:%M %p")
                
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
                    s_name = st.session_state.get(f"shop_name_{j}", None)
                    s_val = st.session_state.get(f"shop_val_{j}", 0.0)
                    s_curr = st.session_state.get(f"shop_curr_{j}", "مصري")
                    s_imgs = st.session_state.get(f"shop_img_{j}", [])
                    
                    if s_imgs:
                        for img in s_imgs:
                            s_path = os.path.join(UPLOAD_DIR, f"shop_{time.time()}_{img.name}")
                            with open(s_path, "wb") as f:
                                f.write(img.getbuffer())
                            all_shop_paths.append(s_path)

                    if s_name:
                        shops_names_only.append(s_name)
                        shops_summary_list.append(f"{s_name}: {s_val} {s_curr}")

                all_shop_paths.extend(other_shops_paths)

                options_summary_list = []
                option_types_list = []
                for i in range(st.session_state.option_rows_count):
                    o_type = st.session_state.get(f"opt_type_{i}", "")
                    o_val = st.session_state.get(f"opt_val_{i}", 0.0)
                    o_curr = st.session_state.get(f"opt_curr_{i}", "مصري")
                    o_pay = st.session_state.get(f"opt_pay_{i}", None)
                    o_holder = st.session_state.get(f"cash_h_{i}", "")
                    
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
                    "Account": account_no,
                    "File No": file_no,
                    "Work Order Images": ",".join(work_order_paths) if work_order_paths else "",
                    "Advances": advances,
                    "Collection": f"{collection_val} {collection_curr}",
                    "Option Type": ", ".join(option_types_list),
                    "Option": " | ".join(options_summary_list),
                    "Tickets": f"{ticket_value} - {ticket_type}",
                    "Tip": tip,
                    "Park": park,
                    "Lunch": lunch,
                    "Lunch Receipt": ",".join(lunch_paths) if lunch_paths else "",
                    "Shop Names": ", ".join(shops_names_only),
                    "Other Shops": other_shops,
                    "Shops Details": " | ".join(shops_summary_list),
                    "Shop Images": ",".join(all_shop_paths) if all_shop_paths else ""
                }
                save_to_file(SUBMISSIONS_FILE, new_entry)
                
                st.session_state.option_rows_count = 1
                st.session_state.shop_rows_count = 1
                st.success("✅ تم إرسال الطلب للمدير بنجاح! جاهز لتسجيل تصفية جديدة...")
                st.rerun()

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
                    st.rerun()

                st.markdown(f"### 📄 تفاصيل تصفية الفايل: {req_row.get('File No', '')} (المرشد: {req_row.get('Guide Name', '')})")
                st.markdown(f"**التاريخ والوقت:** {req_row.get('Timestamp', '')} | **رقم الحساب:** {req_row.get('Account', '')}")
                st.markdown("---")

                st.markdown("#### صور أمر الشغل:")
                wo_paths = req_row.get('Work Order Images', '')
                if pd.notna(wo_paths) and str(wo_paths).strip() != "":
                    wo_list = str(wo_paths).split(",")
                    for idx, p in enumerate(wo_list):
                        if os.path.exists(p):
                            st.image(p, caption=f"صورة أمر الشغل رقم {idx+1}", use_container_width=True)
                else:
                    st.info("لا توجد صور لأمر الشغل.")

                st.markdown("---")
                st.write(f"**العهد (Advances):** {req_row.get('Advances', 0)}")
                st.write(f"**التحصيل (Collection):** {req_row.get('Collection', 0)}")
                st.write(f"**الأوبشنال (Optional):** {req_row.get('Option', '')}")
                st.write(f"**التذاكر (Tickets):** {req_row.get('Tickets', '')}")
                st.write(f"**إكرامية (Tip):** {req_row.get('Tip', 0)}")
                st.write(f"**بارك (Park):** {req_row.get('Park', 0)}")
                st.write(f"**غداء (Lunch):** {req_row.get('Lunch', 0)}")

                st.markdown("#### صور فواتير الغداء:")
                l_paths = req_row.get('Lunch Receipt', '')
                if pd.notna(l_paths) and str(l_paths).strip() != "":
                    l_list = str(l_paths).split(",")
                    for idx, p in enumerate(l_list):
                        if os.path.exists(p):
                            st.image(p, caption=f"صورة فاتورة الغداء رقم {idx+1}", use_container_width=True)
                else:
                    st.info("لا توجد صور لفواتير الغداء.")

                st.markdown("---")
                st.write(f"**تفاصيل المحلات:** {req_row.get('Shops Details', req_row.get('Shop Names', 'لا يوجد'))}")
                if pd.notna(req_row.get('Other Shops', '')) and str(req_row.get('Other Shops', '')).strip() != "":
                    st.write(f"**محلات أخري:** {req_row.get('Other Shops', '')}")

                s_paths = req_row.get('Shop Images', '')
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
                    if st.button("✅ تم (نقل للأرشيف)", type="primary", use_container_width=True):
                        archive_entry = req_row.to_dict()
                        save_to_file(ARCHIVE_FILE, archive_entry)
                        
                        sub_df = sub_df.drop(req_idx).reset_index(drop=True)
                        overwrite_data(SUBMISSIONS_FILE, sub_df)
                        
                        st.session_state.viewing_file = None
                        st.success("✅ تم نقل الطلب للأرشيف بنجاح!")
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
                
                all_guides_in_subs = sub_df['Guide Name'].dropna().unique().tolist()
                selected_guide_filter = st.selectbox(
                    "اختر اسم المرشد لعرض جميع تصفياته وسجلاته",
                    options=["الكل (جميع المرشدين)"] + all_guides_in_subs
                )

                if selected_guide_filter != "الكل (جميع المرشدين)":
                    filtered_sub_df = sub_df[sub_df['Guide Name'] == selected_guide_filter]
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
                        st.error("⚠️ يرجى كتابة رقم الحساب الجديد أولاً!")
                        if st.button("❌ رجوع", type="primary"):
                            st.session_state.confirming_edit_guide = None
                            st.rerun()
                    else:
                        st.warning(f"⚠️ تأكيد تعديل حساب المرشد (**{g_to_edit}**) إلى: **{n_acc}**")
                        ec1, ec2 = st.columns(2)
                        with ec1:
                            if st.button("✔️ تأكيد وحفظ التعديل", type="primary"):
                                guides_df.loc[guides_df[name_column].astype(str) == str(g_to_edit), acc_column] = n_acc
                                guides_df.to_excel(GUIDES_FILE, index=False)
                                st.session_state.confirming_edit_guide = None
                                st.session_state.clear_edit_input = True
                                st.success("✅ تم تعديل رقم الحساب بنجاح!")
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
                new_g_acc = st.text_input("رقم الحساب الجديد للمرشد", key="new_guide_acc_input", value="")

                if st.button("➕ إضافة المرشد للقاعدة", type="primary"):
                    st.session_state.confirming_add_guide = {
                        "name": new_g_name,
                        "acc": new_g_acc
                    }
                    st.rerun()

                if st.session_state.confirming_add_guide is not None:
                    add_g_name = st.session_state.confirming_add_guide["name"]
                    add_g_acc = st.session_state.confirming_add_guide["acc"]

                    if not add_g_name.strip() or not add_g_acc.strip():
                        st.error("⚠️ يرجى إدخال (اسم المرشد) و(رقم الحساب) بشكل كامل!")
                        if st.button("❌ رجوع للقاعدة", type="primary"):
                            st.session_state.confirming_add_guide = None
                            st.rerun()
                    else:
                        st.warning(f"⚠️ تأكيد إضافة المرشد (**{add_g_name}**) برقم حساب (**{add_g_acc}**)؟")
                        ac1, ac2 = st.columns(2)
                        with ac1:
                            if st.button("✔️ تأكيد وإضافة نهائية", type="primary"):
                                new_row = pd.DataFrame({
                                    name_column: [add_g_name],
                                    acc_column: [add_g_acc]
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
                    st.rerun()

                st.markdown(f"### 📄 تفاصيل الأرشيف للفايل: {req_row.get('File No', '')} (المرشد: {req_row.get('Guide Name', '')})")
                st.markdown(f"**التاريخ والوقت:** {req_row.get('Timestamp', '')} | **رقم الحساب:** {req_row.get('Account', '')}")
                st.markdown("---")

                st.markdown("#### صور أمر الشغل:")
                wo_paths = req_row.get('Work Order Images', '')
                if pd.notna(wo_paths) and str(wo_paths).strip() != "":
                    wo_list = str(wo_paths).split(",")
                    for idx, p in enumerate(wo_list):
                        if os.path.exists(p):
                            st.image(p, caption=f"صورة أمر الشغل رقم {idx+1}", use_container_width=True)
                else:
                    st.info("لا توجد صور لأمر الشغل.")

                st.markdown("---")
                st.write(f"**العهد (Advances):** {req_row.get('Advances', 0)}")
                st.write(f"**التحصيل (Collection):** {req_row.get('Collection', 0)}")
                st.write(f"**الأوبشنال (Optional):** {req_row.get('Option', '')}")
                st.write(f"**التذاكر (Tickets):** {req_row.get('Tickets', '')}")
                st.write(f"**إكرامية (Tip):** {req_row.get('Tip', 0)}")
                st.write(f"**بارك (Park):** {req_row.get('Park', 0)}")
                st.write(f"**غداء (Lunch):** {req_row.get('Lunch', 0)}")

                st.markdown("#### صور فواتير الغداء:")
                l_paths = req_row.get('Lunch Receipt', '')
                if pd.notna(l_paths) and str(l_paths).strip() != "":
                    l_list = str(l_paths).split(",")
                    for idx, p in enumerate(l_list):
                        if os.path.exists(p):
                            st.image(p, caption=f"صورة فاتورة الغداء رقم {idx+1}", use_container_width=True)
                else:
                    st.info("لا توجد صور لفواتير الغداء.")

                st.markdown("---")
                st.write(f"**تفاصيل المحلات:** {req_row.get('Shops Details', req_row.get('Shop Names', 'لا يوجد'))}")
                if pd.notna(req_row.get('Other Shops', '')) and str(req_row.get('Other Shops', '')).strip() != "":
                    st.write(f"**محلات أخري:** {req_row.get('Other Shops', '')}")

                s_paths = req_row.get('Shop Images', '')
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
                            st.markdown(f"#### 🏷️ فايل رقم: {row.get('File No', '')} | المرشد: **{row.get('Guide Name', '')}**")
                            col_info1, col_info2 = st.columns(2)
                            with col_info1:
                                st.write(f"**تاريخ التصفية:** {row.get('Timestamp', '')}")
                                st.write(f"**تفاصيل المحلات:** {row.get('Shops Details', row.get('Shop Names', 'لا يوجد'))}")
                                if pd.notna(row.get('Other Shops', '')) and str(row.get('Other Shops', '')).strip() != "":
                                    st.write(f"**محلات أخري:** {row.get('Other Shops', '')}")
                            with col_info2:
                                st.write(f"**التحصيل / القيمة:** {row.get('Collection', '0')}")
                                st.write(f"**الأوبشنال:** {row.get('Option', 'لا يوجد')}")
                            
                            s_paths = row.get('Shop Images', '')
                            if pd.notna(s_paths) and str(s_paths).strip() != "":
                                st.markdown("**📷 فواتير المحلات المرفوعة:**")
                                paths_list = str(s_paths).split(",")
                                img_cols = st.columns(min(len(paths_list), 3))
                                for i, p in enumerate(paths_list):
                                    if os.path.exists(p):
                                        with img_cols[i % 3]:
                                            st.image(p, caption=f"صورة الفاتورة {i+1}", use_container_width=True)
                            else:
                                st.info("لا توجد صور فواتير مرفوعة لهذا المحل.")
                            
                            st.markdown("---")
                    else:
                        st.warning("⚠️ لا توجد أي عمليات تسجيل أو مبيعات لهذا المحل في الأرشيف حتى الآن.")
                else:
                    st.markdown("### 🔍 فلترة وعرض الأرشيف حسب المرشد")
                    all_guides_in_arch = archive_df['Guide Name'].dropna().unique().tolist()
                    selected_guide_arch_filter = st.selectbox(
                        "اختر اسم المرشد لعرض جميع أرشيفه",
                        options=["الكل (جميع المرشدين)"] + all_guides_in_arch,
                        key="arch_guide_filter"
                    )

                    if selected_guide_arch_filter != "الكل (جميع المرشدين)":
                        filtered_arch_df = archive_df[archive_df['Guide Name'] == selected_guide_arch_filter]
                        st.info(f"عرض الأرشيف الخاص بالمرشد: **{selected_guide_arch_filter}** (عدد الطلبات: {len(filtered_arch_df)})")
                    else:
                        filtered_arch_df = archive_df

                    st.markdown(f"إجمالي الطلبات المؤرشفة: {len(archive_df)}")
                    st.markdown("### سجلات الأرشيف")

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
