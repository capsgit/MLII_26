#!/bin/bash

# ============================================================
#   Ubuntu 24.04 — Streamlit Auto Setup Script
#   Usage: bash streamlit_setup.sh
# ============================================================

set -e  # Exit immediately on any error

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

step() {
  echo ""
  echo -e "${BLUE}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${CYAN}${BOLD}  STEP $1: $2${NC}"
  echo -e "${BLUE}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

done_msg() {
  echo -e "${GREEN}  ✔ Done: $1${NC}"
}

# ─────────────────────────────────────────
# STEP 1 — Update & Upgrade
# ─────────────────────────────────────────
step 1 "Update & Upgrade System"
sudo apt update -y && sudo apt upgrade -y
done_msg "System updated and upgraded"

# ─────────────────────────────────────────
# STEP 2 — Create App Folder on Desktop
# ─────────────────────────────────────────
step 2 "Create App Folder on Desktop"
mkdir -p ~/Desktop/app
cd ~/Desktop/app
done_msg "Created ~/Desktop/app and navigated into it"

# ─────────────────────────────────────────
# STEP 3 — Install pip3
# ─────────────────────────────────────────
step 3 "Install pip3"
sudo apt install python3-pip -y
done_msg "pip3 installed: $(pip3 --version)"

# ─────────────────────────────────────────
# STEP 4 — Install python3-venv
# ─────────────────────────────────────────
step 4 "Install Virtual Environment Package"
sudo apt install python3-venv -y
done_msg "python3-venv installed"

# ─────────────────────────────────────────
# STEP 5 — Create Virtual Environment
# ─────────────────────────────────────────
step 5 "Create Virtual Environment"
cd ~/Desktop/app
python3 -m venv venv
done_msg "Virtual environment created at ~/Desktop/app/venv"

# ─────────────────────────────────────────
# STEP 6 — Activate Virtual Environment
# ─────────────────────────────────────────
step 6 "Activate Virtual Environment"
source ~/Desktop/app/venv/bin/activate
done_msg "Virtual environment activated"

# ─────────────────────────────────────────
# STEP 7 — Install Streamlit
# ─────────────────────────────────────────
step 7 "Install Streamlit"
pip install streamlit
done_msg "Streamlit installed: $(streamlit --version)"

# ─────────────────────────────────────────
# STEP 8 — Create Demo app.py
# ─────────────────────────────────────────
step 8 "Create Demo app.py"
cat > ~/Desktop/app/app.py << 'EOF'
import streamlit as st

st.set_page_config(page_title="My App", page_icon="🚀")
st.title("Hello, Streamlit! 🎉")
st.write("Welcome to your first Streamlit app.")

name = st.text_input("Enter your name:")
if name:
    st.success(f"Hello, {name}! 👋")

if st.button("Click Me"):
    st.balloons()
EOF
done_msg "app.py created at ~/Desktop/app/app.py"

# ─────────────────────────────────────────
# STEP 9 — Run the Streamlit App
# ─────────────────────────────────────────
step 9 "Launching Streamlit App"
echo ""
echo -e "${YELLOW}${BOLD}  ✅ Setup complete! Starting Streamlit...${NC}"
echo -e "${YELLOW}     Local URL:  http://localhost:8501${NC}"
echo -e "${YELLOW}     Press Ctrl+C to stop the server${NC}"
echo ""

cd ~/Desktop/app
source venv/bin/activate
streamlit run app.py