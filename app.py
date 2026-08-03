import streamlit as st

# ضبط إعدادات الصفحة لتكون عريضة
st.set_page_config(layout="wide", page_title="Sun Pyramids Tours - تصفية المرشدين")

# حقن كود الـ CSS والتصميم داخل Streamlit
st.markdown("""
<style>
    /* إخفاء عناصر ستريملايت الافتراضية لعمل واجهة مخصصة بالكامل */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #f4f7f6; }

    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
        font-family: 'Arial', sans-serif;
    }

    /* الهيدر العلوي */
    .custom-header {
        background-color: #ffffff;
        border-bottom: 2px solid #e0e0e0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 20px;
        height: 70px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        width: 100%;
        position: fixed;
        top: 0;
        right: 0;
        z-index: 100;
    }

    .logo-container img {
        height: 45px;
    }

    /* المحتوى الرئيسي */
    .main-container {
        display: flex;
        position: relative;
        margin-top: 70px;
        height: calc(100vh - 70px);
        overflow: hidden;
    }

    /* الشريط الجانبي */
    .custom-sidebar {
        width: 280px;
        background-color: #e8f0eb;
        border-left: 1px solid #d0ded3;
        display: flex;
        flex-direction: column;
        padding: 20px;
        transition: transform 0.3s ease;
        position: absolute;
        height: 100%;
        right: 0;
        z-index: 50;
        box-shadow: -2px 0 5px rgba(0,0,0,0.05);
    }

    .custom-sidebar.hidden {
        transform: translateX(100%);
    }

    .sidebar-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #ffffff;
        padding: 10px 15px;
        border-radius: 8px;
        border: 1px solid #c8dcd0;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    .sidebar-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: bold;
        color: #1b4d2e;
    }

    /* زر السهم لإخفاء الشريط */
    .toggle-btn {
        background-color: #1b4d2e;
        color: white;
        border: none;
        width: 32px;
        height: 32px;
        border-radius: 6px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
    }

    .toggle-btn:hover {
        background-color: #12351f;
    }

    .nav-section-title {
        font-size: 14px;
        color: #1b4d2e;
        margin-bottom: 12px;
        font-weight: bold;
    }

    /* مساحة العرض الرئيسية */
    .content-area {
        flex: 1;
        padding: 30px;
        overflow-y: auto;
        margin-right: 280px;
        transition: margin-right 0.3s ease;
        background-color: #f4f7f6;
        height: 100%;
    }

    .content-area.expanded {
        margin-right: 0;
    }

    .page-box {
        background: white;
        padding: 25px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        min-height: 400px;
    }

    h2 {
        color: #1b4d2e;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# إدارة حالة التطبيق (الصفحة الحالية، حالة الشريط الجانبي، وحالة تسجيل الدخول)
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'filter'
if 'sidebar_hidden' not in st.session_state:
    st.session_state.sidebar_hidden = False
if 'authenticated_page' not in st.session_state:
    st.session_state.authenticated_page = None

# معالجة الضغط على أزرار JavaScript المحاكاة عبر Streamlit Query Params أو الأزرار
query_params = st.query_params
if "action" in query_params:
    action = query_params["action"]
    if action == "toggle_sidebar":
        st.session_state.sidebar_hidden = not st.session_state.sidebar_hidden
        st.query_params.clear()
        st.rerun()
    elif action == "navigate":
        page = query_params.get("page", "filter")
        if page in ["manage", "archive"]:
            if st.session_state.authenticated_page == page:
                st.session_state.current_page = page
            else:
                st.session_state.pending_page = page
        else:
            st.session_state.current_page = page
            st.session_state.authenticated_page = None
        st.query_params.clear()
        st.rerun()

# الهيدر العلوي (بدون كلمة القائمة)
st.markdown("""
    <div class="custom-header">
        <div class="logo-container">
            <img src="https://via.placeholder.com/150x45?text=Sun+Pyramids+Tours" alt="Sun Pyramids Tours">
        </div>
    </div>
""", unsafe_allow_html=True)

# تحديد كلاسات الإخفاء
sidebar_class = "custom-sidebar hidden" if st.session_state.sidebar_hidden else "custom-sidebar"
content_class = "content-area expanded" if st.session_state.sidebar_hidden else "content-area"

# زر إظهار الشريط الجانبي إذا كان مخفياً
if st.session_state.sidebar_hidden:
    if st.button("▶ إظهار القائمة", key="show_sidebar_top"):
        st.session_state.sidebar_hidden = False
        st.rerun()

# هيكل الشريط الجانبي وصفحات التنقل
sidebar_html = f"""
    <div class="{sidebar_class}" id="sidebar">
        <div class="sidebar-header">
            <div class="sidebar-title">
                <span>🧭</span> القائمة الرئيسية
            </div>
            <button class="toggle-btn" onclick="window.location.href='?action=toggle_sidebar'" title="إخفاء القائمة">◀</button>
        </div>

        <div class="nav-section-title">اختر الصفحة</div>
        
        <div style="display: flex; flex-direction: column; gap: 10px;">
            <button onclick="window.location.href='?action=navigate&page=filter'" style="padding: 12px; text-align: right; background: {'#f0f7f2' if st.session_state.current_page == 'filter' else 'white'}; border: 1px solid {'#1b4d2e' if st.session_state.current_page == 'filter' else '#c8dcd0'}; border-radius: 8px; cursor: pointer; font-weight: bold; color: #1b4d2e;">
                ⚪ نموذج تصفية المرشد
            </button>
            <button onclick="window.location.href='?action=navigate&page=manage'" style="padding: 12px; text-align: right; background: {'#f0f7f2' if st.session_state.current_page == 'manage' else 'white'}; border: 1px solid {'#1b4d2e' if st.session_state.current_page == 'manage' else '#c8dcd0'}; border-radius: 8px; cursor: pointer; font-weight: bold; color: #1b4d2e;">
                🔒 إدارة التصفيات
            </button>
            <button onclick="window.location.href='?action=navigate&page=archive'" style="padding: 12px; text-align: right; background: {'#f0f7f2' if st.session_state.current_page == 'archive' else 'white'}; border: 1px solid {'#1b4d2e' if st.session_state.current_page == 'archive' else '#c8dcd0'}; border-radius: 8px; cursor: pointer; font-weight: bold; color: #1b4d2e;">
                🔒 الأرشيف
            </button>
        </div>
    </div>
"""
st.markdown(sidebar_html, unsafe_allow_html=True)

# نافذة إدخال كلمة المرور للصفحات المحمية (إدارة التصفيات والأرشيف)
if 'pending_page' in st.session_state:
    st.markdown("---")
    st.warning("⚠️ هذه الصفحة محمية بكلمة المرور (159753)")
    entered_pass = st.text_input("أدخل كلمة المرور:", type="password", key="pass_box")
    col_1, col_2 = st.columns(2)
    with col_1:
        if st.button("دخول"):
            if entered_pass == "159753":
                st.session_state.authenticated_page = st.session_state.pending_page
                st.session_state.current_page = st.session_state.pending_page
                del st.session_state.pending_page
                st.rerun()
            else:
                st.error("كلمة المرور غير صحيحة!")
    with col_2:
        if st.button("إلغاء"):
            del st.session_state.pending_page
            st.rerun()

else:
    # عرض محتوى الصفحة الحالية
    st.markdown(f'<div class="{content_class}">', unsafe_allow_html=True)
    
    if st.session_state.current_page == 'filter':
        st.markdown("""
            <div class="page-box">
                <h2>نموذج تصفية المرشد</h2>
                <p>هنا يتم عرض نموذج تصفية وإدخال بيانات المرشدين السياحيين والمصاريف.</p>
            </div>
        """, unsafe_allow_html=True)
        
    elif st.session_state.current_page == 'manage':
        st.markdown("""
            <div class="page-box">
                <h2>إدارة التصفيات</h2>
                <p>هنا يتم إدارة ومراجعة التصفيات المسجلة.</p>
            </div>
        """, unsafe_allow_html=True)
        
    elif st.session_state.current_page == 'archive':
        st.markdown("""
            <div class="page-box">
                <h2>الأرشيف</h2>
                <p>هنا يتم عرض الأرشيف والسجلات القديمة بأمان.</p>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)
