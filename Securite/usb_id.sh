#!bin/bash 

# #Recupere l'identifiant de la cle USB
#usb_id="${ID_SERIAL_SHORT}"
#usb_id=$(grep -m 1 -v "^$" /var/GateKeepr/Securite/usb_id.txt)
#echo $usb_id >> /var/GateKeepr/text.txt

# #Monte la cle dans un repertoire cree avec comme nom l'id
#sudo mkdir /media/user/$usb_id
#sudo mount /dev/sdb /media/user/$usb_id

#Attend que la cle soit montee
while true; do 
	directory=$(inotifywait -e create --format '%w' /media/user)
	if [ -n "$directory" ]; then
		echo "Cle bien montee dans /media/user : $directory"
		break
	fi 
	sleep 1 
done  



#Scan le repertoire de la cle
sudo find /media/user -type f -not -name ".CHK" -print0 | xargs -0 -P $(nproc) clamscan --infected > /var/log/temp_log.txt

#Fonctionne pas et appelle pas le python
#file="/var/log/temp_log.txt"
#Regarde si le fichier est non vide
#if [ -s "$file" ]; then
PYTHONPATH="/var/GateKeepr/Interface"	
python -c 'exec(open("/var/GateKeepr/Interface/affichage.py").read());
copy_file_content("/var/log/temp_log.txt","/var/log/GateKeepr.log")'
#fi


#echo "$usb_id" >> /home/user/Documents/usbtest.log

# #Demonte et supprime le repertoire de la cle 
#sudo umount /media/user/$usb_id
#sudo rmdir /media/user/$usb_id


# #Affichage sur l'ecran 
# python_file="/home/user/Documents/affichage.py"
# echo "Execution du programme python" >> /home/user/Documents/usbtest.log
# python3 "$python_file" >> /home/user/Documents/usbtest.log
# echo "Done" >> /home/user/Documents/usbtest.log

