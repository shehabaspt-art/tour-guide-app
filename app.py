import streamlit as st

# ضبط إعدادات الصفحة لتكون عريضة
st.set_page_config(
    page_title="Sun Pyramids Tours - تصفية المرشدين",
    layout="wide",
    initial_sidebar_state="expanded"
)

# كلمة المرور الموحدة للصفحات المحمية
CORRECT_PASSWORD = "159753"

# تهيئة المتغيرات في الجلسة (Session State)
if "authenticated_manage" not in st.session_state:
    st.session_state.authenticated_manage = False

if "authenticated_archive" not in st.session_state:
    st.session_state.authenticated_archive = False

# هيدر الصفحة العلوي (بدون كلمة "القائمة" بجانب اللوجو)
st.markdown("""
    <div style="display: flex; align-items: center; padding: 10px 0; border-bottom: 2px solid #e0e0e0; margin-bottom: 20px;">
        <img src="https://via.placeholder.com/150x45?text=Sun+Pyramids+Tours" alt="Sun Pyramids Tours" style="height: 45px;">
    </div>
""", unsafe_allow_html=True)

# الشريط الجانبي (Sidebar) لاختيار الصفحات
st.sidebar.markdown("### 🧭 القائمة الرئيسية")
st.sidebar.markdown("---")
st.sidebar.markdown("#### اختر الصفحة")

page = st.sidebar.radio(
    "التنقل بين الصفحات",
    ["نموذج تصفية المرشد", "إدارة التصفيات", "الأرشيف"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.info("شركة Sun Pyramids Tours - نظام تصفية حسابات المرشدين والمصاريف.")

# منطق عرض الصفحات والحماية بالباسورد
if page == "نموذج تصفية المرشد":
    st.title("نموذج تصفية المرشد")
    st.write("هنا يتم عرض نموذج تصفية وإدخال بيانات المرشدين السياحيين والمصاريف بدقة.")
    # ضع هنا محتويات صفحة التصفية الخاصة بك

elif page == "إدارة التصفيات":
    st.title("إدارة التصفيات")
    
    if not st.session_state.authenticated_manage:
        st.warning("⚠️ هذه الصفحة محمية بكلمة المرور.")
        password_input = st.text_input("أدخل كلمة المرور لإدارة التصفيات:", type="password", key="pass_manage")
        
        if st.button("دخول", key="btn_manage"):
            if password_input == CORRECT_PASSWORD:
                st.session_state.authenticated_manage = True
                st.rerun()
            else:
                st.error("كلمة المرور غير صحيحة!")
    else:
        st.success("تم تسجيل الدخول بنجاح.")
        st.write("هنا يتم إدارة ومراجعة التصفيات المسجلة.")
        # زر لتسجيل الخروج إذا أردت
        if st.button("قفل الصفحة (تسجيل خروج)"):
            st.session_state.authenticated_manage = False
            st.rerun()

elif page == "الأرشيف":
    st.title("الأرشيف")
    
    if not st.session_state.authenticated_archive:
        st.warning("⚠️ صفحة الأرشيف محمية بكلمة المرور.")
        password_input_arch = st.text_input("أدخل كلمة المرور للأرشيف:", type="password", key="pass_archive")
        
        if st.button("دخول", key="btn_archive"):
            if password_input_arch == CORRECT_PASSWORD:
                st.session_state.authenticated_archive = True
                st.rerun()
            else:
                st.error("كلمة المرور غير صحيحة!")
    else:
        st.success("تم التحقق بنجاح.")
        st.write("هنا يتم عرض الأرشيف والسجلات القديمة بأمان تام.")
        if st.button("قفل صفحة الأرشيف"):
            st.session_state.authenticated_archive = False
            st.rerun()
