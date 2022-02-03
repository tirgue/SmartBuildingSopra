#/bin/bash
set -e

# PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games
PATH=/usr/bin

RED='\e[38;5;160m'
ORA='\e[38;5;208m'
WHI='\e[38;5;7m'
GRE='\e[38;5;46m'
NC='\033[0m'
LOG_FILE="setup_$(date +"%Y-%m-%d_%H:%M:%S_%N").log"
TICK="\r[${GRE}✓${NC}]"
CROSS="\r[${RED}✗${NC}]"

trap "echo An error has occured, check ${LOG_FILE} for more details" ERR

echo -e  " ${WHI}                                       ${ORA}  ▄▄${RED} ▄▄▄▄     ${WHI}        ▄              ▀          "
echo -e  " ${WHI}    █▀▀▀▄  ▄▀▀▀▄  ▐█▀▀▀█▄ ▐█▄▀ ▄▄▀▀▄█  ${ORA} ██ ${RED}   ▀▀███  ${WHI} █▀▀▀▄ ▀█▀▀ ▄▀▀▀▄ ▐█▄▀ █  ▄▄▀▀▄█  "
echo -e  " ${WHI}    ▀▀▄▄▄ █     █ ▐█    █ ▐█   █    █  ${RED}         ${ORA} ▄   ${WHI} ▀▀▄▄▄  █  ██▀▀▀▀ ▐█   █  █    █  "
echo -e  " ${WHI}    ▀▄▄▄█  █▄▄▄█  ▐█▄▄▄█▀ ▐█   ▀▄▄▄▄█  ${RED} ███▄▄▄  ${ORA}▄██  ${WHI} ▀▄▄▄█  █▄▄ ▀▄▄▄  ▐█   █  ▀▄▄▄▄█  "
echo -e  " ${WHI}                  ▐█                   ${RED}  ▀▀▀                                           "
echo -e $NC

echo -ne "${CROSS} Updating apt dependencies"
sudo apt update >> $LOG_FILE 2>&1
echo -e $TICK

echo -ne "${CROSS} Upgrating apt dependencies"
sudo apt -y upgrade >> $LOG_FILE 2>&1   
echo -e $TICK

echo -ne "${CROSS} Installing global dependencies"
sudo apt install -y python3-pip i2c-tools >> $LOG_FILE 2>&1
echo -e $TICK

echo -ne "${CROSS} Installing python dependencies"
pip3 install flask wrapt smbus2 Adafruit-BMP persistqueue azure.iot.device >> $LOG_FILE 2>&1
echo -e $TICK

if ! cat /boot/config.txt | grep -q "dtoverlay=dwc2"; then
    echo -ne "${CROSS} Setting up POE"
    {
        sudo sh -c 'echo "dtoverlay=dwc2" >> /boot/config.txt'
        sudo sh -c 'echo "$(cat /boot/cmdline.txt) modules-load=dwc2,g_ether" > /boot/cmdline.txt'
        sudo touch /boot/ssh
    } >> $LOG_FILE 2>&1
    echo -e $TICK
fi

echo -ne "${CROSS} Setting up API"
mkdir src/api/cert/keystore -p >> $LOG_FILE 2>&1
if test "$(ls src/api/cert | grep -E 'cert.pem|key.pem' | wc -l)" -lt 2; then
    openssl req -new -newkey rsa:4096 -days 3650 -nodes -x509 \
        -subj "/C=FR/ST=Herault/L=Montpellier/O=Sopra Steria/CN=raspberrypi" \
        -keyout src/api/cert/key.pem  -out src/api/cert/cert.pem >> $LOG_FILE 2>&1
fi
echo -e $TICK

echo -ne "${CROSS} Setting up sensors"
sudo raspi-config nonint do_i2c 0 >> $LOG_FILE 2>&1
echo -e $TICK

if ! crontab -l | grep '@reboot sh \$HOME/SmartBuildingSopra/run.sh' >> /dev/null; then
    echo -ne "${CROSS} Setting up run at startup"
    echo -e "$(crontab -l)\n@reboot sh \$HOME/SmartBuildingSopra/run.sh" | crontab >> $LOG_FILE 2>&1
    echo -e $TICK
fi
echo ""
echo "» Installation done, please reboot the Raspberry Pi after you've updated the config"
