#/bin/bash

# PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games
PATH=/usr/bin

RED='\e[38;5;160m'
ORA='\e[38;5;208m'
WHI='\e[38;5;7m'
NC='\033[0m'
LOG_FILE="setup_$(date +"%Y-%m-%d_%H:%M:%S_%N").log"

echo -e  " ${WHI}                                       ${ORA}  ▄▄${RED} ▄▄▄▄     ${WHI}        ▄              ▀          "
echo -e  " ${WHI}    █▀▀▀▄  ▄▀▀▀▄  ▐█▀▀▀█▄ ▐█▄▀ ▄▄▀▀▄█  ${ORA} ██ ${RED}   ▀▀███  ${WHI} █▀▀▀▄ ▀█▀▀ ▄▀▀▀▄ ▐█▄▀ █  ▄▄▀▀▄█  "
echo -e  " ${WHI}    ▀▀▄▄▄ █     █ ▐█    █ ▐█   █    █  ${RED}         ${ORA} ▄   ${WHI} ▀▀▄▄▄  █  ██▀▀▀▀ ▐█   █  █    █  "
echo -e  " ${WHI}    ▀▄▄▄█  █▄▄▄█  ▐█▄▄▄█▀ ▐█   ▀▄▄▄▄█  ${RED} ███▄▄▄  ${ORA}▄██  ${WHI} ▀▄▄▄█  █▄▄ ▀▄▄▄  ▐█   █  ▀▄▄▄▄█  "
echo -e  " ${WHI}                  ▐█                   ${RED}  ▀▀▀                                           "
echo -e $NC

echo "Updating apt dependencies..."
sudo apt update >> $LOG_FILE 2>&1

echo "Upgrating apt dependencies..."
sudo apt -y upgrade >> $LOG_FILE 2>&1   

echo "Installing global dependencies..."
# sudo apt install >> $LOG_FILE 2>&1

echo "Installing python dependencies..."
# pip install 

echo "Dependencies installed"

echo "Setting up POE"
{
    sudo sh -c 'echo "dtoverlay=dwc2" >> /boot/config.txt'
    sudo sh -c 'echo "$(cat /boot/cmdline.txt) modules-load=dwc2,g_ether" > /boot/cmdline.txt'
    sudo touch /boot/ssh
} >> $LOG_FILE 2>&1

