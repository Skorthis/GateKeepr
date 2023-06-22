#!/usr/bin/env python3

#    ____       _         _  __                    
#   / ___| __ _| |_ ___  | |/ /___  ___ _ __  _ __ 
#  | |  _ / _` | __/ _ \ | ' // _ \/ _ \ '_ \| '__|
#  | |_| | (_| | ||  __/ | . \  __/  __/ |_) | |   
#   \____|\__,_|\__\___| |_|\_\___|\___| .__/|_|   
#                                      |_|         
#  Your security, our priority




import os
import shutil

def read_last_line():
    file_name = "/var/log/GateKeepr.log"

    with open(file_name, 'r') as file:
        lines = file.readlines()

        if lines:
            last_line = lines[-1].strip()
            return last_line
        else:
            return None


def process_log_file():
    file_name = "/var/log/GateKeepr.log"

    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    processed_lines = []
    process_line(lines, processed_lines)
    if len(processed_lines)>0 and processed_lines[-1].isdigit():
        processed_lines.pop()
    content = '\n'.join(processed_lines)
    return content


def process_line(lines, processed_lines, index=0):
    if index >= len(lines):
        return

    line = lines[index].strip()
    if len(line) > 50 and ' ' in line:
        words = line.split(' ')
        processed_line = ""
        for word in words:
            if len(processed_line) + len(word) <= 50:
                processed_line += word + " "
            else:
                processed_lines.append(processed_line.strip())
                processed_line = word + " "
        processed_lines.append(processed_line.strip())
    else:
        processed_lines.append(line)

    process_line(lines, processed_lines, index + 1)

def parse_scan_result(file_path, text_box= None):
    with open(file_path, 'r') as file:
        content = file.read()

    # Extract potential viruses
    virus_lines = content.split('\n')
    potential_viruses = []
    for line in virus_lines:
        if line.startswith('/'):
            parts = line.split(':')
            virus_location = parts[0].strip()
            virus_type = parts[1].strip()
            potential_viruses.append((virus_location, virus_type))

    # Extract number of potential viruses
    num_viruses = len(potential_viruses)

    # Extract scan time
    scan_time_line = next((line for line in virus_lines[::-1] if line.startswith('Time:')), None)
    if scan_time_line is not None:
        scan_time_parts = scan_time_line.split(':')
        scan_time_seconds = scan_time_parts[1].split()[0].strip() if scan_time_parts else ""
    else: 
         scan_time_seconds = 0

    # Build the result string
    result=""
    #result = "Résultats:\n\n"
    if num_viruses==0 and scan_time_seconds!=0:
        result+="Votre clé USB n'est pas infectée !\n"
    elif scan_time_seconds == 0:
        result+="Le périphérique a été débranché\navant la fin de l'analyse.\n\nAppuyez sur retour pour revenir à l'écran d'accueil"
    else:
        result+="Attention votre clé est compromise !\n" 
        result += "Nombre de virus potentiels: "+str(num_viruses)+"\n\n"
        result += "Emplacement des virus:\n\n"
    for virus_location, virus_type in potential_viruses:
        result += str(virus_location)+" | "+str(virus_type[:len(virus_type)-6:])+" \n"
    result += "\nTemps de scan: "+str(scan_time_seconds)+" secondes."

    # Set the result text in the PyQt label
    if text_box is not None:
        text_box.setText(result)

    return potential_viruses



def suppress_files(label):
    file_path = "/var/log/GateKeepr.log"  # Replace with the path to the log file
    virus_locations = parse_scan_result(file_path)

    if not virus_locations:
        label.setText("Pas de virus à supprimer")
        return

    result = "Conclusion : \n\n"

    for location, _ in virus_locations:
        try:
            os.remove(location)
            result += "Fichier supprimé: \n "+str(location)+"\n"
        except FileNotFoundError:
            result +="Fichier non trouvé: \n "+str(location)+"\n"
        except PermissionError:
            result +="Permission refusée: \n "+str(location)+"\n"
    label.setText(result)


def quarantine_files(label, quarantine_directory):
    #create the directory if doesn't exist
    if not os.path.exists(quarantine_directory):
        os.makedirs(quarantine_directory)


    file_path = "/var/log/GateKeepr.log"  # Replace with the path to the log file
    virus_locations = parse_scan_result(file_path)

    if not virus_locations:
        label.setText("Pas de virus à mettre en quarantaine")
        return

    result = ""


    #Join the location of the potential virus
    for location, _ in virus_locations:
        file_name = os.path.basename(str(location))
        destination = os.path.join(quarantine_directory, file_name)

        try:
            shutil.move(str(location), str(destination))
            result +="Fichier en quarantaine: \n\n "+str(location)+" \n ------> \n "+str(destination)+"\n"
        except FileNotFoundError:
            result +="Fichier non trouvé: \n "+str(location)+"\n"
        except PermissionError:
            result +="Permission refusé: \n "+str(location)+"\n"

    label.setText(result)



def copy_file_content(source_file, destination_file):
    try:
        # Open the source file in read mode
        with open(source_file, 'r') as source:
            # Read the contents of the source file
            content = source.read()

        # Open the destination file in write mode
        with open(destination_file, 'w') as destination:
            # Write the contents to the destination file
            destination.write(content)

        print("File content copied successfully!")
    except IOError:
        print("An error occurred while copying the file.")

