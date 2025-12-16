import os
import json
import asyncio
import time
from typing import Dict, Any, Optional
from datetime import datetime

import streamlit as st
from langchain_openai.chat_models import ChatOpenAI

from brainsait_master import BrainSAITMasterLinc

# -------------------------
# Custom CSS for Enhanced UI/UX
# -------------------------

def load_custom_css():
    """Load custom CSS for beautiful, user-friendly interface"""
    st.markdown("""
        <style>
        /* Modern Card Design */
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        /* Main content area */
        .main .block-container {
            padding: 2rem 3rem;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 1400px;
        }
        
        /* Headers */
        h1 {
            color: #1e3a8a;
            font-weight: 700;
            font-size: 2.5rem !important;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        h2 {
            color: #3b82f6;
            font-weight: 600;
            border-bottom: 3px solid #3b82f6;
            padding-bottom: 0.5rem;
            margin-top: 2rem;
        }
        
        h3 {
            color: #6366f1;
            font-weight: 600;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        
        /* Input fields */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            padding: 0.75rem;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: #f8fafc;
            border-radius: 15px;
            padding: 0.5rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 10px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            color: #64748b;
            transition: all 0.3s ease;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white !important;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
            padding: 2rem 1rem;
        }
        
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label {
            color: white !important;
        }
        
        /* Success/Info/Warning boxes */
        .stSuccess, .stInfo, .stWarning, .stError {
            border-radius: 12px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background-color: #f1f5f9;
            border-radius: 10px;
            font-weight: 600;
            color: #334155;
        }
        
        /* Metrics */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
            color: #667eea;
        }
        
        /* Progress bar */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        }
        
        /* Cards effect for expanders */
        .streamlit-expanderContent {
            background-color: #f8fafc;
            border-radius: 0 0 10px 10px;
            padding: 1.5rem;
        }
        
        /* Tooltips */
        [data-testid="stTooltipIcon"] {
            color: #667eea;
        }
        
        /* Select boxes */
        .stSelectbox > div > div {
            border-radius: 10px;
        }
        
        /* Animation */
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .main .block-container > div {
            animation: slideIn 0.5s ease-out;
        }
        
        /* Loading spinner */
        .stSpinner > div {
            border-top-color: #667eea !important;
        }
        </style>
    """, unsafe_allow_html=True)

# -------------------------
# UI Helpers
# -------------------------

def log_debug(message: str):
    """Log debug messages with timestamp"""
    if "debug_logs" not in st.session_state:
        st.session_state["debug_logs"] = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    st.session_state["debug_logs"].append(f"[{timestamp}] {message}")

def show_welcome_wizard():
    """Interactive welcome wizard for first-time users"""
    if "wizard_completed" not in st.session_state:
        st.session_state["wizard_completed"] = False
    
    if not st.session_state["wizard_completed"]:
        st.markdown("### 👋 Welcome to BrainSAIT Healthcare AI Platform!")
        st.markdown("""
        This platform helps healthcare professionals with:
        - 🏥 **NPHIES Claims Processing** - Automated claim validation
        - 🩺 **Clinical Workflows** - Decision support and documentation
        - 🤖 **AI Assistants** - NVIDIA & OpenAI powered tools
        - 💬 **Smart Chat** - Ask questions in plain English or Arabic
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 Quick Start (Recommended)", use_container_width=True):
                st.session_state["wizard_completed"] = True
                st.session_state["show_quick_setup"] = True
                st.rerun()
        with col2:
            if st.button("⚙️ Advanced Setup", use_container_width=True):
                st.session_state["wizard_completed"] = True
                st.session_state["show_quick_setup"] = False
                st.rerun()
        
        st.info("💡 **Tip:** Start with Quick Start to get up and running in minutes!")
        return True
    return False

def show_quick_setup_guide():
    """Show quick setup guide for non-technical users"""
    if st.session_state.get("show_quick_setup"):
        with st.expander("🚀 Quick Setup Guide", expanded=True):
            st.markdown("""
            #### Get Started in 3 Easy Steps:
            
            **Step 1: Choose Your Tool** 🎯
            - Click on any tab above (NPHIES, Clinical, AI Chat)
            - Each tab has examples to get you started
            
            **Step 2: Enter Your API Key** 🔑
            - For LLM Chat: Enter OpenAI key in sidebar
            - For NVIDIA Tools: Add NVIDIA key in NVIDIA tab
            - Don't have keys? [Get OpenAI Key](https://platform.openai.com/api-keys)
            
            **Step 3: Try It Out!** ✨
            - Use the example data provided
            - Click the big colorful buttons
            - Results appear instantly below
            
            ---
            
            **Need Help?** 
            - 📘 Hover over any (?) icon for tips
            - 📊 Check "Debug Logs" tab to see what's happening
            - 💬 Use LLM Chat to ask questions
            """)
            
            if st.button("✓ Got it! Hide this guide"):
                st.session_state["show_quick_setup"] = False
                st.rerun()

def init_session_state():
    defaults = {
        "jira_site": "",
        "jira_email": "",
        "jira_token": "",
        "jira_project_key": "",
        "confluence_site": "",
        "confluence_email": "",
        "confluence_token": "",
        "confluence_space_key": "",
        "n8n_webhook_base": os.getenv("N8N_WEBHOOK_URL", ""),
        "nphies_endpoint": os.getenv("NPHIES_ENDPOINT", ""),
        "fhir_base_url": os.getenv("FHIR_BASE_URL", ""),
        "hipaa_audit_log": os.getenv("HIPAA_AUDIT_LOG", "audit.log"),
        "claude_api_key": os.getenv("CLAUDE_API_KEY", ""),
        "nvidia_rag_endpoint": os.getenv("NVIDIA_RAG_ENDPOINT", ""),
        "nvidia_ambient_endpoint": os.getenv("NVIDIA_AMBIENT_ENDPOINT", ""),
        "nvidia_ava_endpoint": os.getenv("NVIDIA_AVA_ENDPOINT", ""),
        "nvidia_api_key": os.getenv("NVIDIA_API_KEY", ""),
        "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
        "debug_logs": [],
        "wizard_completed": False,
        "show_quick_setup": True,
        "user_mode": "simple",  # simple or advanced
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def make_masterlinc() -> BrainSAITMasterLinc:
    config = {
        "NPHIES_ENDPOINT": st.session_state.get("nphies_endpoint"),
        "FHIR_BASE_URL": st.session_state.get("fhir_base_url"),
        "HIPAA_AUDIT_LOG": st.session_state.get("hipaa_audit_log", "audit.log"),
        "CLAUDE_API_KEY": st.session_state.get("claude_api_key"),
        "N8N_WEBHOOK_URL": st.session_state.get("n8n_webhook_base"),
    }
    return BrainSAITMasterLinc(config)


# -------------------------
# Atlassian REST minimal helpers (Cloud)
# -------------------------
import base64
import requests


def _basic_auth(email: str, token: str) -> Dict[str, str]:
    auth_str = f"{email}:{token}".encode()
    return {"Authorization": "Basic " + base64.b64encode(auth_str).decode()}


def create_jira_issue(site: str, email: str, token: str, project_key: str,
                      summary: str, description: str, issuetype: str = "Task") -> Dict[str, Any]:
    url = site.rstrip("/") + "/rest/api/3/issue"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    headers.update(_basic_auth(email, token))
    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "description": {"type": "doc", "version": 1, "content": [
                {"type": "paragraph", "content": [{"type": "text", "text": description}]}
            ]},
            "issuetype": {"name": issuetype}
        }
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    if resp.status_code not in (200, 201):
        raise RuntimeError(f"Jira create issue failed: {resp.status_code} {resp.text}")
    return resp.json()


def create_confluence_page(site: str, email: str, token: str, space_key: str,
                           title: str, body_html: str) -> Dict[str, Any]:
    # Confluence Cloud v1 REST
    base = site.rstrip("/")
    if not base.endswith("/wiki"):
        # Common Cloud base is https://<org>.atlassian.net/wiki
        base = base + "/wiki"
    url = base + "/rest/api/content"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    headers.update(_basic_auth(email, token))
    payload = {
        "type": "page",
        "title": title,
        "space": {"key": space_key},
        "body": {
            "storage": {
                "value": body_html,
                "representation": "storage"
            }
        }
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    if resp.status_code not in (200, 201):
        raise RuntimeError(f"Confluence create page failed: {resp.status_code} {resp.text}")
    return resp.json()


# -------------------------
# Sidebar Status
# -------------------------

def render_sidebar():
    with st.sidebar:
        # Logo and title
        st.markdown("""
            <div style='text-align: center; padding: 1rem 0;'>
                <h1 style='font-size: 2rem; margin: 0; color: white;'>🧠</h1>
                <h2 style='font-size: 1.3rem; margin: 0.5rem 0; color: white;'>BrainSAIT</h2>
                <p style='font-size: 0.9rem; color: #94a3b8; margin: 0;'>Healthcare AI Platform</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Language selector
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🇬🇧 EN", use_container_width=True, type="primary" if st.session_state.get("ui_language", "en")=="en" else "secondary"):
                st.session_state["ui_language"] = "en"
                st.rerun()
        with col2:
            if st.button("🇸🇦 AR", use_container_width=True, type="primary" if st.session_state.get("ui_language", "en")=="ar" else "secondary"):
                st.session_state["ui_language"] = "ar"
                st.rerun()
        
        st.divider()
        
        # System Status with progress
        st.markdown("### 📊 System Status")
        
        checks = {
            "OpenAI": bool(st.session_state.get("openai_api_key")),
            "NVIDIA": bool(st.session_state.get("nvidia_api_key")),
            "NPHIES": bool(st.session_state.get("nphies_endpoint")),
            "FHIR": bool(st.session_state.get("fhir_base_url")),
            "Jira": bool(st.session_state.get("jira_token")),
            "Confluence": bool(st.session_state.get("confluence_token")),
        }
        
        # Calculate readiness percentage
        total = len(checks)
        configured = sum(checks.values())
        readiness = (configured / total) * 100
        
        st.progress(readiness / 100)
        st.caption(f"**{readiness:.0f}% Ready** • {configured}/{total} configured")
        
        st.divider()
        
        # Essential services (collapsible)
        with st.expander("🔌 Essential Services", expanded=True):
            for name, status in list(checks.items())[:2]:  # OpenAI & NVIDIA
                if status:
                    st.success(f"✅ {name}")
                else:
                    st.error(f"⚪ {name}")
        
        # Optional services
        with st.expander("⚡ Optional Services", expanded=False):
            for name, status in list(checks.items())[2:]:
                st.write(f"{'✅' if status else '⚪'} {name}")
        
        # Quick actions
        st.divider()
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🔄 Refresh Status", use_container_width=True):
            st.rerun()
        
        if st.button("🗑️ Clear Logs", use_container_width=True):
            st.session_state["debug_logs"] = []
            st.success("Logs cleared!")
            time.sleep(1)
            st.rerun()
        
        if st.button("🔧 Reset Wizard", use_container_width=True, help="Show welcome wizard again"):
            st.session_state["wizard_completed"] = False
            st.rerun()
        
        # Footer links
        st.divider()
        st.markdown("### 📚 Resources")
        
        lang = st.session_state.get("ui_language", "en")
        st.page_link("pages/1_Privacy_Policy.py", label=("🛡️ Privacy" if lang=="en" else "🛡️ الخصوصية"))
        st.page_link("pages/2_Terms_of_Service.py", label=("📜 Terms" if lang=="en" else "📜 الشروط"))
        
        st.markdown("---")
        st.markdown("""
            <div style='text-align: center; font-size: 0.8rem; color: #94a3b8;'>
                <p>Made with ❤️ by <a href='https://github.com/fadil369' style='color: #667eea;'>@fadil369</a></p>
            </div>
        """, unsafe_allow_html=True)

# -------------------------
# Footer
# -------------------------

def render_footer():
    lang = st.session_state.get("ui_language", "en")
    # Title
    title = "BrainSAIT.AI • GIVC" if lang == "en" else "BrainSAIT.AI • مركز GIVC"
    st.divider()
    st.write(title)

    # Internal page links
    privacy_label = "🛡️ Privacy Policy" if lang == "en" else "🛡️ سياسة الخصوصية"
    terms_label = "📜 Terms of Service" if lang == "en" else "📜 شروط الخدمة"
    notfound_label = "🔍 404 Not Found" if lang == "en" else "🔍 الصفحة غير موجودة"

    cols = st.columns(3)
    with cols[0]:
        st.page_link("pages/1_Privacy_Policy.py", label=privacy_label)
    with cols[1]:
        st.page_link("pages/2_Terms_of_Service.py", label=terms_label)
    with cols[2]:
        st.page_link("pages/404_Not_Found.py", label=notfound_label)

    # External links
    st.markdown(
        " | ".join([
            "[GitHub @fadil369](https://github.com/fadil369)",
            "[elfadil.com](https://elfadil.com)",
            "[thefadil.site](https://thefadil.site)",
        ]),
        help=(
            "Community links" if lang == "en" else "روابط المجتمع"
        ),
    )


# -------------------------
# Pages
# -------------------------

def page_configuration():
    st.header("⚙️ Configuration")
    
    # User mode toggle
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.caption("Configure your integrations and API connections")
    with col2:
        user_mode = st.toggle("Advanced Mode", value=st.session_state.get("user_mode") == "advanced", key="mode_toggle")
        st.session_state["user_mode"] = "advanced" if user_mode else "simple"
    with col3:
        if st.button("🔄 Reset All", help="Clear all configuration"):
            for key in list(st.session_state.keys()):
                if key.endswith(("_token", "_key", "_site", "_email", "_endpoint", "_url")):
                    st.session_state[key] = ""
            st.success("Configuration cleared!")
            time.sleep(1)
            st.rerun()
    
    # Configuration status overview
    if st.session_state["user_mode"] == "simple":
        st.info("💡 **Simple Mode:** Only essential settings shown. Toggle 'Advanced Mode' for all options.")
    
    # Quick config status cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        openai_status = "✅" if st.session_state.get("openai_api_key") else "⚪"
        st.metric("OpenAI", openai_status, help="Required for LLM Chat")
    with col2:
        nvidia_status = "✅" if st.session_state.get("nvidia_api_key") else "⚪"
        st.metric("NVIDIA", nvidia_status, help="Required for NVIDIA tools")
    with col3:
        jira_status = "✅" if st.session_state.get("jira_token") else "⚪"
        st.metric("Jira", jira_status, help="Optional: For ticket creation")
    with col4:
        health_status = "✅" if st.session_state.get("nphies_endpoint") else "⚪"
        st.metric("Healthcare", health_status, help="Optional: For NPHIES/FHIR")

    st.divider()

    # Essential Configuration (Always visible)
    with st.expander("🔑 Essential API Keys", expanded=True):
        st.markdown("**These are the main keys you'll need to get started:**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.session_state["openai_api_key"] = st.text_input(
                "OpenAI API Key",
                st.session_state["openai_api_key"],
                type="password",
                help="Get your key from: https://platform.openai.com/api-keys",
                placeholder="sk-..."
            )
            if st.session_state.get("openai_api_key"):
                st.success("✓ OpenAI configured")
        
        with col2:
            st.session_state["nvidia_api_key"] = st.text_input(
                "NVIDIA API Key",
                st.session_state["nvidia_api_key"],
                type="password",
                help="Get your key from: https://build.nvidia.com",
                placeholder="nvapi-..."
            )
            if st.session_state.get("nvidia_api_key"):
                st.success("✓ NVIDIA configured")

    # Healthcare Systems (Simple mode)
    with st.expander("🏥 Healthcare Systems (Optional)", expanded=False):
        st.markdown("**Configure these if you're working with NPHIES/FHIR:**")
        
        st.session_state["nphies_endpoint"] = st.text_input(
            "NPHIES Endpoint",
            st.session_state["nphies_endpoint"],
            help="Saudi Arabia's NPHIES system endpoint",
            placeholder="https://nphies.sa/api/v1"
        )
        st.session_state["fhir_base_url"] = st.text_input(
            "FHIR Base URL",
            st.session_state["fhir_base_url"],
            help="Your FHIR server endpoint",
            placeholder="https://your-fhir-server.com/fhir"
        )
        
        if st.session_state["user_mode"] == "advanced":
            st.session_state["hipaa_audit_log"] = st.text_input(
                "HIPAA Audit Log File",
                st.session_state["hipaa_audit_log"],
                help="Local file path for audit logs"
            )
            st.session_state["claude_api_key"] = st.text_input(
                "Claude API Key (optional)",
                st.session_state["claude_api_key"],
                type="password",
                help="Anthropic Claude API key for advanced AI features"
            )

    # Advanced: Jira Cloud
    if st.session_state["user_mode"] == "advanced":
        with st.expander("📋 Jira Cloud Integration (Advanced)", expanded=False):
            st.markdown("**Connect to Jira for automatic ticket creation:**")
            st.session_state["jira_site"] = st.text_input(
                "Jira Site Base URL",
                st.session_state["jira_site"],
                placeholder="https://your-domain.atlassian.net"
            )
            st.session_state["jira_email"] = st.text_input(
                "Jira Email",
                st.session_state["jira_email"]
            )
            st.session_state["jira_token"] = st.text_input(
                "Jira API Token",
                st.session_state["jira_token"],
                type="password",
                help="Generate from: https://id.atlassian.com/manage-profile/security/api-tokens"
            )
            st.session_state["jira_project_key"] = st.text_input(
                "Default Project Key",
                st.session_state["jira_project_key"],
                placeholder="PROJ"
            )

        # Advanced: Confluence Cloud
        with st.expander("📝 Confluence Cloud Integration (Advanced)", expanded=False):
            st.markdown("**Connect to Confluence for documentation:**")
            st.session_state["confluence_site"] = st.text_input(
                "Confluence Base URL",
                st.session_state["confluence_site"],
                placeholder="https://your-domain.atlassian.net/wiki"
            )
            st.session_state["confluence_email"] = st.text_input(
                "Confluence Email",
                st.session_state["confluence_email"]
            )
            st.session_state["confluence_token"] = st.text_input(
                "Confluence API Token",
                st.session_state["confluence_token"],
                type="password"
            )
            st.session_state["confluence_space_key"] = st.text_input(
                "Default Space Key",
                st.session_state["confluence_space_key"],
                placeholder="SPACE"
            )

        # Advanced: n8n Automation
        with st.expander("🔗 n8n Automation (Advanced)", expanded=False):
            st.markdown("**Connect to n8n for workflow automation:**")
            st.session_state["n8n_webhook_base"] = st.text_input(
                "N8N Webhook Base URL",
                st.session_state["n8n_webhook_base"],
                placeholder="https://n8n.example.com/webhook"
            ) 
        st.session_state["confluence_space_key"] = st.text_input("Default Space Key", st.session_state["confluence_space_key"]) 

    st.success("Configuration saved in session. Use the other tabs to run workflows.")


def page_nphies_claims():
    st.header("NPHIES Claim Processing")
    st.caption("Validate a FHIR Claim and trigger n8n automation via MASTERLINC.")

    default_claim = {
        "resourceType": "Claim",
        "id": "example-claim-001",
        "status": "active",
        "type": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/claim-type", "code": "professional"}]},
        "patient": {"reference": "Patient/example"},
        "provider": {"reference": "Organization/example"},
        "insurance": [{"sequence": 1, "focal": True, "coverage": {"reference": "Coverage/example"}}],
    }
    claim_json = st.text_area("FHIR Claim JSON", value=json.dumps(default_claim, indent=2), height=280)
    user_role = st.selectbox("User Role", ["provider", "admin", "nurse", "auditor"], index=0)

    if st.button("Validate & Trigger n8n"):
        try:
            start_time = time.time()
            log_debug(f"Starting NPHIES claim validation for user_role={user_role}")
            
            claim_data = json.loads(claim_json)
            master = make_masterlinc()
            result = asyncio.run(master.process_nphies_claim(claim_data=claim_data, user_role=user_role))
            
            elapsed = time.time() - start_time
            log_debug(f"NPHIES claim processed in {elapsed:.2f}s")
            
            st.success(f"Claim processed successfully in {elapsed:.2f}s")
            st.json(result)

            with st.expander("Create Jira/Confluence from result", expanded=False):
                st.caption("Per your policy, creation requires explicit confirmation.")
                create_jira = st.checkbox("Create Jira issue", value=False)
                create_conf = st.checkbox("Create Confluence page", value=False)
                summary = st.text_input("Title / Summary", value=f"NPHIES Claim {claim_data.get('id', '')} processed")
                description = st.text_area("Description (used for Jira)", value=json.dumps(result, indent=2))
                conf_space = st.text_input("Confluence Space Key", value=st.session_state.get("confluence_space_key", ""))
                if st.button("Confirm & Create"):
                    created = {}
                    if create_jira:
                        created["jira"] = create_jira_issue(
                            st.session_state.get("jira_site", ""),
                            st.session_state.get("jira_email", ""),
                            st.session_state.get("jira_token", ""),
                            st.session_state.get("jira_project_key", ""),
                            summary,
                            description,
                        )
                    if create_conf:
                        body_html = f"<p><strong>Claim Processing Result</strong></p><pre>{json.dumps(result, indent=2)}</pre>"
                        created["confluence"] = create_confluence_page(
                            st.session_state.get("confluence_site", ""),
                            st.session_state.get("confluence_email", ""),
                            st.session_state.get("confluence_token", ""),
                            conf_space,
                            summary,
                            body_html,
                        )
                    st.success("Created:")
                    st.json(created)
        except Exception as e:
            st.error(f"Error: {e}")


def page_clinical_workflow():
    st.header("Clinical Decision Support")
    st.caption("Run clinical workflow with bilingual support.")

    workflow_type = st.selectbox("Workflow Type", ["diagnosis", "treatment", "radiology", "laboratory"], index=0)
    default_patient = {
        "resourceType": "Patient",
        "id": "patient-001",
        "name": [{"family": "Doe", "given": ["Jane"]}],
        "gender": "female",
        "birthDate": "1990-01-01",
        "communication": [{"language": {"coding": [{"code": "en"}]}, "preferred": True}],
    }
    patient_json = st.text_area("FHIR Patient JSON", value=json.dumps(default_patient, indent=2), height=260)
    bilingual = st.checkbox("Bilingual content (Arabic/English)", value=True)

    if st.button("Run Clinical Workflow"):
        try:
            start_time = time.time()
            log_debug(f"Starting clinical workflow: {workflow_type}, bilingual={bilingual}")
            
            patient_data = json.loads(patient_json)
            master = make_masterlinc()
            result = asyncio.run(master.orchestrate_clinical_workflow(
                workflow_type=workflow_type,
                patient_data=patient_data,
                bilingual_content=bilingual,
            ))
            
            elapsed = time.time() - start_time
            log_debug(f"Clinical workflow completed in {elapsed:.2f}s")
            
            st.success(f"Workflow executed in {elapsed:.2f}s")
            st.json(result)

            with st.expander("Create Jira/Confluence from result", expanded=False):
                st.caption("Creation requires explicit confirmation.")
                create_jira = st.checkbox("Create Jira issue", value=False, key="clinical_create_jira")
                create_conf = st.checkbox("Create Confluence page", value=False, key="clinical_create_conf")
                summary = st.text_input("Title / Summary", value=f"Clinical workflow: {workflow_type}", key="clinical_summary")
                description = st.text_area("Description (used for Jira)", value=json.dumps(result, indent=2), key="clinical_description")
                conf_space = st.text_input("Confluence Space Key", value=st.session_state.get("confluence_space_key", ""), key="clinical_space")
                if st.button("Confirm & Create", key="clinical_confirm"):
                    created = {}
                    if create_jira:
                        created["jira"] = create_jira_issue(
                            st.session_state.get("jira_site", ""),
                            st.session_state.get("jira_email", ""),
                            st.session_state.get("jira_token", ""),
                            st.session_state.get("jira_project_key", ""),
                            summary,
                            description,
                        )
                    if create_conf:
                        body_html = f"<p><strong>Clinical Workflow Result</strong></p><pre>{json.dumps(result, indent=2)}</pre>"
                        created["confluence"] = create_confluence_page(
                            st.session_state.get("confluence_site", ""),
                            st.session_state.get("confluence_email", ""),
                            st.session_state.get("confluence_token", ""),
                            conf_space,
                            summary,
                            body_html,
                        )
                    st.success("Created:")
                    st.json(created)
        except Exception as e:
            st.error(f"Error: {e}")


def page_llm_chat():
    st.header("💬 AI Chat Assistant")
    st.caption("Ask anything! I can help with healthcare, FHIR, coding, or general questions.")
    
    # Check API key status
    has_api_key = st.session_state.get("openai_api_key", "").startswith("sk-")
    
    if not has_api_key:
        st.warning("⚠️ **OpenAI API Key Required**")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.info("👉 Go to **Configuration** tab → **Essential API Keys** → Enter your OpenAI key")
        with col2:
            if st.button("🔑 Go to Configuration", use_container_width=True):
                st.session_state["show_config_hint"] = True
        st.markdown("---")
        st.markdown("**Don't have an API key?**")
        st.markdown("1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)")
        st.markdown("2. Sign up or log in")
        st.markdown("3. Create a new API key")
        st.markdown("4. Copy and paste it in the Configuration tab")
        return
    
    # Quick action buttons
    st.markdown("### 🎯 Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    quick_prompts = {
        "🏥 NPHIES Help": "Explain how NPHIES claim validation works in Saudi Arabia and what are the key requirements.",
        "📋 FHIR Guide": "How do I create a FHIR Patient resource? Show me an example with all required fields.",
        "🩺 Clinical Workflow": "What are the best practices for clinical documentation in healthcare IT systems?"
    }
    
    selected_prompt = None
    with col1:
        if st.button("🏥 NPHIES Help", use_container_width=True, help="Learn about NPHIES claims"):
            selected_prompt = quick_prompts["🏥 NPHIES Help"]
    with col2:
        if st.button("📋 FHIR Guide", use_container_width=True, help="Get FHIR resources help"):
            selected_prompt = quick_prompts["📋 FHIR Guide"]
    with col3:
        if st.button("🩺 Clinical Workflow", use_container_width=True, help="Clinical best practices"):
            selected_prompt = quick_prompts["🩺 Clinical Workflow"]
    
    st.divider()
    
    def generate_response(input_text):
        """Generate AI response using OpenAI"""
        try:
            with st.spinner("🤔 Thinking..."):
                start_time = time.time()
                log_debug(f"LLM Chat query: '{input_text[:50]}...'")
                
                model = ChatOpenAI(
                    temperature=0.7, 
                    api_key=st.session_state["openai_api_key"],
                    model="gpt-3.5-turbo"
                )
                response = model.invoke(input_text)
                
                elapsed = time.time() - start_time
                log_debug(f"LLM response generated in {elapsed:.2f}s")
            
            # Show response in a nice format
            st.markdown("### 💡 Answer")
            st.markdown(response.content if hasattr(response, 'content') else str(response))
            st.caption(f"⏱️ Response time: {elapsed:.2f}s")
            
            return response
        except Exception as e:
            log_debug(f"LLM error: {str(e)}")
            st.error(f"❌ Error: {e}")
            if "api_key" in str(e).lower():
                st.info("💡 Check your API key in the Configuration tab")
            return None

    # Main chat interface
    st.markdown("### ✍️ Your Question")
    
    # Use selected prompt or default
    default_text = selected_prompt if selected_prompt else ""
    
    text = st.text_area(
        "Type your question here:",
        value=default_text,
        height=150,
        placeholder="Example: How do I validate a FHIR Claim resource for NPHIES?",
        help="Ask anything! Healthcare, FHIR, NPHIES, coding, or general questions",
        label_visibility="collapsed"
    )
    
    # Example prompts
    with st.expander("💡 Example Questions", expanded=False):
        st.markdown("""
        **Healthcare & NPHIES:**
        - What are the required fields for NPHIES claim submission?
        - How does HIPAA compliance work in healthcare applications?
        - Explain the difference between ICD-10 and CPT codes
        
        **FHIR Resources:**
        - Create an example FHIR Patient resource
        - How to link a Claim to a Patient in FHIR?
        - What's the structure of a FHIR Observation?
        
        **Technical Help:**
        - How do I integrate with a FHIR server?
        - Best practices for API authentication in healthcare
        - Explain OAuth 2.0 for healthcare APIs
        
        **General:**
        - Explain machine learning in healthcare
        - What is Natural Language Processing?
        - How does AI help in clinical decision support?
        """)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        submit_button = st.button("🚀 Ask Question", use_container_width=True, type="primary")
    with col2:
        clear_button = st.button("🔄 Clear", use_container_width=True)
    with col3:
        lang_toggle = st.toggle("🌐 AR", help="Answer in Arabic")
    
    if clear_button:
        st.rerun()
    
    if submit_button and text.strip():
        # Add language instruction if Arabic
        if lang_toggle:
            text = f"Please answer in Arabic: {text}"
        
        response = generate_response(text)
        
        # Optional: Create Jira/Confluence from chat
        if response:
            with st.expander("📋 Save to Jira/Confluence", expanded=False):
                create_jira = st.checkbox("Create Jira issue", value=False, key="llm_create_jira")
                create_conf = st.checkbox("Create Confluence page", value=False, key="llm_create_conf")
                summary = st.text_input("Title", value=f"LLM Chat: {text[:50]}...", key="llm_summary")
                
                if st.button("Save", key="llm_save"):
                    created = {}
                    response_text = response.content if hasattr(response, 'content') else str(response)
                    description = f"Query: {text}\n\nResponse:\n{response_text}"
                    
                    if create_jira:
                        created["jira"] = create_jira_issue(
                            st.session_state.get("jira_site", ""),
                            st.session_state.get("jira_email", ""),
                            st.session_state.get("jira_token", ""),
                            st.session_state.get("jira_project_key", ""),
                            summary,
                                description,
                            )
                        if create_conf:
                            body_html = f"<h3>Query</h3><p>{text}</p><h3>Response</h3><pre>{response_text}</pre>"
                            created["confluence"] = create_confluence_page(
                                st.session_state.get("confluence_site", ""),
                                st.session_state.get("confluence_email", ""),
                                st.session_state.get("confluence_token", ""),
                                st.session_state.get("confluence_space_key", ""),
                                summary,
                                body_html,
                            )
                        st.success("Saved successfully!")
                        st.json(created)


def page_nvidia_integrations():
    st.header("NVIDIA AI Blueprints")
    st.caption("Run RAG, Ambient Healthcare Agent, and AI Virtual Assistant via MasterLinc.")

    with st.expander("⚙️ Configure NVIDIA Endpoints", expanded=False):
        st.caption("Configure NVIDIA API endpoints and credentials (saved to session)")
        st.session_state["nvidia_api_key"] = st.text_input(
            "NVIDIA API Key", 
            st.session_state.get("nvidia_api_key", ""),
            type="password",
            help="Your NVIDIA API key for accessing blueprints"
        )
        st.session_state["nvidia_rag_endpoint"] = st.text_input(
            "RAG Endpoint", 
            st.session_state.get("nvidia_rag_endpoint", ""),
            placeholder="https://api.nvidia.com/rag/v1"
        )
        st.session_state["nvidia_ambient_endpoint"] = st.text_input(
            "Ambient Healthcare Endpoint", 
            st.session_state.get("nvidia_ambient_endpoint", ""),
            placeholder="https://api.nvidia.com/ambient/v1"
        )
        st.session_state["nvidia_ava_endpoint"] = st.text_input(
            "AI Virtual Assistant Endpoint", 
            st.session_state.get("nvidia_ava_endpoint", ""),
            placeholder="https://api.nvidia.com/ava/v1"
        )
        if st.button("Save NVIDIA Config to .env"):
            try:
                env_content = f"""# NVIDIA Configuration - Generated {datetime.now().isoformat()}
NVIDIA_API_KEY={st.session_state.get('nvidia_api_key', '')}
NVIDIA_RAG_ENDPOINT={st.session_state.get('nvidia_rag_endpoint', '')}
NVIDIA_AMBIENT_ENDPOINT={st.session_state.get('nvidia_ambient_endpoint', '')}
NVIDIA_AVA_ENDPOINT={st.session_state.get('nvidia_ava_endpoint', '')}
"""
                with open(".env", "a") as f:
                    f.write(env_content)
                st.success("NVIDIA config appended to .env file")
                log_debug("NVIDIA config saved to .env")
            except Exception as e:
                st.error(f"Failed to save .env: {e}")

    master = make_masterlinc()

    st.subheader("RAG Query")
    rag_query = st.text_input("Query", "What are NPHIES claim required fields?")
    rag_corpus = st.text_input("Corpus (optional)", "")
    rag_topk = st.number_input("Top K", min_value=1, max_value=50, value=5)
    if st.button("Run RAG"):
        try:
            start_time = time.time()
            log_debug(f"RAG query: '{rag_query}', top_k={rag_topk}")
            
            result = asyncio.run(master.query_nvidia_rag(query=rag_query, corpus=rag_corpus or None, top_k=int(rag_topk)))
            
            elapsed = time.time() - start_time
            log_debug(f"RAG completed in {elapsed:.2f}s")
            
            st.success(f"Query completed in {elapsed:.2f}s")
            st.json(result)
        except Exception as e:
            log_debug(f"RAG error: {str(e)}")
            st.error(f"RAG error: {e}")

    st.subheader("Ambient Healthcare Agent")
    ambient_transcript = st.text_area("Transcript", "Patient reports mild chest pain for 2 hours...")
    ambient_task = st.selectbox("Task", ["summarize", "sbar", "soap", "codify"])
    if st.button("Run Ambient Agent"):
        try:
            start_time = time.time()
            log_debug(f"Ambient agent task: {ambient_task}")
            
            result = asyncio.run(master.run_ambient_healthcare_agent(transcript=ambient_transcript, task=ambient_task))
            
            elapsed = time.time() - start_time
            log_debug(f"Ambient agent completed in {elapsed:.2f}s")
            
            st.success(f"Task completed in {elapsed:.2f}s")
            st.json(result)
        except Exception as e:
            log_debug(f"Ambient agent error: {str(e)}")
            st.error(f"Ambient agent error: {e}")

    st.subheader("AI Virtual Assistant")
    ava_intent = st.text_input("Intent", "triage_patient")
    ava_payload = st.text_area("Payload (JSON)", "{}")
    if st.button("Run Assistant"):
        try:
            start_time = time.time()
            log_debug(f"AI Assistant intent: {ava_intent}")
            
            payload = json.loads(ava_payload or "{}")
            result = asyncio.run(master.run_ai_virtual_assistant(intent=ava_intent, payload=payload))
            
            elapsed = time.time() - start_time
            log_debug(f"AI Assistant completed in {elapsed:.2f}s")
            
            st.success(f"Intent processed in {elapsed:.2f}s")
            st.json(result)
        except Exception as e:
            log_debug(f"AI Assistant error: {str(e)}")
            st.error(f"Assistant error: {e}")


# -------------------------
# App Entry
# -------------------------

def main():
    st.set_page_config(
        page_title="BrainSAIT Healthcare AI Platform", 
        page_icon="🧠", 
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/fadil369',
            'About': "# BrainSAIT AI\nHealthcare AI Platform powered by OpenAI & NVIDIA"
        }
    )
    
    # Load custom CSS
    load_custom_css()
    
    init_session_state()
    
    # Show welcome wizard for first-time users
    if show_welcome_wizard():
        return
    
    render_sidebar()
    
    # Show quick setup guide
    show_quick_setup_guide()
    
    # Main title with gradient effect
    st.markdown("""
        <h1 style='text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
        font-size: 3rem; font-weight: 800; margin-bottom: 0.5rem;'>
        🧠 BrainSAIT Healthcare AI
        </h1>
        <p style='text-align: center; color: #64748b; font-size: 1.2rem; margin-bottom: 2rem;'>
        Intelligent Healthcare Workflows | NPHIES | FHIR | AI Assistants
        </p>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["⚙️ Configuration", "🏥 NPHIES Claims", "🩺 Clinical Workflow", "🤖 NVIDIA AI", "💬 Chat Assistant", "📊 Debug Logs"])

    with tabs[0]:
        page_configuration()
        render_footer()
    with tabs[1]:
        page_nphies_claims()
        render_footer()
    with tabs[2]:
        page_clinical_workflow()
        render_footer()
    with tabs[3]:
        page_nvidia_integrations()
        render_footer()
    with tabs[4]:
        page_llm_chat()
        render_footer()
    with tabs[5]:
        st.header("Debug Logs")
        st.caption("Real-time execution logs with timestamps")
        
        if st.session_state.get("debug_logs"):
            log_text = "\n".join(st.session_state["debug_logs"][-100:])  # Last 100 entries
            st.text_area("Logs", value=log_text, height=400, disabled=True)
            
            if st.button("Download Logs"):
                log_content = "\n".join(st.session_state["debug_logs"])
                st.download_button(
                    label="Save as TXT",
                    data=log_content,
                    file_name=f"brainsait_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
        else:
            st.info("No debug logs yet. Run operations to generate logs.")


if __name__ == "__main__":
    main()
