#!bin/python3
from pynput import keyboard
from Xlib import X, display

import subprocess
import os 
import psutil
import signal
import subprocess

print("Dans keylogfile")

# Liste de commandes considérées comme néfastes
commandes_nefastes = ["rm -rf", "format C:", "shutdown", "ls"]

# Chaîne de caractères pour stocker la commande en cours de saisie
commande_en_cours = ""

#Fonction pour ecrire dans le fichier log 
def write_file(path_file,text):
	with open(path_file,'w') as file:
		#file.truncate(0)
		file.write(text)
	return

# Fonction pour bloquer les raccourcis clavier
def block_shortcuts():
    d = display.Display()
    root = d.screen().root
    root.grab_keyboard(True, X.GrabModeAsync, X.GrabModeAsync, X.CurrentTime)


# Fonction pour charger la blacklist depuis un fichier
def load_blacklist(file_path):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                command = line.strip()  # Supprimer les espaces et les sauts de ligne
                commandes_nefastes.append(command)

        print("Blacklist chargée avec succès.")
    except FileNotFoundError:
        print("Fichier introuvable :"+file_path)
    except Exception as e:
        print("Une erreur s'est produite lors du chargement de la blacklist :"+str(e))

#Permet d'arreter le programme a l'aide d'un signal
def simulate_end():
    # Obtenir l'identifiant de processus (PID) du programme en cours
    current_pid = os.getpid()

    # Envoyer un signal de terminaison au processus en cours
    os.kill(current_pid, signal.SIGINT)
   
def QuitMainProgram():
    with open("/var/GateKeepr/Securite/pid.txt",'r') as file:
    	pid=file.read()
    print(str(pid))
    os.kill(int(pid), signal.SIGINT)
    return 

#Permet de regarder si un element de la commande est nefaste 
def check_command(commande):
	words=commande.split(" ")
	for elmt in words:
		if elmt in commandes_nefastes:
			return True
	return False
		
# Fonction de traitement des touches pressées
def on_keypress(key):
    global commande_en_cours

    # Vérifier si la touche est un caractère imprimable
    if hasattr(key, 'char'):
        touche = key.char
    else:
        # Utiliser le nom de la touche pour les touches spéciales
        touche = key.name
    
    if key==keyboard.Key.space:
    	commande_en_cours+=" "
    elif key==keyboard.Key.shift:
    	pass
    elif key == keyboard.Key.enter:
    	
        if commande_en_cours:
            # Analyse de la commande en cours
            if commande_en_cours=="gatekeepr":
            	QuitMainProgram()
            	simulate_end()
            if commande_en_cours=="exit":
            	simulate_end()
            if check_command(commande_en_cours):
                write_file("/var/log/GateKeepr.log","\nLa commande en cours est détectée comme potentiellement néfaste. L'exécution est bloquée.")

            # Réinitialisation de la commande en cours
            commande_en_cours = ""
            
    #Permet de supprimer un element de la commande en cours 
    elif key == keyboard.Key.backspace:
        # Suppression du dernier caractère de la commande en cours
        commande_en_cours = commande_en_cours[:-1]
    
    # Vérifier si le raccourci Ctrl est pressé
    elif key == keyboard.Key.ctrl:
    	write_file("/var/log/GateKeepr.log","Attention vous avez appuye sur la touche Controle\nCela peut etre malveillant ! ")
    	#simulate_end()
    	
    # Vérifier si le raccourci alt est pressé
    elif key == keyboard.Key.alt:
    	write_file("/var/log/GateKeepr.log","Attention vous avez appuye sur la touche Alt\nCela peut etre malveillant !")
    	#simulate_end()
    	
    elif key == keyboard.Key.cmd:
    	write_file("/var/log/GateKeepr.log","Attention vous avez appuye sur la touche Windows\nCela peut etre malveillant ! ")
    	#simulate_end()
    	
    else:
        # Ajout de la touche à la commande en cours
        commande_en_cours += touche

# Exécute toutes les commandes du buffer
def executer_commandes_buffer():
    print("Exécution des commandes :")
    for commande in commandes_buffer:
        subprocess.call(commande, shell=True)
        print(f"- {commande}")
    print("Fin de l'exécution des commandes.")

    # Réinitialisation du buffer
    commandes_buffer.clear()

# Ajout du gestionnaire d'événements pour intercepter les touches pressées
listener = keyboard.Listener(on_press=on_keypress)
listener.start()

# Charger la blacklist depuis un fichier
load_blacklist("/var/GateKeepr/Securite/blacklist.txt")

# Changer la disposition du clavier en français
subprocess.call(['setxkbmap', 'fr'])


# Bloquer le raccourci
block_shortcuts()

# Boucle principale pour maintenir le programme en cours d'exécution
try:
    listener.join()
except KeyboardInterrupt:
    pass

