import os
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Terms of Service • BrainSAIT", page_icon="📜", layout="wide")

# Language selection
lang = st.session_state.get("ui_language", "en")
lang = st.radio("Language / اللغة", ["en", "ar"], index=0 if lang=="en" else 1, horizontal=True, key="tos_lang")
st.session_state["ui_language"] = lang

effective = os.getenv("LEGAL_EFFECTIVE_DATE") or datetime.utcnow().date().isoformat()

T = {
    "en": {
        "title": "Terms of Service",
        "effective": "Effective date: {}",
        "intro": "These Terms of Service (the “Terms”) govern your use of the BrainSAIT Platform. By accessing or using the Platform, you agree to these Terms. If you do not agree, do not use the Platform.",
        "s1": "1. Use of the Platform",
        "s1b": "- You are responsible for complying with all applicable laws and regulations (e.g., HIPAA, NPHIES policies).\n- You will not misuse the Platform or attempt to access data or functionality without authorization.",
        "s2": "2. Accounts and Access",
        "s2b": "- Access may be provisioned by your organization; you are responsible for safeguarding credentials.\n- Access may be revoked for violations of these Terms or organizational policies.",
        "s3": "3. Clinical and Operational Disclaimers",
        "s3b": "- Outputs may assist workflows but are not a substitute for professional judgment.\n- The Platform is provided \"as is\" without warranties of any kind.",
        "s4": "4. Data and Privacy",
        "s4b": "- Use of the Platform is subject to the Privacy Policy.\n- Data handling depends on your deployment configuration and organization policies.",
        "s5": "5. Third-Party Services",
        "s5b": "- Integrations (e.g., FHIR, NPHIES, n8n, Claude, Atlassian) are governed by their providers’ terms.",
        "s6": "6. Modifications and Availability",
        "s6b": "- Features and services may change without notice. Availability may be affected by maintenance or outages.",
        "s7": "7. Limitation of Liability",
        "s7b": "- To the extent permitted by law, the Platform and its contributors shall not be liable for indirect, incidental, or consequential damages.",
        "s8": "8. Governing Law",
        "s8b": "- These Terms should be adapted to reflect your jurisdiction and organizational requirements.",
        "s9": "9. Contact",
        "s9b": "For questions about these Terms, contact your organization’s BrainSAIT administrator.",
        "footer": "This page is a template. Consult legal counsel and customize for your organization.",
    },
    "ar": {
        "title": "شروط الخدمة",
        "effective": "تاريخ السريان: {}",
        "intro": "تحكم شروط الخدمة هذه استخدامك لمنصة BrainSAIT. باستخدام المنصة، فإنك توافق على هذه الشروط. إذا لم توافق، فلا تستخدم المنصة.",
        "s1": "1. استخدام المنصة",
        "s1b": "- تقع عليك مسؤولية الامتثال لجميع القوانين واللوائح المطبقة (مثل HIPAA وسياسات NPHIES).\n- لا تسئ استخدام المنصة أو تحاول الوصول إلى بيانات أو وظائف دون إذن.",
        "s2": "2. الحسابات والوصول",
        "s2b": "- قد يتم منح الوصول من قبل مؤسستك؛ أنت مسؤول عن حماية بيانات الاعتماد.\n- قد يتم إلغاء الوصول عند مخالفة هذه الشروط أو سياسات المؤسسة.",
        "s3": "3. إخلاءات المسؤولية السريرية والتشغيلية",
        "s3b": "- قد تساعد المخرجات في سير العمل ولكنها لا تغني عن الحكم المهني.\n- تُقدم المنصة \"كما هي\" دون أي ضمانات.",
        "s4": "4. البيانات والخصوصية",
        "s4b": "- يخضع استخدام المنصة لسياسة الخصوصية.\n- تعتمد معالجة البيانات على إعدادات النشر وسياسات مؤسستك.",
        "s5": "5. خدمات الطرف الثالث",
        "s5b": "- تخضع عمليات التكامل (مثل FHIR وNPHIES وn8n وClaude وAtlassian) لشروط مزوديها.",
        "s6": "6. التعديلات والتوافر",
        "s6b": "- قد تتغير الميزات والخدمات دون إشعار. قد يتأثر التوافر بالصيانة أو الأعطال.",
        "s7": "7. تحديد المسؤولية",
        "s7b": "- إلى الحد الذي يسمح به القانون، لا تتحمل المنصة أو المساهمون فيها المسؤولية عن الأضرار غير المباشرة أو العرضية أو التبعية.",
        "s8": "8. القانون الحاكم",
        "s8b": "- ينبغي تكييف هذه الشروط لتعكس متطلبات ولايتك القضائية ومؤسستك.",
        "s9": "9. تواصل",
        "s9b": "للاستفسارات حول هذه الشروط، تواصل مع مسؤول BrainSAIT في مؤسستك.",
        "footer": "هذه الصفحة نموذج. يرجى استشارة القسم القانوني وتخصيصها بما يناسب مؤسستك.",
    },
}

tr = T[lang]

st.title(tr["title"]) 
st.caption(tr["effective"].format(effective))

st.info(tr["intro"]) 

for k in ["s1","s2","s3","s4","s5","s6","s7","s8","s9"]:
    st.header(tr[k])
    st.markdown(tr[f"{k}b"]) 

st.divider()
st.caption(tr["footer"])