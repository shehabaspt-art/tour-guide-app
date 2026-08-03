import os
import base64
from datetime import datetime
import time
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sun Pyramids Tours", page_icon="🧭", layout="wide")

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

SUBMISSIONS_FILE = "submissions.xlsx"
ARCHIVE_FILE = "archive.xlsx"
GUIDES_FILE = "guides.xlsx"

ADMIN_EMAIL = "shehab.a.spt@gmail.com"

def get_current_logo():
    fixed_logo_path = "sun_2.png"
    if os.path.exists(fixed_logo_path):
        return fixed_logo_path
    return None

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

current_logo_path = get_current_logo()
if current_logo_path:
    try:
        st.logo(current_logo_path)
    except:
        pass

def get_image_base64(path):
    if path and os.path.exists(path):
        with open(path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            ext = path.split(".")[-1].lower()
            if ext == "jpg" or ext == "jpeg":
                mime = "image/jpeg"
            elif ext == "png":
                mime = "image/png"
            elif ext == "svg":
                mime = "image/svg+xml"
            else:
                mime = "image/png"
            return f"data:{mime};base64,{encoded}"
    return ""

logo_base64 = get_image_base64(current_logo_path)

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

if new_order_arrived:
    st.markdown("""
    <script>
        document.title = "🚨 (طلب جديد!) Sun Pyramids Tours";
        var audio = new Audio('https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3');
        audio.play().catch(e => console.log("Audio play blocked"));
    </script>
    """, unsafe_allow_html=True)

# إدارة حالة إظهار أو إخفاء القائمة الجانبية عبر الجافاسكريبت المخصص للتحكم بـ Streamlit
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"

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
        background-color: #d8ebd8;
        border-left: 2px solid #c2e0c2;
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
    
    .sticky-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: #f8f9fa;
        z-index: 999999;
        padding: 8px 20px;
        border-bottom: 1px solid #e0e0e0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .block-container {
        padding-top: 5rem !important;
    }
    </style>
""", unsafe_allow_html=True)

logo_html = f'<img src="{logo_base64}" style="height: 42px; width: auto; max-width: 180px; object-fit: contain; filter: contrast(1.15) saturate(1.1);" />' if logo_base64 else '<span style="font-weight: bold; color: #1b5e20; font-size: 1.1rem;">Sun Pyramids</span>'

# زر جافاسكريبت لضغط زر الـ Sidebar الأصلي الخاص بـ Streamlit لضمان عمله بكل قوة
st.markdown(f"""
    <div class="sticky-header">
        <div style="display: flex; align-items: center; gap: 12px;">
            <button onclick="
                var btn = document.querySelector('[data-testid=\\'collapsedControl\\']') || parent.document.querySelector('[data-testid=\\'collapsedControl\\']');
                if(btn) {{ btn.click(); }}
                else {{
                    var toggleIcons = window.parent.document.getElementsByTagName('button');
                    for (let b of toggleIcons) {{
                        if (b.getAttribute('aria-label') && b.getAttribute('aria-label').includes('sidebar')) {{ b.click(); break; }}
                    }}
                }}
            " style="background-color: #1b5e20; color: white; border: none; padding: 6px 12px; border-radius: 8px; font-weight: bold; font-size: 0.9rem; cursor: pointer; display: flex; align-items: center; gap: 5px;">
                ☰ القائمة
            </button>
            {logo_html}
        </div>
        <div style="display: flex; align-items: center; gap: 20px;">
            <div style="font-size: 0.95rem; font-weight: bold; color: #333;">
                🔔 <span style="background-color: #e9ecef; padding: 2px 6px; border-radius: 6px; color: #d9534f;">{pending_count}</span>
            </div>
            <div style="font-size: 0.95rem; font-weight: bold; color: #333;">
                👤 <b>SA</b>
            </div>
        </div>
    </div>
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

st.sidebar.markdown("<h2 style='color: #1b5e20; margin-bottom: 5px; font-size: 1.3rem;'>🧭 القائمة الرئيسية</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='font-weight: 800; color: #1b5e20; font-size: 1rem; margin-top: 5px; margin-bottom: 10px;'>اختر الصفحة</p>", unsafe_allow_html=True)
page = st.sidebar.radio("اختر الصفحة", ["نموذج تصفية المرشد", "إدارة التصفيات", "الأرشيف"], label_visibility="collapsed")

if page == "نموذج تصفية المرشد":
    st.title("🧭 نموذج تصفية المرشدين")
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
            
        work_order_image = st.file_uploader("رفع صور أمر الشغل", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="work_order_imgs")
        
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
            
            option_data_list.append({"type": opt_type, "value": opt_val, "curr": opt_curr, "pay": opt_pay, "holder": cash_h})
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
                
                work_order_paths = []
                if work_order_image:
                    for img in work_order_image:
                        wo_path = os.path.join(UPLOAD_DIR, f"wo_{time.time()}_{img.name}")
                        with open(wo_path, "wb") as f:
                            f.write(img.getbuffer())
                        work_order_paths.append(wo_path)

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
                    "Work Order Images": ",".join(work_order_paths) if work_order_paths else "",
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
                
                st.session_state.option_rows_count = 1
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
                wo_paths = req_row.get("Work Order Images", "")
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
                st.markdown("### اتخاذ القرار بشأن الطلب (يتطلب صلاحية التعديل):")
                
                action_email = st.text_input("أدخل البريد الإلكتروني للمسؤول لتأكيد القرار", key="action_email_decision")
                
                col_btn1, col_btn2 = st.columns(2)
                
                with col_btn1:
                    if st.button("✅ تم (نقل للأرشيف)", type="primary", use_container_width=True):
                        if action_email.strip().lower() == ADMIN_EMAIL.lower():
                            archive_entry = req_row.to_dict()
                            save_to_file(ARCHIVE_FILE, archive_entry)
                            
                            sub_df = sub_df.drop(req_idx).reset_index(drop=True)
                            overwrite_data(SUBMISSIONS_FILE, sub_df)
                            
                            st.session_state.viewing_file = None
                            st.success("✅ تم نقل الطلب للأرشيف بنجاح!")
                            st.rerun()
                        else:
                            st.error("❌ مرفوض! البريد الإلكتروني المدخل غير مسموح له بتنفيذ التعديل أو نقل الطلبات.")
                
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
                        st.warning(f"⚠️ تأكيد حذف طلب الفايل رقم ({row.get('File No', '')})؟")
                        del_email_check = st.text_input("أدخل البريد الإلكتروني للمسؤول لتأكيد الحذف", key=f"del_email_sub_{idx}")
                        c_col1, c_col2 = st.columns(2)
                        with c_col1:
                            if st.button("✔️ تأكيد الحذف النهائي", key=f"confirm_del_sub_{idx}", type="primary"):
                                if del_email_check.strip().lower() == ADMIN_EMAIL.lower():
                                    sub_df = sub_df.drop(idx).reset_index(drop=True)
                                    overwrite_data(SUBMISSIONS_FILE, sub_df)
                                    st.session_state.confirming_del_sub = None
                                    st.success("تم الحذف بنجاح.")
                                    st.rerun()
                                else:
                                    st.error("❌ مرفوض! البريد الإلكتروني غير صحيح ولا تملك صلاحية الحذف.")
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
                        edit_email_chk = st.text_input("أدخل البريد الإلكتروني للمسؤول لتأكيد التعديل", key="edit_email_chk_field")
                        ec1, ec2 = st.columns(2)
                        with ec1:
                            if st.button("✔️ تأكيد وحفظ التعديل", type="primary", key="confirm_save_guide_acc"):
                                if edit_email_chk.strip().lower() == ADMIN_EMAIL.lower():
                                    guides_df.loc[guides_df[name_column].astype(str) == g_to_edit, acc_column] = n_acc
                                    overwrite_data(GUIDES_FILE, guides_df)
                                    st.session_state.confirming_edit_guide = None
                                    st.session_state.clear_edit_input = True
                                    st.success("✅ تم التعديل بنجاح!")
                                    st.rerun()
                                else:
                                    st.error("❌ مرفوض! البريد الإلكتروني غير مصرح له بتعديل الحسابات.")
                        with ec2:
                            if st.button("❌ إلغاء", key="cancel_save_guide_acc", type="primary"):
                                st.session_state.confirming_edit_guide = None
                                st.rerun()

                if st.session_state.confirming_del_guide is not None:
                    g_to_del = st.session_state.confirming_del_guide["name"]
                    
                    st.warning(f"⚠️ تأكيد حذف المرشد (**{g_to_del}**) نهائياً؟")
                    del_guide_email_chk = st.text_input("أدخل البريد الإلكتروني للمسؤول لتأكيد الحذف", key="del_guide_email_chk_field")
                    dc1, dc2 = st.columns(2)
                    with dc1:
                        if st.button("✔️ تأكيد الحذف النهائي", type="primary", key="confirm_del_guide_btn"):
                            if del_guide_email_chk.strip().lower() == ADMIN_EMAIL.lower():
                                guides_df = guides_df[guides_df[name_column].astype(str) != g_to_del].reset_index(drop=True)
                                overwrite_data(GUIDES_FILE, guides_df)
                                st.session_state.confirming_del_guide = None
                                st.success("تم حذف المرشد بنجاح.")
                                st.rerun()
                            else:
                                st.error("❌ مرفوض! البريد الإلكتروني غير مصرح له بحذف المرشدين.")
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
                        st.error("⚠️ يرجى إدخال (اسم المرشد) و(رقم الحساب) معاً!")
                        if st.button("❌ رجوع", type="primary", key="cancel_empty_add"):
                            st.session_state.confirming_add_guide = None
                            st.rerun()
                    else:
                        st.warning(f"⚠️ تأكيد إضافة المرشد (**{a_name}**) برقم حساب (**{a_acc}**)؟")
                        add_email_chk = st.text_input("أدخل البريد الإلكتروني للمسؤول لتأكيد الإضافة", key="add_email_chk_field")
                        ac1, ac2 = st.columns(2)
                        with ac1:
                            if st.button("✔️ تأكيد الإضافة", type="primary", key="confirm_add_guide_final"):
                                if add_email_chk.strip().lower() == ADMIN_EMAIL.lower():
                                    new_row = pd.DataFrame({name_column: [a_name], acc_column: [a_acc]})
                                    guides_df = pd.concat([guides_df, new_row], ignore_index=True)
                                    overwrite_data(GUIDES_FILE, guides_df)
                                    st.session_state.confirming_add_guide = None
                                    st.session_state.clear_add_inputs = True
                                    st.success("✅ تم إضافة المرشد بنجاح!")
                                    st.rerun()
                                else:
                                    st.error("❌ مرفوض! البريد الإلكتروني غير مصرح له بإضافة مرشدين جدد.")
                        with ac2:
                            if st.button("❌ إلغاء", key="cancel_add_guide_final", type="primary"):
                                st.session_state.confirming_add_guide = None
                                st.rerun()
    elif password != "":
        st.error("⚠️ كلمة المرور غير صحيحة!")

elif page == "الأرشيف":
    st.title("📁 الأرشيف (الطلبات التي تم تصفيتها وتأكيدها)")
    st.markdown("---")
    
    arch_password = st.text_input("أدخل كلمة المرور لعرض الأرشيف", type="password", key="arch_pass")
        
    if arch_password == "159753":
        st.success("تم تسجيل الدخول لعرض الأرشيف بنجاح.")
        archive_df = load_data(ARCHIVE_FILE)
        if not archive_df.empty:
            st.dataframe(archive_df, use_container_width=True)
        else:
            st.info("الأرشيف فارغ حالياً.")
    elif arch_password != "":
        st.error("⚠️ كلمة المرور غير صحيحة!")
