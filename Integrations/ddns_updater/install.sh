#!/bin/sh
cd /tmp/userdata
rm -rf ddns_updater
mkdir ddns_updater
/userfs/bin/curl -Lk -o ddns_updater/updater_v5 https://github.com/qdm12/ddns-updater/releases/download/v2.9.0/ddns-updater_2.9.0_linux_armv5
cd ddns_updater
chmod 777 updater_v5
./updater_v5
