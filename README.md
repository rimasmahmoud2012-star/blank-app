import streamlit as st
import os
from google import genai
from google.genai import types

# إعداد الصفحة
st.set_page_title("محلل مكالمات المبيعات الذكي")
st.set_page_layout("wide")

st.title("📞 محلل مكالمات المبيعات بالذكاء الاصطناعي")
st.write("قم برفع ملف نصي يحتوي على نص مكالمة المبيعات، وسيقوم النظام بتحليله واستخراج النقاط الهامة.")

# إدخال مفتاح الـ API
api_key = st.text_input("أدخل مفتاح Gemini API الخاص بك:", type="password")

# رفع ملف نصي للمكالمة
uploaded_file = st.file_uploader("اختر ملف نصي للمكالمة (TXT)", type=["txt"])

if uploaded_file is not None and api_key:
    # قراءة محتوى الملف
    call_text = uploaded_file.read().decode("utf-8")
    
    with st.expander("عرض نص المكالمة الأصلي"):
        st.text(call_text)
        
    if st.button("بدء التحليل الشامل", type="primary"):
        with st.spinner("جاري تحليل المكالمة باستخدام Gemini..."):
            try:
                # تهيئة عميل Gemini الجديد
                client = genai.Client(api_key=api_key)
                
                prompt = f"""
                قم بتحليل مكالمات المبيعات التالية بدقة واحترافية عالية. قدم التحليل باللغة العربية ويتضمن:
                1. ملخص تنفيذي للمكالمة.
                2. أبرز نقاط الألم واحتياجات العميل.
                3. الاعتراضات التي أبداها العميل وكيف تم التعامل معها.
                4. تقييم أداء مسؤول المبيعات (نقاط القوة والتحسين).
                5. الخطوات القادمة أو التوصيات لإغلاق الصفقة بنجاح.

                نص المكالمة:
                {call_text}
                """
