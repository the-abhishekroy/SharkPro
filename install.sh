#!/bin/bash

# SharkPro v2.6 Installer
# For Termux & Linux

RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║              🦈 SharkPro v2.6 Installer                   ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Detect environment
if [ -d "/data/data/com.termux/files/usr" ]; then
    TERMUX=true
    PREFIX="/data/data/com.termux/files/usr"
else
    TERMUX=false
    PREFIX="/usr"
fi

echo -e "${YELLOW}[*] Updating packages...${NC}"
if $TERMUX; then
    pkg update -y && pkg upgrade -y
else
    sudo apt update -y && sudo apt upgrade -y
fi

echo -e "${YELLOW}[*] Installing dependencies...${NC}"
if $TERMUX; then
    pkg install -y python python-pip php git curl wget unzip termux-api
else
    sudo apt install -y python3 python3-pip php git curl wget unzip
fi

echo -e "${YELLOW}[*] Installing Python modules...${NC}"
pip3 install requests qrcode[pil] pyngrok --user

# Install ngrok
echo -e "${YELLOW}[*] Setting up ngrok...${NC}"
if $TERMUX; then
    if ! command -v ngrok &> /dev/null; then
        curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee $PREFIX/etc/apt/trusted.gpg.d/ngrok.asc
        echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | tee $PREFIX/etc/apt/sources.list.d/ngrok.list
        pkg update && pkg install -y ngrok
    fi
else
    if ! command -v ngrok &> /dev/null; then
        curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc
        echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
        sudo apt update && sudo apt install -y ngrok
    fi
fi

# Install cloudflared
echo -e "${YELLOW}[*] Setting up cloudflared...${NC}"
if ! command -v cloudflared &> /dev/null; then
    if $TERMUX; then
        wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64 -O $PREFIX/bin/cloudflared
        chmod +x $PREFIX/bin/cloudflared
    else
        wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O /tmp/cloudflared
        sudo mv /tmp/cloudflared /usr/local/bin/cloudflared
        sudo chmod +x /usr/local/bin/cloudflared
    fi
fi

# Create launcher
echo -e "${YELLOW}[*] Creating launcher...${NC}"
mkdir -p $PREFIX/share/sharkpro
cp sharkpro.py $PREFIX/share/sharkpro/

cat > $PREFIX/bin/sharkpro << 'EOF'
#!/bin/bash
cd $PREFIX/share/sharkpro
python3 sharkpro.py
EOF
chmod +x $PREFIX/bin/sharkpro

echo -e "${GREEN}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                 Installation Complete!                    ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${GREEN}[✓] SharkPro v2.6 installed${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Get ngrok authtoken from ${BLUE}https://dashboard.ngrok.com${NC}"
echo "  2. Run: ${GREEN}ngrok config add-authtoken YOUR_TOKEN${NC}"
echo "  3. Run tool: ${GREEN}sharkpro${NC}"
echo ""
echo -e "${RED}⚠️  EDUCATIONAL USE ONLY ⚠️${NC}"