#!/bin/sh

if [ ! -e /tmp/SafeGate/AdGuardHome ]; then
    export SSL_CERT_FILE=/tmp/userdata/AdGuard/accvraiz1.crt
    cd /tmp/SafeGate || exit 1
    /userfs/bin/curl -s -fSL -o AdGuardHome_linux_armv5.tar.gz \
        https://github.com/AdguardTeam/AdGuardHome/releases/latest/download/AdGuardHome_linux_armv5.tar.gz
    tar -xzf AdGuardHome_linux_armv5.tar.gz
    rm AdGuardHome_linux_armv5.tar.gz
    cd AdGuardHome || exit 1
    chmod +x AdGuardHome
    pidof dnsmasq >/dev/null && kill $(pidof dnsmasq)
    ./AdGuardHome -c /tmp/userdata/AdGuard/AdGuardHome.yaml -w /tmp/SafeGate
fi
