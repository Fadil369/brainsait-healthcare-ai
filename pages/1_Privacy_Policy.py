import os
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Privacy Policy • BrainSAIT", page_icon="🛡️", layout="wide")

# Language selection (uses global sidebar state if present)
lang = st.session_state.get("ui_language", "en")
lang = st.radio("Language / اللغة", ["en", "ar"], index=0 if lang=="en" else 1, horizontal=True, key="privacy_lang")
st.session_state["ui_language"] = lang

# Effective date from env or today
effective = os.getenv("LEGAL_EFFECTIVE_DATE") or datetime.utcnow().date().isoformat()

# Translations
T = {
    "en": {
        "title": "Privacy Policy",
        "effective": "Effective date: {}",
        "intro": "This Privacy Policy describes how BrainSAIT (the “Platform”) collects, uses, and protects information. It is designed for healthcare environments and aims to align with HIPAA and local regulations.",
        "sec1": "1. Information We Collect",
        "sec1_body": "- PHI/PII provided by users or systems (e.g., EHR/FHIR, claims/NPHIES).\n- Operational metadata and audit logs for compliance.\n- Configuration and integration data (e.g., workflow endpoints, API keys).",
        "sec2": "2. How We Use Information",
        "sec2_body": "- To deliver clinical decision support, claims validation, and workflow automation.\n- To maintain security, auditability, and regulatory compliance.\n- To improve system reliability and user experience.",
        "sec3": "3. Data Security and Compliance",
        "sec3_body": "- Encryption in transit and at rest where supported by deployment.\n- HIPAA-oriented audit logging (configurable via environment).\n- Access controls aligned to least-privilege principles.",
        "sec4": "4. Data Retention",
        "sec4_body": "- Retention periods are configurable by the deploying organization.\n- Audit logs are retained pursuant to policy and regulatory needs.",
        "sec5": "5. Third-Party Services",
        "sec5_body": "- The Platform may integrate with services such as NPHIES, FHIR servers, n8n, Claude, and Atlassian.\n- Your use is subject to the terms and policies of those providers.",
        "sec6": "6. International and Local Regulations",
        "sec6_body": "- Deployments should verify alignment with local regulations (e.g., KSA MOH, NPHIES policies).",
        "sec7": "7. Your Rights and Choices",
        "sec7_body": "- Contact your organization’s administrator to request access, correction, or deletion where applicable.",
        "sec8": "8. Contact",
        "sec8_body": "For privacy inquiries, please contact your organization’s BrainSAIT administrator or privacy office.",
        "footer": "This page is provided as a template. Customize per your organization’s legal guidance.",
    },
    "ar": {
        "title": "سياسة الخصوصية",
        "effective": "تاريخ السريان: {}",
        "intro": "توضح سياسة الخصوصية هذه كيفية قيام منصة BrainSAIT بجمع المعلومات واستخدامها وحمايتها. تم تصميمها لبيئات الرعاية الصحية وتهدف إلى التوافق مع HIPAA واللوائح المحلية.",
        "sec1": "1. المعلومات التي نجمعها",
        "sec1_body": "- معلومات صحية أو شخصية يوفرها المستخدمون أو الأنظمة (مثل FHIR/EHR، مطالبات NPHIES).\n- بيانات وصفية تشغيلية وسجلات تدقيق للامتثال.\n- بيانات التهيئة والتكامل (مثل عناوين الخدمات ومفاتيح API).",
        "sec2": "2. كيفية استخدام المعلومات",
        "sec2_body": "- لتقديم دعم القرار السريري والتحقق من المطالبات وأتمتة سير العمل.\n- للحفاظ على الأمان وقابلية التدقيق والامتثال التنظيمي.\n- لتحسين موثوقية النظام وتجربة المستخدم.",
        "sec3": "3. أمان البيانات والامتثال",
        "sec3_body": "- تشفير أثناء النقل والتخزين حيثما أمكن.\n- تسجيل تدقيق متوافق مع HIPAA (قابل للتهيئة عبر البيئة).\n- ضوابط وصول متوافقة مع مبدأ أقل صلاحية.",
        "sec4": "4. الاحتفاظ بالبيانات",
        "sec4_body": "- فترات الاحتفاظ قابلة للتهيئة من قبل المؤسسة الناشرة.\n- يتم الاحتفاظ بسجلات التدقيق وفق السياسات والمتطلبات التنظيمية.",
        "sec5": "5. الخدمات الطرف الثالث",
        "sec5_body": "- قد تتكامل المنصة مع خدمات مثل NPHIES وخوادم FHIR وn8n وClaude وAtlassian.\n- يخضع استخدامك لشروط وسياسات هؤلاء المزودين.",
        "sec6": "6. اللوائح الدولية والمحلية",
        "sec6_body": "- يجب التحقق من توافق النشر مع اللوائح المحلية (مثل وزارة الصحة السعودية وسياسات NPHIES).",
        "sec7": "7. حقوقك وخياراتك",
        "sec7_body": "- تواصل مع مسؤول النظام لطلب الوصول أو التصحيح أو الحذف عند الاقتضاء.",
        "sec8": "8. تواصل معنا",
        "sec8_body": "للاستفسارات المتعلقة بالخصوصية، يرجى الاتصال بمسؤول BrainSAIT في مؤسستك أو مكتب الخصوصية.",
        "footer": "هذه الصفحة نموذج قابل للتخصيص وفق توجيهاتكم القانونية.",
    },
}

tr = T[lang]

st.title(tr["title"]) 
st.caption(tr["effective"].format(effective))

st.info(tr["intro"])

st.header(tr["sec1"]) ; st.markdown(tr["sec1_body"])
st.header(tr["sec2"]) ; st.markdown(tr["sec2_body"])
st.header(tr["sec3"]) ; st.markdown(tr["sec3_body"])
st.header(tr["sec4"]) ; st.markdown(tr["sec4_body"])
st.header(tr["sec5"]) ; st.markdown(tr["sec5_body"])
st.header(tr["sec6"]) ; st.markdown(tr["sec6_body"])
st.header(tr["sec7"]) ; st.markdown(tr["sec7_body"])
st.header(tr["sec8"]) ; st.markdown(tr["sec8_body"])

st.divider()
st.caption(tr["footer"])