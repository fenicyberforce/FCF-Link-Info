#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
echo "╔══════════════════════════════════════╗"
echo "║        FCF LINK INFO INSTALLER       ║"
echo "║      Feni Cyber Force - Official     ║"
echo "╚══════════════════════════════════════╝"
echo -e "${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR] Python3 is not installed!${NC}"
    echo "Install Python3 first:"
    echo "Termux: pkg install python"
    echo "Linux: sudo apt install python3"
    echo "Mac: brew install python3"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}[INFO] Installing pip3...${NC}"
    if [[ "$OSTYPE" == "linux-android"* ]]; then
        pkg install python -y
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt install python3-pip -y
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install python3
    fi
fi

# Create directory
mkdir -p ~/.fcftools
cd ~/.fcftools

# Download main script
echo -e "${YELLOW}[INFO] Downloading FCF LINK INFO...${NC}"
curl -s -o fcflinkinfo.py "https://raw.githubusercontent.com/feniccyberforce/fcflinkinfo/main/fcflinkinfo.py"

# Make executable
chmod +x fcflinkinfo.py

# Install dependencies
echo -e "${YELLOW}[INFO] Installing dependencies...${NC}"
pip3 install httpx requests colorama pyfiglet tqdm

# Create symlink
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    mkdir -p ~/.local/bin
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
fi

ln -sf ~/.fcftools/fcflinkinfo.py ~/.local/bin/fcflinkinfo

echo -e "${GREEN}"
echo "╔══════════════════════════════════════╗"
echo "║         INSTALLATION COMPLETE        ║"
echo "╚══════════════════════════════════════╝"
echo -e "${NC}"
echo -e "${GREEN}[SUCCESS] FCF LINK INFO installed successfully!${NC}"
echo -e "${CYAN}Run the tool with: fcflinkinfo${NC}"
echo -e "${YELLOW}Make sure to restart your terminal or run: source ~/.bashrc${NC}"

# Run the tool
echo -e "\n${YELLOW}[INFO] Starting FCF LINK INFO...${NC}"
sleep 2
python3 ~/.fcftools/fcflinkinfo.py