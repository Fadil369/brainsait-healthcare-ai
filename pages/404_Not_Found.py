import streamlit as st

st.set_page_config(page_title="404 • BrainSAIT", page_icon="🔍", layout="wide")

lang = st.session_state.get("ui_language", "en")
lang = st.radio("Language / اللغة", ["en", "ar"], index=0 if lang=="en" else 1, horizontal=True, key="notfound_lang")
st.session_state["ui_language"] = lang

T = {
    "en": {
        "title": "404 - Page Not Found",
        "desc": "The page you are looking for doesn’t exist. It may have been moved, renamed, or removed.",
        "home": "Go to Home",
        "privacy": "Privacy Policy",
        "tos": "Terms of Service",
        "footer": "If you believe this is an error, contact your administrator or check navigation from the sidebar.",
    },
    "ar": {
        "title": "404 - الصفحة غير موجودة",
        "desc": "الصفحة التي تبحث عنها غير موجودة. ربما تم نقلها أو إعادة تسميتها أو حذفها.",
        "home": "الذهاب إلى الرئيسية",
        "privacy": "سياسة الخصوصية",
        "tos": "شروط الخدمة",
        "footer": "إذا كنت تعتقد أن هذا خطأ، يرجى التواصل مع المسؤول أو التحقق من القائمة الجانبية.",
    }
}
tr = T[lang]

st.title(tr["title"]) 
st.write(tr["desc"]) 

st.page_link("app.py", label=tr["home"], icon="🏠")
st.page_link("pages/1_Privacy_Policy.py", label=tr["privacy"], icon="🛡️")
st.page_link("pages/2_Terms_of_Service.py", label=tr["tos"], icon="📜")

st.caption(tr["footer"])