import streamlit as st

# ضبط إعدادات الصفحة لتكون عريضة
st.set_page_config(layout="wide", page_title="Sun Pyramids Tours - تصفية المرشدين")

# حقن كود الـ CSS وتصميم الواجهة المخصص تماماً
st.markdown("""
<style>
    /* إخفاء عناصر ستريملايت الافتراضية */
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

    /* الشريط الجانبي (في جهة اليمين للغة العربية) */
    .custom-sidebar {
        width: 280px;
        background-color: #e8f0eb;
        border-left: 1px solid #d0ded3;
        display: flex;
        flex-direction: column;
        padding: 20px;
        position: absolute;
        height: 100%;
        right: 0;
        z-index: 50;
        box-shadow: -2px 0 5px rgba(0,0,0,0.05);
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
        background-color: #f4f7f6;
        height: 100%;
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

# إدارة حالة التطبيق
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'filter'
if 'authenticated_archive' not in st.session_state:
    st.session_state.authenticated_archive = False
if 'authenticated_manage' not in st.session_state:
    st.session_state.authenticated_manage = False

# هيدر علوي (بدون كلمة القائمة)
st.markdown("""
    <div class="custom-header">
        <div class="logo-container">
            <img src="https://via.placeholder.com/150x45?text=Sun+Pyramids+Tours" alt="Sun Pyramids Tours">
        </div>
    </div>
""", unsafe_allow_html=True)

# الهيكل العام والتنقل
st.markdown("""
    <div class="main-container">
        <div class="custom-sidebar">
            <div class="sidebar-header">
                <div class="sidebar-title">
                    <span>🧭</span> القائمة الرئيسية
                </div>
            </div>
            <div class="nav-section-title">اختر الصفحة</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# استخدام أدوات Streamlit الأصلية بطريقة منسقة داخل الكلاسات مظبوطة تماماً
st.sidebar.markdown("### 🧭 القائمة الرئيسية")
st.sidebar.markdown("---")
st.sidebar.markdown("#### اختر الصفحة")

selected_page = st.sidebar.radio(
    "التنقل",
    ["نموذج تصفية المرشد", "إدارة التصفيات", "الأرشيف"],
    label_visibility="collapsed"
)

# محتوى الصفحات مع الحماية الكاملة بالباسورد 159753
if selected_page == "نموذج تصفية المرشد":
    st.markdown("""
        <div style="margin-right: 280px; padding: 30px;">
            <div class="page-box">
                <h2>نموذج تصفية المرشد</h2>
                <p>هنا يتم عرض نموذج تصفية وإدخال بيانات المرشدين السياحيين والمصاريف.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

elif selected_page == "إدارة التصفيات":
    st.markdown('<div style="margin-right: 280px; padding: 30px;"><div class="page-box">', unsafe_allow_html=True)
    st.subheader("إدارة التصفيات")
    
    if not st.session_state.authenticated_manage:
        st.warning("⚠️ هذه الصفحة محمية بكلمة المرور.")
        pwd_manage = st.text_input("أدخل كلمة المرور:", type="password", key="p_manage")
        if st.button("دخول لإدارة التصفيات"):
            if pwd_manage == "159753":
                st.session_state.authenticated_manage = True
                st.rerun()
            else:
                st.error("كلمة المرور غير صحيحة!")
    else:
        st.success("تم تسجيل الدخول بنجاح.")
        st.write("هنا يتم إدارة ومراجعة التصفيات المسجلة.")
        if st.button("تسجيل خروج من الإدارة"):
            st.session_state.authenticated_manage = False
            st.rerun()
            
    st.markdown('</div></div>', unsafe_allow_html=True)

elif selected_page == "الأرشيف":
    st.markdown('<div style="margin-right: 280px; padding: 30px;"><div class="page-box">', unsafe_allow_html=True)
    st.subheader("الأرشيف")
    
    if not st.session_state.authenticated_archive:
        st.warning("⚠️ صفحة الأرشيف محمية بكلمة المرور.")
        pwd_archive = st.text_input("أدخل كلمة المرور:", type="password", key="p_archive")
        if st.button("دخول للأرشيف"):
            if pwd_archive == "159753":
                st.session_state.authenticated_archive = True
                st.rerun()
            else:
                st.error("كلمة المرور غير صحيحة!")
    else:
        st.success("تم التحقق بنجاح.")
        st.write("هنا يتم عرض الأرشيف والسجلات القديمة.")
        if st.button("تسجيل خروج من الأرشيف"):
            st.session_state.authenticated_archive = False
            st.rerun()
            
    st.markdown('</div></div>', unsafe_allow_html=True)
