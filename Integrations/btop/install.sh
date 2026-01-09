#!/bin/sh
cd /tmp/userdata
rm -rf btop
mkdir btop
/userfs/bin/curl -Lk -o btop/btop https://github.com/Expl01tHunt3r/vnptmodemresearch/raw/refs/heads/master/Integrations/btop/btop
cd btop
chmod 777 btop
echo "Btop have been installed at \"/tmp/userdata/btop/btop\"."
echo "You can start btop using \"/tmp/userdata/btop/btop --force-utf\""