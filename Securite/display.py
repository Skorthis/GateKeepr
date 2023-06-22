#!bin/python3
# Script python qui permet d'afficher les informations concernant les périphériques dans le terminal
#import subprocess
import os

file_path = "/var/log/USBGuard_logs.txt"
i = 0
blocked = 0
multiple_interface = 0

def write_file(file_path,text):
	with open(file_path,'w') as file:
		file.write(text)
	return 
	
def read_file(file_path):
	with open(file_path,'r') as file:
		contenu=file.read()
	return contenu

try:
	file = open(file_path, 'r', encoding="utf-8")
except:
	print("Le fichier contenant les logs n'a pas pu être trouvé !!! \n")
else:
	logs = file.readlines()
	for i in range (len(logs)):
		if i == len(logs)-1:
			#print(logs[i])
			USB_device = logs[i].split(" ")
			if "block" in USB_device:
				blocked = 1
			if USB_device[USB_device.index("with-interface") + 1] == '{':
				if (USB_device.index("}") - USB_device.index("{")) > 2:
					USB_code = USB_device[USB_device.index("with-interface") + 2].split(":")
					multiple_interface = 1
				else:
					USB_code = USB_device[USB_device.index("with-interface") + 2].split(":")
			else:
				USB_code = USB_device[USB_device.index("with-interface") + 1].split(":")
			USB_class = USB_code[0]
			USB_subclass = USB_code[1]
			USB_protocol = USB_code[2]
			
			#USB_class = "03"
			#USB_subclass = "01"
			#USB_protocol = "01"
			
			USB_classification = {"00":"un dispositif ayant une classification USB non connue", 
				"01":"un périphérique audio", 
				"02":"un périphérique de communication (téléphone, modem, contrôleur ATM, contrôleur ethernet,...)", 
				"03":"un périphérique d'interface utilisateur", 
				"05":"un périphérique physique", 
				"06":"un périphérique de capture d'images", 
				"07":"un périphérique d'impression", 
				"08":"un périphérique de stockage de masse", 
				"09":"un hub USB", 
				"0a":"un périphérique de données CDC (modem USB ou communication série)", 
				"0b":"une carte à puce", 
				"0d":"un périphérique de sécurité du contenu", 
				"0e":"un périphérique vidéo", 
				"ef":"un périphérique multiple", 
				"fe":"un périphérique à application spécifique", 
				"ff":"un périphérique d'un vendeur spécifique"}
			
			#print(USB_device)
			#print(USB_code)
			#print(USB_class, USB_subclass, USB_protocol)
			if blocked == 1 and multiple_interface == 1 and (USB_class!="03" and USB_protocol != "02"):
				write_file("/var/log/GateKeepr.log","Le périphérique que vous venez d'insérer est reconnu comme une combinaison de périphériques. Nous vous conseillons de ne pas l'utiliser car il est potentiellement dangereux.")
			elif USB_class == "03" and (USB_subclass == "01" or USB_subclass=="00") and USB_protocol == "01":
				write_file("/var/log/GateKeepr.log","Le système a détecté que vous avez branché un clavier. Une analyse des frappes de clavier va être lancée pour déterminer le niveau de menace de ce périphérique.\n3")
				terminal_command="lxterminal"
				path_file="/var/GateKeepr/Securite/keylogger.py"
				#os.system(f"{terminal_command} -e python3 {path_file}")
				os.putenv("DISPLAY",":0")
				#os.system("sudo lxterminal")
				os.system("sudo python3 "+str(path_file))
			elif USB_class == "03" and USB_subclass == "01" and USB_protocol == "02":
				write_file("/var/log/GateKeepr.log","Le système a détecté que vous avez branché une souris. Êtes-vous sûr qu'il s'agit du bon dispositif USB ?")
			elif USB_class == "08":
				write_file("/var/log/GateKeepr.log","Le système a détecté que vous avez branché " + USB_classification.get(USB_class) + ". Votre périphérique va être scanné à la recherche de virus.\n2")
				path_file="/var/GateKeepr/Securite/usb_id.sh"
				os.system(f"sudo bash {path_file}")
			else:
				write_file("/var/log/GateKeepr.log","Le système a détecté que vous avez branché " + USB_classification.get(USB_class) + ". Êtes-vous sûr qu'il s'agit du bon dispositif USB ?")
	#print(logs)
	
finally:
	file.close()
