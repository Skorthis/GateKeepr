#!/bin/bash

### BEGIN INIT INFO
# Provides:          display
# Required-Start:    $local_fs $network
# Required-Stop:     $local_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: affichage des logs générés par USBGuard
### END INIT INFO

#essai avec une autre commande parce que le démon et le processus watch entrent en conflit
#usb_id=${ID_SERIAL_SHORT}
#dev_name=${ID_FS_MOUNTPOINT}
#usb_id=$(udevadm info --query=property --name=/dev/sda | grep "ID_SERIAL_SHORT=" | cut -d "=" -f 2)
#echo "$usb_id" >> /var/GateKeepr/Securite/usb_id.txt
#echo "$dev_name" >> /var/GateKeepr/Securite/usb_id.txt

rm /var/log/USBGuard_logs.txt
touch /var/log/USBGuard_logs.txt
usbguard list-devices >> /var/log/USBGuard_logs.txt
python3 /var/GateKeepr/Securite/display.py


