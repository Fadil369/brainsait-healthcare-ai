# 🧠 BrainSAIT Healthcare AI Platform

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Intelligent Healthcare Workflows powered by OpenAI & NVIDIA AI**

![BrainSAIT Platform](https://img.shields.io/badge/Healthcare-AI%20Platform-purple?style=for-the-badge)

---

## ✨ Features

### 🏥 Healthcare Workflows
- **NPHIES Claims Processing** - Automated validation for Saudi healthcare system
- **Clinical Decision Support** - AI-powered clinical workflows
- **FHIR Integration** - Full HL7 FHIR R4 support
- **HIPAA Compliance** - Secure audit logging and data handling

### 🤖 AI Assistants
- **OpenAI Chat** - GPT-powered healthcare Q&A
- **NVIDIA RAG** - Knowledge retrieval from medical documents
- **Ambient Healthcare Agent** - Clinical documentation automation
- **AI Virtual Assistant** - Patient triage and support

### 🎨 User Experience
- **Beautiful Modern UI** - Gradient design with smooth animations
- **Welcome Wizard** - Guided onboarding for first-time users
- **Simple/Advanced Modes** - Complexity control for all skill levels
- **Bilingual Support** - English & Arabic interface
- **Quick Actions** - Pre-built prompts and templates

### 🔗 Integrations
- **Jira** - Automatic issue creation
- **Confluence** - Documentation generation
- **n8n** - Workflow automation
- **Multiple AI Providers** - OpenAI, NVIDIA, Claude

---

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Fadil369/brainsait-healthcare-ai.git
   cd brainsait-healthcare-ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   ```
   http://localhost:8501
   ```

### Deploy to Streamlit Cloud

See **[STREAMLIT_DEPLOYMENT.md](STREAMLIT_DEPLOYMENT.md)** for detailed deployment instructions.

**Quick Deploy:**
1. Go to https://share.streamlit.io
2. Connect this repository
3. Set `app.py` as main file
4. Add your API keys in secrets
5. Deploy! 🎉

---

## 📋 Requirements

- Python 3.13+
- OpenAI API key (for LLM Chat)
- NVIDIA API key (optional, for NVIDIA AI tools)
- Streamlit

See [requirements.txt](requirements.txt) for full list.

---

## 🎯 Use Cases

### For Healthcare Providers
- Validate NPHIES claims before submission
- Get clinical decision support
- Automate documentation
- Query medical knowledge base

### For Administrators
- Monitor system integrations
- Configure API connections
- Track audit logs
- Manage workflows

### For Developers
- Integrate with FHIR servers
- Build healthcare automations
- Extend with custom workflows
- Add new AI capabilities

---

## 📚 Documentation

- **[Deployment Guide](STREAMLIT_DEPLOYMENT.md)** - How to deploy to Streamlit Cloud
- **[UI/UX Enhancements](UI_UX_ENHANCEMENTS.md)** - Design documentation
- **[LLM Integration](LLM_INTEGRATION_COMPLETE.md)** - OpenAI integration details

---

## 🛠️ Tech Stack

- **Framework**: Streamlit
- **AI/ML**: OpenAI GPT, NVIDIA NIM, LangChain
- **Healthcare**: HL7 FHIR, NPHIES
- **Integration**: Jira API, Confluence API, n8n
- **Security**: HIPAA-compliant audit logging, Encryption

---

## 🔐 Security & Compliance

- ✅ HIPAA-compliant audit logging
- ✅ Encrypted sensitive data
- ✅ Secure API key management
- ✅ Role-based access control
- ✅ Session-based configuration (no persistence)

---

## 🌐 Environment Variables

Configure these in Streamlit Cloud secrets or local `.env`:

```bash
# Essential
OPENAI_API_KEY=sk-...
NVIDIA_API_KEY=nvapi-...

# Optional
NPHIES_ENDPOINT=https://...
FHIR_BASE_URL=https://...
CLAUDE_API_KEY=sk-ant-...
N8N_WEBHOOK_URL=https://...
```

---

## 📸 Screenshots

### Welcome Wizard
First-time users get a guided onboarding experience.

### LLM Chat Assistant
Ask questions about healthcare, FHIR, or anything else.

### Configuration Dashboard
Simple mode for beginners, advanced mode for power users.

### System Status
Real-time monitoring with visual progress indicators.

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 👨‍💻 Author

**Fadil Ahmed**
- GitHub: [@Fadil369](https://github.com/Fadil369)
- Website: [elfadil.com](https://elfadil.com)
- Portfolio: [thefadil.site](https://thefadil.site)

---

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [OpenAI](https://openai.com/)
- NVIDIA AI integrations via [NVIDIA NIM](https://build.nvidia.com/)
- Healthcare standards: [HL7 FHIR](https://fhir.org/), [NPHIES](https://nphies.sa/)

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Fadil369/brainsait-healthcare-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Fadil369/brainsait-healthcare-ai/discussions)
- **Email**: Contact via GitHub profile

---

**Made with ❤️ for Healthcare Professionals**

*Simplifying healthcare technology, one workflow at a time.*
