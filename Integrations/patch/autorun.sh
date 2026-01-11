#!/bin/sh

# ===== COLORS =====
GREEN='\033[32m'
B_MAGENTA='\033[95m'
RED='\033[31m'
RESET='\033[0m'
YELLOW='\033[33m'
CYAN='\033[36m'

# ===== CLEAR SPACE =====
echo -e "\n\n\n\n\n\n\n\n\n\n"

# ===== BANNER =====
echo -e "\033[31;43mScript Make By AppleSang With <3\033[0m\n"

echo -e "${RED}############################################################"
echo ""
echo -e "${GREEN} https://github.com/Expl01tHunt3r/vnptmodemresearch"
echo ""
echo -e "${RED}############################################################\n"
echo ""
echo -e "        ${YELLOW}Press enter to confirm for patch ${CYAN}Auto Startup ${RESET}"
read _

# ===== PATCH CONTENT =====
STC='#!/bin/sh
/tmp/userdata/startup.sh >/dev/null 2>&1
'

cd /etc/safegate || exit 1

echo "$STC" > init.sh
echo "$STC" > md5.sh
echo "$STC" > safegate.sh
chmod +x init.sh md5.sh safegate.sh

# ===== USER STARTUP =====
cd /tmp/userdata || exit 1

echo 'echo "Hello World! From https://github.com/Expl01tHunt3r/vnptmodemresearch"' > startup.sh
chmod +x startup.sh

# ===== DONE =====
echo -e "${GREEN}Patch Done!${RESET}"
echo -e "${B_MAGENTA}To run commands after the router connects to the internet,
use ${RED}echo${B_MAGENTA} or ${RED}sed${B_MAGENTA} to edit:${RESET} /tmp/userdata/startup.sh
${CYAN}Example: ${RED}echo 'echo "Hello World! From https://github.com/Expl01tHunt3r/vnptmodemresearch"' > startup.sh ${RESET}"
