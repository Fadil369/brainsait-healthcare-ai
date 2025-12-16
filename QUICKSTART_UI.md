# BrainSAIT MasterLinc UI - Quick Start Guide

## Prerequisites
1. Python 3.8+ installed
2. Virtual environment created at `~/.brainsait/brainsait_env`
3. Dependencies installed (see setup.sh)

## Installation

### Option 1: Using setup.sh (Recommended)
```bash
cd /Users/fadil369/mcp-linc
bash setup.sh
```

### Option 2: Manual Setup
```bash
# Create virtual environment
python3 -m venv ~/.brainsait/brainsait_env

# Activate it
source ~/.brainsait/brainsait_env/bin/activate

# Install dependencies
pip install streamlit requests anthropic

# Install additional dependencies if needed
pip install -r requirements.txt  # if requirements.txt exists
```

## Running the UI

```bash
# 1. Activate virtual environment
source ~/.brainsait/brainsait_env/bin/activate

# 2. Navigate to repo
cd /Users/fadil369/mcp-linc

# 3. Run Streamlit
streamlit run app.py

# The UI will open in your browser at http://localhost:8501
```

## UI Features

### 📊 Sidebar
- **Environment Status**: Shows if virtual env is active
- **Quick Checks**: Visual indicators for configured services
- **NVIDIA Repos**: Detection of cloned NVIDIA blueprint repos
- **Clear Logs**: Reset debug logs

### 🔧 Configuration Tab
Configure connections for:
- **n8n**: Webhook URL for workflow automation
- **NPHIES**: Saudi Healthcare payer endpoint
- **FHIR**: FHIR server base URL
- **HIPAA**: Audit log file path
- **Claude**: API key for AI processing
- **Jira Cloud**: Site, email, token, project key
- **Confluence Cloud**: Site, email, token, space key

### 💳 NPHIES Claims Tab
- Validate FHIR Claims
- Trigger n8n workflows
- User role-based processing
- Optional Jira/Confluence creation
- Execution timing displayed

### 🏥 Clinical Workflow Tab
- Run decision support workflows
- Types: diagnosis, treatment, radiology, laboratory
- Bilingual Arabic/English support
- Optional Jira/Confluence documentation
- Execution timing displayed

### 🤖 NVIDIA Integrations Tab
**Configuration Panel** (new):
- NVIDIA API Key
- RAG Endpoint URL
- Ambient Healthcare Endpoint URL
- AI Virtual Assistant Endpoint URL
- Save to .env button

**Operations**:
- **RAG Query**: Query knowledge base with configurable top-k
- **Ambient Healthcare Agent**: Process transcripts (summarize, sbar, soap, codify)
- **AI Virtual Assistant**: Execute intents with custom payloads

All operations show execution time and log to debug tab.

### 🐛 Debug Logs Tab (new)
- Real-time log viewer with timestamps
- Last 100 log entries displayed
- Download logs as TXT file
- Execution timing for all operations
- Error tracking and troubleshooting

## Environment Variables

Create a `.env` file in the repo root or set these in your environment:

```bash
# Healthcare
N8N_WEBHOOK_URL=https://n8n.example.com/webhook
NPHIES_ENDPOINT=https://api.nphies.sa
FHIR_BASE_URL=https://fhir.example.com
HIPAA_AUDIT_LOG=./audit.log

# AI Services
CLAUDE_API_KEY=sk-ant-...
NVIDIA_API_KEY=nvapi-...

# NVIDIA Endpoints
NVIDIA_RAG_ENDPOINT=https://api.nvidia.com/rag/v1
NVIDIA_AMBIENT_ENDPOINT=https://api.nvidia.com/ambient/v1
NVIDIA_AVA_ENDPOINT=https://api.nvidia.com/ava/v1
```

## Testing NVIDIA Integration

```bash
# Activate venv
source ~/.brainsait/brainsait_env/bin/activate

# Run NVIDIA test (if brainsait-cli exists)
brainsait-cli nvidia-test

# Or manually test imports
python3 -c "
try:
    import sys
    sys.path.append('nvidia-rag-canonical')
    sys.path.append('nvidia-ambient-healthcare-agent')
    sys.path.append('nvidia-ai-virtual-assistant')
    print('✅ NVIDIA repos accessible')
except Exception as e:
    print(f'⚠️ NVIDIA repos not found: {e}')
"
```

## Troubleshooting

### Virtual Environment Not Active
```bash
# Activate it
source ~/.brainsait/brainsait_env/bin/activate

# Verify
echo $VIRTUAL_ENV
```

### Streamlit Not Installed
```bash
pip install streamlit
```

### Port Already in Use
```bash
# Use different port
streamlit run app.py --server.port 8502
```

### NVIDIA Operations Fail
- Ensure NVIDIA repos are cloned in the current directory
- Check NVIDIA API key is configured
- Verify endpoints are correct
- Check debug logs tab for detailed errors

### Import Errors
```bash
# Install all dependencies
pip install streamlit requests anthropic
```

## Advanced Usage

### Custom Port
```bash
streamlit run app.py --server.port 8888
```

### Disable Browser Auto-Open
```bash
streamlit run app.py --server.headless true
```

### Enable Debug Mode
```bash
streamlit run app.py --logger.level debug
```

### Background Mode
```bash
nohup streamlit run app.py > streamlit.log 2>&1 &
```

## Support

For issues or questions:
1. Check Debug Logs tab in UI
2. Review `streamlit.log` if running in background
3. Verify configuration in Configuration tab
4. Check sidebar status indicators
5. Review PR_UI_ENHANCEMENTS.md for recent changes

---

**Version**: 1.0.0 (Enhanced UI with sidebar, NVIDIA config, and debug logging)
**Last Updated**: 2024-12-16
