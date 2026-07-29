import streamlit as st
import pandas as pd

st.set_page_config(page_title="نظام تصفية المرشدين", page_icon="🧭", layout="wide")

try:
    guides_df = pd.read_excel("guides.xlsx")
except:
    guides_df = pd.DataFrame({"Guide Name": ["أحمد", "محمود"], "Account Number": ["1805000493514500022", "1805000493514500033"]})

acc_column = guides_df.columns[1] if len(guides_df.columns) > 1 else guides_df.columns[0]

st.sidebar.title("القائمة الرئيسية")
page = st.sidebar.radio("اختر الصفحة", ["نموذج تصفية المرشد", "لوحة تحكم المدير"])

if "submissions" not in st.session_state:
    st.session_state["submissions"] = []

if page == "نموذج تصفية المرشد":
    st.title("🧭 نظام تصفية المرشدين")
    st.markdown("---")
    
    # الحقول الأساسية فوق فقط
    account_no = st.selectbox("رقم الحساب الخاص بالمرشد", options=guides_df[acc_column].astype(str).tolist())
    file_no = st.text_input("رقم الفايل (File Number)")
    
    st.markdown("---")
    st.subheader("الحقول المالية")
    
    # نقل الإكرامية لتكون مع باقي الحقول المالية وتحت
    tip = st.number_input("إكرامية (Tip)", min_value=0.0, step=10.0)
    tickets = st.number_input("تذاكر (Tickets)", min_value=0.0, step=10.0)
    park = st.number_input("بارك (Park)", min_value=0.0, step=10.0)
    
    # بند الغداء مع رفع صورة الفاتورة
    lunch = st.number_input("غداء (Lunch)", min_value=0.0, step=10.0)
    lunch_image = st.file_uploader("رفع صورة فاتورة الغداء", type=["png", "jpg", "jpeg"], key="lunch_img")
    
    st.markdown("---")
    shop_bills_amount = st.number_input("قيمة فواتير المحلات", min_value=0.0, step=10.0)
    shop_images = st.file_uploader("رفع صور فواتير المحلات", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="shop_imgs")
    
    if st.button("إرسال الطلب للمدير", type="primary"):
        new_entry = {
            "Account": account_no,
            "File No": file_no,
            "Tip": tip,
            "Tickets": tickets,
            "Park": park,
            "Lunch": lunch,
            "Lunch Receipt": lunch_image.name if lunch_image else "لا توجد صورة",
            "Shop Bills": shop_bills_amount,
            "Shop Images Count": len(shop_images) if shop_images else 0
        }
        st.session_state["submissions"].append(new_entry)
        st.success("تم إرسال الطلب بنجاح مع الصور والمرفقات!")

elif page == "لوحة تحكم المدير":
    st.title("📊 لوحة تحكم المدير")
    st.markdown("---")
    
    password = st.text_input("أدخل كلمة المرور", type="password")
    
    if password == "159753":
        st.success("تم تسجيل الدخول بنجاح!")
        if len(st.session_state["submissions"]) > 0:
            sub_df = pd.DataFrame(st.session_state["submissions"])
            st.markdown("### الطلبات الواردة")
            st.data_editor(sub_df, use_container_width=True)
        else:
            st.info("لا توجد طلبات جديدة حتى الآن.")
        
        st.markdown("### قاعدة بيانات المرشدين")
        st.dataframe(guides_df, use_container_width=True)
    elif password:
        st.error("كلمة المرور غير صحيحة.")
    else:
        st.info("الرجاء إدخال كلمة المرور لعرض لوحة التحكم.")
