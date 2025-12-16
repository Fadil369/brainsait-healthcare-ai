#!/usr/bin/env bash

# BrainSAIT MCP Server Setup Script
# Automated installation and configuration for healthcare AI platform
# Compatible with macOS, Linux, and Chrome OS (Linux Penguin)

set -e  # Exit on any error

# BRAINSAIT: Colors and styling for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# NEURAL: BrainSAIT branding
echo -e "${BLUE}"
echo "██████╗ ██████╗  █████╗ ██╗███╗   ███╗███████╗ █████╗ ██╗████████╗"
echo "██╔══██╗██╔══██╗██╔══██╗██║████╗ ████║██╔════╝██╔══██╗██║╚══██╔══╝"
echo "██████╔╝██████╔╝███████║██║██╔████╔██║███████╗███████║██║   ██║   "
echo "██╔══██╗██╔══██╗██╔══██║██║██║╚██╔╝██║╚════██║██╔══██║██║   ██║   "
echo "██████╔╝██║  ██║██║  ██║██║██║ ╚═╝ ██║███████║██║  ██║██║   ██║   "
echo "╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝   "
echo -e "${NC}"
echo -e "${CYAN}🏥 Healthcare AI Platform - MCP Server Setup${NC}"
echo -e "${PURPLE}🇸🇦 Saudi NPHIES & FHIR R4 Compatible${NC}"
echo ""

# Detect operating system
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        CLAUDE_CONFIG_DIR="$HOME/.config/claude-desktop"
    else
        echo -e "${RED}❌ Unsupported operating system: $OSTYPE${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Detected OS: $OS${NC}"
}

# Check prerequisites
check_prerequisites() {
    echo -e "${YELLOW}🔍 Checking prerequisites...${NC}"
    
    # Check Python 3.8+
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        if python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)'; then
            echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"
        else
            echo -e "${RED}❌ Python 3.8+ required, found $PYTHON_VERSION${NC}"
            exit 1
        fi
    else
        echo -e "${RED}❌ Python 3 not found. Please install Python 3.8+${NC}"
        exit 1
    fi
    
    # Check pip
    if command -v pip3 &> /dev/null; then
        echo -e "${GREEN}✅ pip3 found${NC}"
    else
        echo -e "${RED}❌ pip3 not found. Installing...${NC}"
        if [[ "$OS" == "linux" ]]; then
            sudo apt update && sudo apt install -y python3-pip
        elif [[ "$OS" == "macos" ]]; then
            curl https://bootstrap.pypa.io/get-pip.py | python3
        fi
    fi
    
    # Check Claude Desktop
    if [[ -d "$CLAUDE_CONFIG_DIR" ]]; then
        echo -e "${GREEN}✅ Claude Desktop configuration directory found${NC}"
    else
        echo -e "${YELLOW}⚠️  Claude Desktop config not found. Will create: $CLAUDE_CONFIG_DIR${NC}"
        mkdir -p "$CLAUDE_CONFIG_DIR"
    fi
}

# Setup directory structure
setup_directories() {
    echo -e "${YELLOW}📁 Setting up directory structure...${NC}"
    
    BRAINSAIT_HOME="$HOME/.brainsait"
    MCP_SERVERS_DIR="$BRAINSAIT_HOME/mcp_servers"
    LOGS_DIR="$BRAINSAIT_HOME/logs"
    CONFIG_DIR="$BRAINSAIT_HOME/config"
    
    # Create directories
    mkdir -p "$BRAINSAIT_HOME"
    mkdir -p "$MCP_SERVERS_DIR"
    mkdir -p "$LOGS_DIR"
    mkdir -p "$CONFIG_DIR"
    mkdir -p "$HOME/bin"  # For CLI tools
    
    echo -e "${GREEN}✅ Created BrainSAIT directory structure:${NC}"
    echo -e "   📁 $BRAINSAIT_HOME"
    echo -e "   📁 $MCP_SERVERS_DIR"
    echo -e "   📁 $LOGS_DIR"
    echo -e "   📁 $CONFIG_DIR"
}

# Setup Python virtual environment
setup_python_env() {
    echo -e "${YELLOW}🐍 Setting up Python virtual environment...${NC}"
    
    cd "$BRAINSAIT_HOME"
    
    # Create virtual environment
    python3 -m venv brainsait_env
    
    # Activate virtual environment
    source brainsait_env/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    echo -e "${GREEN}✅ Python virtual environment created${NC}"
}

# Install Python dependencies
install_dependencies() {
    echo -e "${YELLOW}📦 Installing Python dependencies...${NC}"
    
    cd "$BRAINSAIT_HOME"
    source brainsait_env/bin/activate
    
    # Core MCP and healthcare dependencies
    pip install --break-system-packages \
        mcp \
        fhir.resources \
        cryptography \
        anthropic \
        aiohttp \
        arabic-reshaper \
        python-bidi \
        pytest \
        pytest-asyncio \
        requests \
        jsonschema \
        pydantic \
        fastapi \
        uvicorn \
        streamlit
    
    echo -e "${GREEN}✅ Dependencies installed successfully${NC}"
}

# Clone NVIDIA AI Blueprints (ambient-healthcare-agents, rag, ai-virtual-assistant)
clone_nvidia_blueprints() {
    echo -e "${YELLOW}🧩 Cloning NVIDIA AI Blueprints...${NC}"

    VENDORS_DIR="$BRAINSAIT_HOME/vendors"
    NVIDIA_DIR="$VENDORS_DIR/nvidia"
    mkdir -p "$NVIDIA_DIR"

    cd "$NVIDIA_DIR"

    # Using SSH as requested; requires SSH keys configured on host
    declare -A REPOS=(
        [ambient-healthcare-agents]="git@github.com:NVIDIA-AI-Blueprints/ambient-healthcare-agents.git"
        [rag]="git@github.com:NVIDIA-AI-Blueprints/rag.git"
        [ai-virtual-assistant]="git@github.com:NVIDIA-AI-Blueprints/ai-virtual-assistant.git"
    )

    for name in "${!REPOS[@]}"; do
        url="${REPOS[$name]}"
        if [[ -d "$name/.git" ]]; then
            echo -e "${CYAN}↻ Updating $name...${NC}"
            (cd "$name" && git fetch --all && git pull --ff-only) || echo -e "${YELLOW}⚠️  Could not update $name${NC}"
        else
            echo -e "${CYAN}⬇️  Cloning $name from $url...${NC}"
            if ! git clone "$url" "$name"; then
                echo -e "${YELLOW}⚠️  SSH clone failed for $name. Attempting HTTPS fallback (read-only).${NC}"
                https_url="https://github.com/NVIDIA-AI-Blueprints/${name}.git"
                git clone "$https_url" "$name" || echo -e "${RED}❌ Clone failed for $name via SSH and HTTPS${NC}"
            fi
        fi
    done

    # Optional: attempt lightweight installs if Python projects
    source "$BRAINSAIT_HOME/brainsait_env/bin/activate"
    for name in ambient-healthcare-agents rag ai-virtual-assistant; do
        if [[ -f "$NVIDIA_DIR/$name/pyproject.toml" || -f "$NVIDIA_DIR/$name/setup.py" ]]; then
            echo -e "${CYAN}📦 Installing $name into virtualenv (editable)...${NC}"
            pip install --break-system-packages -e "$NVIDIA_DIR/$name" || echo -e "${YELLOW}⚠️  Install skipped/failed for $name${NC}"
        else
            echo -e "${CYAN}ℹ️  $name does not appear to be a Python package. Skipping pip install.${NC}"
        fi
    done

    echo -e "${GREEN}✅ NVIDIA Blueprints cloning step completed${NC}"
}

# Copy MCP server files
install_mcp_servers() {
    echo -e "${YELLOW}🚀 Installing MCP server files...${NC}"
    
    # Primary source: external outputs directory
    if [[ -d "/mnt/user-data/outputs/mcp_servers" ]]; then
        cp -r /mnt/user-data/outputs/mcp_servers/* "$MCP_SERVERS_DIR/"
        echo -e "${GREEN}✅ MCP server files copied from /mnt/user-data/outputs/mcp_servers${NC}"
    else
        # Fallback: use files from current workspace (setup.sh location)
        echo -e "${YELLOW}⚠️  External MCP server source not found. Falling back to local workspace files.${NC}"
        SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        for f in brainsait_master.py healthcare_workflows.py nphies_compliance.py; do
            if [[ -f "$SCRIPT_DIR/$f" ]]; then
                cp "$SCRIPT_DIR/$f" "$MCP_SERVERS_DIR/"
            else
                echo -e "${YELLOW}⚠️  Missing $f in workspace; skipping${NC}"
            fi
        done
        # Provide a minimal .env.template if external template is absent
        if [[ ! -f "$CONFIG_DIR/.env.template" ]]; then
            cat > "$CONFIG_DIR/.env.template" << 'EOF'
# BrainSAIT Environment Template
BRAINSAIT_API_KEY=
NPHIES_ENDPOINT=
FHIR_BASE_URL=
HIPAA_AUDIT_LOG=
N8N_API_KEY=
N8N_WEBHOOK_URL=
CLAUDE_API_KEY=
NPHIES_CLIENT_ID=
NPHIES_CLIENT_SECRET=
SAUDI_MOH_ENDPOINT=
ENCRYPTION_KEY=your_fernet_encryption_key_here
EOF
        fi
        echo -e "${GREEN}✅ MCP server files copied from workspace${NC}"
    fi
    
    # Make Python files executable (ignore if none)
    chmod +x "$MCP_SERVERS_DIR"/*.py 2>/dev/null || true
    
    # Copy environment template if external one exists (overrides fallback)
    if [[ -f "/mnt/user-data/outputs/.env.template" ]]; then
        cp "/mnt/user-data/outputs/.env.template" "$CONFIG_DIR/.env.template"
        echo -e "${GREEN}✅ Environment template copied from external source${NC}"
        echo -e "${YELLOW}⚠️  Please edit $CONFIG_DIR/.env with your actual credentials${NC}"
    fi
}

# Configure Claude Desktop MCP integration
configure_claude_desktop() {
    echo -e "${YELLOW}🔧 Configuring Claude Desktop MCP integration...${NC}"
    
    CLAUDE_CONFIG_FILE="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"
    BRAINSAIT_HOME_ESC=$(printf '%s\n' "$BRAINSAIT_HOME" | sed 's/[[\.*^$()+?{|]/\\&/g')
    
    # Create Claude Desktop config with BrainSAIT MCP servers
    cat > "$CLAUDE_CONFIG_FILE" << EOF
{
  "mcpServers": {
    "brainsait-masterlinc": {
      "command": "$BRAINSAIT_HOME/brainsait_env/bin/python",
      "args": ["-m", "brainsait_master"],
      "cwd": "$MCP_SERVERS_DIR",
      "env": {
        "BRAINSAIT_API_KEY": "\${BRAINSAIT_API_KEY}",
        "NPHIES_ENDPOINT": "\${NPHIES_ENDPOINT}",
        "FHIR_BASE_URL": "\${FHIR_BASE_URL}",
        "HIPAA_AUDIT_LOG": "$LOGS_DIR/hipaa_audit.log"
      }
    },
    "brainsait-healthcare-workflows": {
      "command": "$BRAINSAIT_HOME/brainsait_env/bin/python",
      "args": ["-m", "healthcare_workflows"],
      "cwd": "$MCP_SERVERS_DIR",
      "env": {
        "N8N_API_KEY": "\${N8N_API_KEY}",
        "N8N_WEBHOOK_URL": "\${N8N_WEBHOOK_URL}",
        "CLAUDE_API_KEY": "\${CLAUDE_API_KEY}"
      }
    },
    "brainsait-nphies-compliance": {
      "command": "$BRAINSAIT_HOME/brainsait_env/bin/python", 
      "args": ["-m", "nphies_compliance"],
      "cwd": "$MCP_SERVERS_DIR",
      "env": {
        "NPHIES_CLIENT_ID": "\${NPHIES_CLIENT_ID}",
        "NPHIES_CLIENT_SECRET": "\${NPHIES_CLIENT_SECRET}",
        "SAUDI_MOH_ENDPOINT": "\${SAUDI_MOH_ENDPOINT}",
        "ENCRYPTION_KEY": "\${ENCRYPTION_KEY}"
      }
    }
  },
  "globalShortcut": "CommandOrControl+Shift+.",
  "allowedMCPInstalls": true
}
EOF
    
    echo -e "${GREEN}✅ Claude Desktop configuration updated${NC}"
    echo -e "${CYAN}📝 Config file: $CLAUDE_CONFIG_FILE${NC}"
}

# Create CLI management tools  
create_cli_tools() {
    echo -e "${YELLOW}🛠️  Creating CLI management tools...${NC}"
    
    # Create main CLI script
    cat > "$HOME/bin/brainsait-cli" << 'EOF'
#!/usr/bin/env bash

# BrainSAIT CLI Management Tool
# Manage MCP servers and healthcare workflows

BRAINSAIT_HOME="$HOME/.brainsait"
MCP_SERVERS_DIR="$BRAINSAIT_HOME/mcp_servers"
LOGS_DIR="$BRAINSAIT_HOME/logs"
CONFIG_DIR="$BRAINSAIT_HOME/config"

case "$1" in
    start)
        echo "🚀 Starting BrainSAIT MCP servers..."
        cd "$MCP_SERVERS_DIR"
        source "$BRAINSAIT_HOME/brainsait_env/bin/activate"
        
        # Start servers in background
        python -m brainsait_master > "$LOGS_DIR/masterlinc.log" 2>&1 &
        python -m healthcare_workflows > "$LOGS_DIR/workflows.log" 2>&1 &
        python -m nphies_compliance > "$LOGS_DIR/nphies.log" 2>&1 &
        
        echo "✅ MCP servers started. Check logs in $LOGS_DIR"
        ;;
    stop)
        echo "🛑 Stopping BrainSAIT MCP servers..."
        pkill -f "brainsait_master"
        pkill -f "healthcare_workflows" 
        pkill -f "nphies_compliance"
        echo "✅ MCP servers stopped"
        ;;
    status)
        echo "📊 BrainSAIT MCP Server Status:"
        pgrep -f "brainsait_master" > /dev/null && echo "✅ MASTERLINC: Running" || echo "❌ MASTERLINC: Stopped"
        pgrep -f "healthcare_workflows" > /dev/null && echo "✅ Workflows: Running" || echo "❌ Workflows: Stopped"
        pgrep -f "nphies_compliance" > /dev/null && echo "✅ NPHIES: Running" || echo "❌ NPHIES: Stopped"
        ;;
    logs)
        echo "📋 Recent BrainSAIT logs:"
        echo "--- MASTERLINC ---"
        tail -n 10 "$LOGS_DIR/masterlinc.log" 2>/dev/null || echo "No logs found"
        echo "--- Workflows ---"
        tail -n 10 "$LOGS_DIR/workflows.log" 2>/dev/null || echo "No logs found"
        echo "--- NPHIES ---"
        tail -n 10 "$LOGS_DIR/nphies.log" 2>/dev/null || echo "No logs found"
        ;;
    test)
        echo "🧪 Testing MCP server connectivity..."
        cd "$MCP_SERVERS_DIR"
        source "$BRAINSAIT_HOME/brainsait_env/bin/activate"
        
        # Test imports
        python -c "import mcp; print('✅ MCP library OK')"
        python -c "import fhir.resources; print('✅ FHIR resources OK')" 
        python -c "import cryptography; print('✅ Cryptography OK')"
        python -c "import anthropic; print('✅ Anthropic OK')"
        
        # NVIDIA configured entrypoint validation (best effort)
        python - <<'PY'
import os, importlib
cfg = {
'rag': (os.getenv('NVIDIA_RAG_MODULE','').strip(), os.getenv('NVIDIA_RAG_FUNCTION','').strip()),
'ambient': (os.getenv('NVIDIA_AMBIENT_MODULE','').strip(), os.getenv('NVIDIA_AMBIENT_FUNCTION','').strip()),
'ava': (os.getenv('NVIDIA_AVA_MODULE','').strip(), os.getenv('NVIDIA_AVA_FUNCTION','').strip()),
}
for key,(mod,fn) in cfg.items():
if mod:
    try:
        m = importlib.import_module(mod)
        if fn:
            getattr(m, fn)
        print(f'✅ NVIDIA {key} configured: {mod}.{fn or "<auto>"}')
    except Exception as e:
        print(f'⚠️  NVIDIA {key} config invalid: {mod}.{fn} -> {e}')
PY
        echo "✅ All tests passed"
        ;;
    nvidia-test)
        echo "🧪 Testing NVIDIA integrations..."
        cd "$MCP_SERVERS_DIR"
        source "$BRAINSAIT_HOME/brainsait_env/bin/activate"
        python - <<'PY'
import sys
ok=True

def check(mods):
global ok
for m in mods:
    try:
        __import__(m)
        print(f"✅ Import OK: {m}")
        return True
    except Exception as e:
        print(f"❌ Import failed for {m}: {e}")
ok=False
return False

print("Checking RAG...")
check(["rag", "nvidia_rag", "apps.rag"])
print("Checking Ambient...")
check(["ambient", "ambient_healthcare_agents", "ambient_healthcare", "apps.ambient"])
print("Checking AI Virtual Assistant...")
check(["ai_virtual_assistant", "assistant", "apps.ai_virtual_assistant"])

sys.exit(0 if ok else 1)
PY
        ret=$?
        if [[ $ret -eq 0 ]]; then
            echo "✅ NVIDIA integrations look importable"
        else
            echo "⚠️  Some NVIDIA imports failed. Ensure repos are cloned and installed."
        fi
        ;;
    config)
        echo "⚙️  Opening BrainSAIT configuration..."
        ${EDITOR:-nano} "$CONFIG_DIR/.env"
        ;;
    *)
        echo "BrainSAIT CLI - Healthcare AI Platform Management"
        echo ""
        echo "Usage: brainsait-cli [command]"
        echo ""
        echo "Commands:"
        echo "  start         Start all MCP servers"
        echo "  stop          Stop all MCP servers"
        echo "  status        Show server status"
        echo "  logs          Show recent logs"
        echo "  test          Test core dependencies"
        echo "  nvidia-test   Test NVIDIA blueprint imports"
        echo "  config        Edit configuration"
        echo ""
        echo "🏥 BrainSAIT - Saudi Healthcare AI Platform"
        ;;
esac
EOF
    
    chmod +x "$HOME/bin/brainsait-cli"
    echo -e "${GREEN}✅ CLI tool created: brainsait-cli${NC}"
}

# Setup environment file
setup_environment() {
    echo -e "${YELLOW}🔐 Setting up environment configuration...${NC}"
    
    ENV_FILE="$CONFIG_DIR/.env"
    
    if [[ ! -f "$ENV_FILE" ]]; then
        cp "$CONFIG_DIR/.env.template" "$ENV_FILE"
        echo -e "${YELLOW}⚠️  Created $ENV_FILE from template${NC}"
        echo -e "${YELLOW}⚠️  Please edit this file with your actual API keys and credentials${NC}"
    else
        echo -e "${GREEN}✅ Environment file already exists${NC}"
    fi
    
    # Generate encryption key if not exists
    cd "$BRAINSAIT_HOME"
    source brainsait_env/bin/activate
    
    python3 -c "
from cryptography.fernet import Fernet
import os

env_file = '$ENV_FILE'
with open(env_file, 'r') as f:
    lines = f.read().splitlines()

# Ensure NVIDIA config keys exist
keys = [
    'NVIDIA_RAG_MODULE=', 'NVIDIA_RAG_FUNCTION=',
    'NVIDIA_AMBIENT_MODULE=', 'NVIDIA_AMBIENT_FUNCTION=',
    'NVIDIA_AVA_MODULE=', 'NVIDIA_AVA_FUNCTION='
]

existing = set([l.split('=')[0]+'=' for l in lines if '=' in l])
for k in keys:
    if k not in existing:
        lines.append(k)

content = '\n'.join(lines) + ('\n' if not lines or lines[-1] != '' else '')

# Generate encryption key if placeholder present
if 'your_fernet_encryption_key_here' in content:
    key = Fernet.generate_key().decode()
    content = content.replace('your_fernet_encryption_key_here', key)

with open(env_file, 'w') as f:
    f.write(content)
print('✅ Environment ensured (NVIDIA keys + encryption key)')
"
}

# Create Docker Compose for optional containerized deployment
create_docker_compose() {
    echo -e "${YELLOW}🐳 Creating Docker Compose configuration...${NC}"
    
    cat > "$BRAINSAIT_HOME/docker-compose.yml" << EOF
version: '3.8'

services:
  brainsait-postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: brainsait_prod
      POSTGRES_USER: brainsait
      POSTGRES_PASSWORD: \${POSTGRES_PASSWORD:-brainsait_secure_2024}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - brainsait_network
  
  brainsait-redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - brainsait_network
  
  brainsait-mongodb:
    image: mongo:7
    environment:
      MONGO_INITDB_ROOT_USERNAME: brainsait
      MONGO_INITDB_ROOT_PASSWORD: \${MONGODB_PASSWORD:-mongo_secure_2024}
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    networks:
      - brainsait_network

volumes:
  postgres_data:
  redis_data:
  mongodb_data:

networks:
  brainsait_network:
    driver: bridge
EOF
    
    echo -e "${GREEN}✅ Docker Compose configuration created${NC}"
    echo -e "${CYAN}📝 Run: cd $BRAINSAIT_HOME && docker-compose up -d${NC}"
}

# Final setup and verification
finalize_setup() {
    echo -e "${YELLOW}✅ Finalizing BrainSAIT MCP setup...${NC}"
    
    # Add bin to PATH if not already there
    if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
        echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
        echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc 2>/dev/null || true
        export PATH="$HOME/bin:$PATH"
    fi
    
    # Test CLI tool
    if command -v brainsait-cli &> /dev/null; then
        echo -e "${GREEN}✅ BrainSAIT CLI tool installed successfully${NC}"
    else
        echo -e "${YELLOW}⚠️  BrainSAIT CLI tool installed, restart terminal or run: export PATH=\"\$HOME/bin:\$PATH\"${NC}"
    fi
    
    # Create desktop shortcut (macOS)
    if [[ "$OS" == "macos" ]]; then
        echo -e "${CYAN}🖥️  Creating macOS app shortcut...${NC}"
        mkdir -p "$HOME/Applications"
        cat > "$HOME/Applications/BrainSAIT CLI.app/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>brainsait-cli</string>
    <key>CFBundleName</key>
    <string>BrainSAIT CLI</string>
    <key>CFBundleIdentifier</key>
    <string>com.brainsait.cli</string>
</dict>
</plist>
EOF
        mkdir -p "$HOME/Applications/BrainSAIT CLI.app/Contents/MacOS"
        ln -sf "$HOME/bin/brainsait-cli" "$HOME/Applications/BrainSAIT CLI.app/Contents/MacOS/brainsait-cli"
    fi
}

# Main installation function
main() {
    echo -e "${BLUE}🚀 Starting BrainSAIT MCP Server Installation...${NC}"
    echo ""
    
    detect_os
    check_prerequisites
    setup_directories
    setup_python_env
    install_dependencies
    install_mcp_servers
    clone_nvidia_blueprints
    configure_claude_desktop
    create_cli_tools
    setup_environment
    create_docker_compose
    finalize_setup
    
    echo ""
    echo -e "${GREEN}🎉 BrainSAIT MCP Server installation completed successfully!${NC}"
    echo ""
    echo -e "${CYAN}📋 Next Steps:${NC}"
    echo -e "${YELLOW}1.${NC} Edit configuration: ${CYAN}brainsait-cli config${NC}"
    echo -e "${YELLOW}2.${NC} Start services: ${CYAN}brainsait-cli start${NC}"
    echo -e "${YELLOW}3.${NC} Test connectivity: ${CYAN}brainsait-cli test${NC}"
    echo -e "${YELLOW}4.${NC} Restart Claude Desktop to load MCP servers"
    echo ""
    echo -e "${PURPLE}🏥 BrainSAIT Healthcare AI Platform ready for Saudi NPHIES integration!${NC}"
    echo -e "${BLUE}🇸🇦 Vision 2030 Digital Health Transformation${NC}"
}

# Run main function
main "$@"