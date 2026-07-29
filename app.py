import streamlit as st
import pandas as pd

st.set_page_config(page_title="نظام تصفية المرشدين", page_icon="🧭", layout="wide")

# تحميل ملف الداتا بأمان
try:
    guides_df = pd.read_excel("guides.xlsx")
except:
    guides_df = pd.DataFrame({"Guide Name": ["أحمد", "محمود"], "Account Number": ["1805000493514500022", "1805000493514500033"]})

# تجهيز اسم عمود الحسابات بذكاء بره الفورم لتجنب أي أخطاء مسافات
acc_column = guides_df.columns[1] if len(guides_df.columns) > 1 else guides_df.columns[0]

st.sidebar.title("القائمة الرئيسية")
page = st.sidebar.radio("اختر الصفحة", ["نموذج تصفية المرشد", "لوحة تحكم المدير"])

if "submissions" not in st.session_state:
    st.session_state["submissions"] = []

if page == "نموذج تصفية المرشد":
    st.title("🧭 نظام تصفية المرشدين")
    st.markdown("---")
    
    with st.form("guide_form"):
        account_no = st.selectbox("رقم الحساب الخاص بالمرشد", options=guides_df[acc_column].astype(str).tolist())
        tip = st.number_input("إكرامية (Tip)", min_value=0.0, step=10.0)
        file_no = st.text_input("رقم الفايل (File Number)")
        
        st.subheader("الحقول المالية (أرقام فقط)")
        tickets = st.number_input("تذاكر (Tickets)", min_value=0.0, step=10.0)
        park = st.number_input("بارك (Park)", min_value=0.0, step=10.0)
        lunch = st.number_input("غداء (Lunch)", min_value=0.0, step=10.0)
        
        submitted = st.form_submit_button("إرسال الطلب للمدير")
        
        if submitted:
            new_entry = {
                "Account": account_no,
                "File No": file_no,
                "Tip": tip,
                "Tickets": tickets,
                "Park": park,
                "Lunch": lunch
            }
            st.session_state["submissions"].append(new_entry)
            st.success("تم إرسال الطلب بنجاح!")

elif page == "لوحة تحكم المدير":
    st.title("📊 لوحة تحكم المدير")
    st.markdown("---")
    
    password = st.text_input("أدخل كلمة المرور", type="password")
    
    if password == "159753":
        st.success("تم تسجيل الدخول بنجاح!")
        if len(st.session_state["submissions"]) > 0:
            sub_df = pd.DataFrame(st.session_state["submissions"])
            st.data_editor(sub_df, use_container_width=True)
        else:
            st.info("لا توجد طلبات جديدة حتى الآن.")
        
        st.markdown("### قاعدة بيانات المرشدين")
        st.dataframe(guides_df, use_container_width=True)
    elif password:
        st.error("كلمة المرور غير صحيحة.")
    else:
        st.info("الرجاء إدخال كلمة المرور لعرض لوحة التحكم.")
