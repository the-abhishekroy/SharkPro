#!/bin/bash
# SharkPro v3.0 - Installation Script
# ===================================

set -e

# Colors
R='\033[1;31m'
G='\033[1;32m'
Y='\033[1;33m'
C='\033[1;36m'
NC='\033[0m'

# Banner
echo -e "${C}"
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║   ███████╗██╗  ██╗ █████╗ ██████╗ ██╗  ██╗██████╗ ██████╗ ██████╗ ║"
echo "║   ██╔════╝██║  ██║██╔══██╗██╔══██╗██║ ██╔╝╚═══██╗╚═══██╗ ██╔══██╗║"
echo "║   ███████╗███████║███████║██████╔╝█████╔╝    ██╔╝   ██╔╝ ██████╔╝║"
echo "║   ╚════██║██╔══██║██╔══██║██╔══██╗██╔═██╗   ██╔╝   ██╔╝  ██╔═══╝ ║"
echo "║   ███████║██║  ██║██║  ██║██║  ██║██║  ██╗███████╗██║   ██║      ║"
echo "║   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝      ║"
echo "║                                                                  ║"
echo "║              ⚠️  EDUCATIONAL USE ONLY - v3.0  ⚠️               ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${Y}[*] Installing SharkPro v3.0...${NC}"
echo ""

# Detect OS
if [ -d "/data/data/com.termux/files/usr" ]; then
    OS="termux"
    INSTALL_DIR="/data/data/com.termux/files/usr/share/sharkpro"
    BIN_DIR="/data/data/com.termux/files/usr/bin"
elif [ -f "/etc/debian_version" ]; then
    OS="debian"
    INSTALL_DIR="/opt/sharkpro"
    BIN_DIR="/usr/local/bin"
elif [ -f "/etc/redhat-release" ]; then
    OS="redhat"
    INSTALL_DIR="/opt/sharkpro"
    BIN_DIR="/usr/local/bin"
else
    OS="linux"
    INSTALL_DIR="$HOME/.sharkpro"
    BIN_DIR="$HOME/.local/bin"
fi

echo -e "${C}[*] Detected OS: $OS${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${R}[!] Python3 not found. Installing...${NC}"
    if [ "$OS" = "termux" ]; then
        pkg update -y && pkg install python python-pip -y
    elif [ "$OS" = "debian" ]; then
        apt-get update && apt-get install python3 python3-pip -y
    elif [ "$OS" = "redhat" ]; then
        yum install python3 python3-pip -y
    fi
else
    echo -e "${G}[✓] Python3 found${NC}"
fi

# Install essential packages
echo -e "${Y}[*] Installing essential packages...${NC}"

if [ "$OS" = "termux" ]; then
    pkg install -y git curl wget python python-pip openssh nano
elif command -v apt-get &> /dev/null; then
    apt-get update
    apt-get install -y git curl wget python3 python3-pip openssh-client
elif command -v yum &> /dev/null; then
    yum install -y git curl wget openssh-clients
elif command -v pacman &> /dev/null; then
    pacman -S --needed git curl wget openssh
fi

# Create directories
echo -e "${Y}[*] Creating directories...${NC}"
mkdir -p "$INSTALL_DIR" "$BIN_DIR"
mkdir -p "$INSTALL_DIR/templates" "$INSTALL_DIR/modules" "$INSTALL_DIR/core"
mkdir -p "$INSTALL_DIR/static/css" "$INSTALL_DIR/static/js" "$INSTALL_DIR/static/img"

# Install Python modules
echo -e "${Y}[*] Installing Python modules...${NC}"
pip3 install --user requests colorama beautifulsoup4 qrcode pillow flask psutil 2>/dev/null || \
pip install requests colorama beautifulsoup4 qrcode pillow flask psutil

echo -e "${G}[✓] Python modules installed${NC}"

# Create launcher script
echo -e "${Y}[*] Creating launcher...${NC}"
cat > "$BIN_DIR/sharkpro" << 'EOF'
#!/bin/bash
INSTALL_DIR="${SHARKPRO_DIR:-$HOME/.sharkpro}"
if [ -d "/opt/sharkpro" ]; then
    INSTALL_DIR="/opt/sharkpro"
elif [ -d "/data/data/com.termux/files/usr/share/sharkpro" ]; then
    INSTALL_DIR="/data/data/com.termux/files/usr/share/sharkpro"
fi

cd "$INSTALL_DIR"
python3 main.py "$@"
EOF

chmod +x "$BIN_DIR/sharkpro"

# Check if directories are writable
if [ ! -w "$INSTALL_DIR" ] && [ "$OS" != "termux" ]; then
    echo -e "${Y}[*] Need sudo to install to $INSTALL_DIR${NC}"
    INSTALL_DIR="$HOME/.sharkpro"
    mkdir -p "$INSTALL_DIR" "$HOME/.local/bin"
    BIN_DIR="$HOME/.local/bin"
    
    # Update launcher
    cat > "$BIN_DIR/sharkpro" << EOF
#!/bin/bash
cd "$INSTALL_DIR"
python3 main.py "\$@"
EOF
    chmod +x "$BIN_DIR/sharkpro"
    
    # Add to PATH if needed
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
        echo -e "${Y}[*] Added ~/.local/bin to PATH${NC}"
    fi
fi

echo -e "${C}"
echo "╔════════════════════════════════════════════════════════╗"
echo "║  ✅ INSTALLATION COMPLETE                             ║"
echo "╠════════════════════════════════════════════════════════╣"
echo "║                                                        ║"
echo "║  Installation Directory: $INSTALL_DIR         ║"
echo "║  Binary: $BIN_DIR/sharkpro                      ║"
echo "║                                                        ║"
echo "╠════════════════════════════════════════════════════════╣"
echo "║  USAGE:                                                ║"
echo "║                                                        ║"
echo "║    sharkpro                                            ║"
echo "║    OR                                                  ║"
echo "║    cd $INSTALL_DIR && python3 main.py        ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${G}[✓] Installation complete!${NC}"
echo -e "${Y}[*] Run 'sharkpro' to start${NC}"

# Optional tunnel tools
echo ""
echo -e "${C}[?] Install tunnel tools? (highly recommended)${NC}"
echo -e "    This will install:"
echo -e "    • ${G}ngrok${NC} - global tunnel service"
echo -e "    • ${G}cloudflared${NC} - fast reliable tunnels"
echo -e ""

read -p "Install tunnel tools? [Y/n]: " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]?$ ]]; then
    echo -e "${Y}[*] Installing tunnel tools...${NC}"
    
    # Install ngrok
    if ! command -v ngrok &> /dev/null; then
        echo -e "${Y}[*] Installing ngrok...${NC}"
        if [ "$OS" = "termux" ]; then
            pkg install ngrok -y 2>/dev/null || echo -e "${Y}[!] Please install ngrok manually${NC}"
        else
            curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
                | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null 2>/dev/null
            echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
                | sudo tee /etc/apt/sources.list.d/ngrok.list >/dev/null 2>/dev/null
            sudo apt-get update && sudo apt-get install -y ngrok 2>/dev/null || \
            echo -e "${Y}[!] Please install ngrok from https://ngrok.com/download${NC}"
        fi
    fi
    
    # Install cloudflared
    if ! command -v cloudflared &> /dev/null; then
        echo -e "${Y}[*] Installing cloudflared...${NC}"
        if [ "$OS" = "termux" ]; then
            pkg install cloudflared -y 2>/dev/null || echo -e "${Y}[!] Please install cloudflared manually${NC}"
        else
            # Get latest release URL
            ARCH=$(uname -m)
            if [ "$ARCH" = "x86_64" ]; then
                URL="https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
            elif [ "$ARCH" = "aarch64" ]; then
                URL="https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64"
            else
                URL="https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-386"
            fi
            
            curl -Lo /tmp/cloudflared "$URL" 2>/dev/null
            sudo install -m 755 /tmp/cloudflared /usr/local/bin/cloudflared 2>/dev/null || \
            mv /tmp/cloudflared "$HOME/.local/bin/cloudflared" 2>/dev/null && chmod +x "$HOME/.local/bin/cloudflared"
            rm -f /tmp/cloudflared
        fi
    fi
    
    echo -e "${G}[✓] Tunnel tools installation attempted${NC}"
fi

# SSH setup for localhost.run
if [ ! -f "$HOME/.ssh/id_rsa" ]; then
    echo ""
    echo -e "${Y}[*] SSH key not found. Setting up for localhost.run...${NC}"
    mkdir -p "$HOME/.ssh"
    ssh-keygen -t rsa -N "" -f "$HOME/.ssh/id_rsa" -C "sharkpro@localhost"
    echo -e "${G}[✓] SSH key generated${NC}"
    echo -e "${Y}[!] Add this key to https://localhost.run/keys.html${NC}"
    cat "$HOME/.ssh/id_rsa.pub"
    echo ""
fi

echo -e "\n${G}🦈 SharkPro is ready to use!${NC}\n"