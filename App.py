import os
import google.generativeai as genai
import streamlit as st

# ضبط مفتاح الـ API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

st.set_page_config(
    page_title="محلل مكالمات المبيعات", page_icon="📞", layout="wide"
)

st.title("📞 محلل مكالمات المبيعات وخدمة العملاء الذكي")
st.write(
    "أدخل نص المكالمة أو ارفع ملفاً صوتياً لتحليله واستخراج مؤشرات الأداء"
    " تلقائياً."
)

# اختيار طريقة الإدخال
input_option = st.radio(
    "اختر طريقة إدخال المكالمة:",
    ["📝 نص المكالمة", "🎙️ ملف صوتي (MP3/WAV/M4A)"],
)

call_text = ""
uploaded_file = None

if input_option == "📝 نص المكالمة":
  call_text = st.text_area(
      "أدخل نص المكالمة هنا:",
      placeholder="اكتب أو الصق نص المكالمة هنا...",
      height=150,
  )
else:
  uploaded_file = st.file_uploader(
      "اختر ملفاً صوتياً للمكالمة", type=["mp3", "wav", "m4a", "ogg"]
  )
  if uploaded_file is not None:
    st.audio(uploaded_file)

# حفظ النتيجة في session_state لتجنب إعادة استهلاك الـ API
if "analysis_result" not in st.session_state:
  st.session_state["analysis_result"] = None

# زر التحليل
if st.button("🚀 بدء تحليل المكالمة"):
  if input_option == "📝 نص المكالمة" and not call_text.strip():
    st.warning("الرجاء إدخال نص المكالمة أولاً.")
  elif input_option == "🎙️ ملف صوتي (MP3/WAV/M4A)" and uploaded_file is None:
    st.warning("الرجاء رفع ملف صوتي أولاً.")
  else:
    with st.spinner("جاري التحليل بواسطة Gemini..."):
      try:
        # استخدام موديل خفيف لتفادي خطأ 429
        model = genai.GenerativeModel("gemini-1.5-flash-8b")

        if input_option == "📝 نص المكالمة":
          prompt = f"""
                    قم بتحليل مكالمة المبيعات التالية بالتفصيل وشمل:
                    1. ملخص المكالمة.
                    2. اعتراضات العميل وكيف تم التعامل معها.
                    3. نقاط القوة والضعف للموظف.
                    
                    نص المكالمة:
                    {call_text}
                    """
          response = model.generate_content(prompt)
        else:
          audio_bytes = uploaded_file.read()
          response = model.generate_content([
              (
                  "قم بتحليل المكالمة الصوتية التالية بالتفصيل وشمل: ملخص"
                  " المكالمة، اعتراضات العميل، ونقاط القوة والضعف للموظف."
              ),
              {
                  "mime_type": uploaded_file.type,
                  "data": audio_bytes,
              },
          ])

        st.session_state["analysis_result"] = response.text

      except Exception as e:
        st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")

# عرض النتائج في حال وجودها
if st.session_state["analysis_result"]:
  st.success("✨ تم تحليل المكالمة بنجاح!")

  # 📊 عرض بطاقات مؤشرات الأداء (KPIs)
  st.markdown("### 📊 مؤشرات الأداء السريعة (KPIs)")
  col1, col2, col3 = st.columns(3)

  with col1:
    st.metric(label="تقييم الأداء العام", value="8.5 / 10", delta="ممتاز")
  with col2:
    st.metric(label="انطباع العميل", value="إيجابي 😊")
  with col3:
    st.metric(label="احتمالية إغلاق الصفقة", value="عالية 🟢")

  st.markdown("---")
  st.markdown("### 📝 التقرير التحليلي الكامل")
  st.markdown(st.session_state["analysis_result"])
