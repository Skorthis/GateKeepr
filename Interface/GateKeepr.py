#!/usr/bin/env python3

#    ____       _         _  __                    
#   / ___| __ _| |_ ___  | |/ /___  ___ _ __  _ __ 
#  | |  _ / _` | __/ _ \ | ' // _ \/ _ \ '_ \| '__|
#  | |_| | (_| | ||  __/ | . \  __/  __/ |_) | |   
#   \____|\__,_|\__\___| |_|\_\___|\___| .__/|_|   
#                                      |_|         
#  Your security, our priority

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget, QStackedWidget
from PyQt5.QtGui import QPixmap, QMovie, QFont, QCursor
from PyQt5.QtCore import Qt, QSize, QRect, QFileSystemWatcher, QTimer
import affichage
import psutil
import os

#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
#                                       FUNCTIONS
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------

#Function to clear the log file 
def clear_file(file_path):
    try:
            with open(file_path, 'w') as file:
                file.truncate(0)  # Truncate the file size to 0
            print(f"Contents of {file_path} cleared.")
    except IOError:
            print(f"An error occurred while clearing {file_path}.")



def switchPage(new_index, file_path=None, clear_file_flag=False):
    if clear_file_flag == False:
        window.stacked_widget.setCurrentIndex(new_index)
    else:
        file_watcher.removePath(file_path)  # Remove the file from the watcher temporarily
        clear_file(file_path)  # Clear the file
        file_watcher.addPath(file_path)  # Add the file back to the watcher
        window.stacked_widget.setCurrentIndex(new_index)

def pid_liste():
    processes=psutil.process_iter()
    name,pid=[],[]
    for process in processes:
        try :
            pid.append(process.pid)
            name.append(process.name())
			#print("PID : "+str(process.pid)+", name : "+str(process.name()))
        except (psutil.NoSuchProcess,psutil.AccessDenied,psutil.ZombieProcess):
            pass

    if "keylogger.py" in name:
        
        index = name.index("keylogger.py")
    		#print("L'index du processus 'keylogger.py' est :"+str(index))
    		#print("Le PID associe est : "+str(pid[index]))
    		# Obtenir l'identifiant de processus (PID) du programme en cours
        current_pid = pid[index]

    		# Envoyer un signal de terminaison au processus en cours
    		#os.kill(current_pid, signal.SIGINT)
        #os.system("sudo killall -e keylogger.py")
        keylogger=False
        MainWindow.switchPage(window,pageIndex=0)
        
    if "clamscan" in name:
		#index = name.index("clamscan")
		#print("L'index du processus 'clamscan' est :"+str(index))
		#print("Le PID associe est : "+str(pid[index]))
        os.system("sudo killall -e clamscan")
        MainWindow.switchPage(window,pageIndex=0)
    else : 
        MainWindow.switchPage(window,pageIndex=0)
    return

#Function to know if watcher is connected to a file
def is_file_connected(watcher,file_path):
	if len(watcher.files())>0:
		for path in watcher.files():
			return path==file_path
	else:
		return False

def WritePID():
    with open("/var/GateKeepr/Securite/pid.txt",'w') as file:
    	file.write(str(os.getpid()))
    return

#Function to put the MS Gothic font to a text 
def font_text( text, size, police, italic, bold):
    

    font_gothic = QFont()
    if police:
        font_gothic.setFamily("MS Gothic")
    else:
        font_gothic.setFamily("Arial") 
    font_gothic.setPointSize(size)
    font_gothic.setWeight(50)
    font_gothic.setItalic(italic)
    font_gothic.setBold(bold)
    text.setFont(font_gothic)

def hide_show_gif(loading_label, is_visible):
    if is_visible:
        loading_label.show()  # Affiche le QLabel contenant le GIF
        loading_label.movie().start()  # Démarre l'animation du GIF
    else:
        loading_label.hide()  # Cache le QLabel contenant le GIF
        loading_label.movie().stop()  # Arrête l'animation du GIF




#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
#                                           CLASSES
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------

class HomePage(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setObjectName("HomePage")
        self.setGeometry(0, 0, 800, 480)


        # Set background image with an animated gif
        background_label = QLabel(self)
        background_label.setGeometry(QRect(0, 0, 800, 480))
        background_label.resize(800,480)
        bg_pixmap = QPixmap("/var/GateKeepr/Interface/background_interface.png")        
        background_label.setPixmap(bg_pixmap)
        background_label.resize(bg_pixmap.width(),bg_pixmap.height())


        # Add logo
        logo_label = QLabel(self)
        logo_label.setGeometry(QRect(150,150,500,200))
        logo_pixmap = QPixmap("/var/GateKeepr/Interface/logo.png")
        logo_pixmap2 = logo_pixmap.scaled(500,200)
        logo_label.setPixmap(logo_pixmap2)
        


        #Add the background behind the logo
        bg_label = QLabel(self)
        bg_label.setGeometry(QRect(150, 140, 510, 210))
        bg_label.setStyleSheet(""" 
            background-color:rgba(0, 0, 0, 60);
            border-radius : 20px 
        """)

        
        #Add the analyse button 
        #button_analyse = QPushButton("Analyser", self)
        #button_analyse.setObjectName("pushButton")
        #button_analyse.setGeometry(QRect(310,350,200,80))
        #button_analyse.clicked.connect(lambda: switchPage(0, 1))
        #button_analyse.setStyleSheet("""
                    #QPushButton#pushButton{
                     #   background-color:rgba(0,255,255);
                      #  border-radius : 20px;
                    #}

                    #QPushButton#pushButton:hover{
                    #    background-color:rgba(32,220,220);                    
                    #} 

        #""")


        #Add the quit button 
        #quit_button = QPushButton("Quitter", self)
        #quit_button.setObjectName("pushButton1")
        #quit_button.setGeometry(QRect(15,20,70,40))
        #quit_button.clicked.connect(lambda: sys.exit(app.exec_()))
        #quit_button.setStyleSheet("""
                    #QPushButton#pushButton1{
                    #    background-color:rgba(0,255,255);
                    #    border-radius : 15px;
                    #}

                    #QPushButton#pushButton1:hover{
                    #    background-color:rgba(32,220,220);                    
                    #} 

        #""")


        #Add the background behind  the analyse page
        bg_label2 = QLabel(self)
        bg_label2.setGeometry(QRect(150, 140, 510, 210))
        bg_label2.setStyleSheet(""" 
            background-color:rgba(0, 0, 0, 180);
            border-radius : 20px 
        """)

        logo_label.raise_()

class ThirdPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 800, 480)

      # Set background image with an animated gif
        background_label = QLabel(self)
        background_label.setGeometry(QRect(0, 0, 800, 480))
        background_label.resize(800,480)
        bg_pixmap = QPixmap("/var/GateKeepr/Interface/background_interface.png")        
        background_label.setPixmap(bg_pixmap)
        background_label.resize(bg_pixmap.width(),bg_pixmap.height())

        # Add logo
        logo_label = QLabel(self)
        logo_label.setGeometry(QRect(260,10,300,120))
        logo_pixmap = QPixmap("/var/GateKeepr/Interface/logo_2.png")
        logo_pixmap2 = logo_pixmap.scaled(300,120)
        logo_label.setPixmap(logo_pixmap2)
        


        #Add the background behind the logo
        bg_label = QLabel(self)
        bg_label.setGeometry(QRect(255, 15, 300, 100))
        bg_label.setStyleSheet(""" 
            background-color:rgba(0, 0, 0, 200);
            border-radius : 20px 
        """)

        # Add text label
        global text_label_3 
        text_label_3= QLabel(self)
        text_label_3.setGeometry(QRect(105,130,590,320))
        text_label_3.setAlignment(Qt.AlignCenter)
        font_text(text_label_3,15,True,False,True)
        text_label_3.setStyleSheet("""
                color: white;
        """)

        #Add the background behind the text
        bg_text = QLabel(self)
        bg_text.setGeometry(QRect(98, 130, 600, 320))
        bg_text.setStyleSheet(""" 
            background-color:rgba(0, 0, 0, 200);
            border-radius : 20px 
        """)



        # Add back button
        back_button = QPushButton("Retour", self)
        back_button.setObjectName("pushButton")
        back_button.setGeometry(QRect(15,15,55,35))
        back_button.setStyleSheet("""
                    QPushButton#pushButton{
                        background-color:rgba(0,255,255);
                        border-radius : 5px;
                    }

                    QPushButton#pushButton:hover{
                        background-color:rgba(32,220,220);                    
                    } 

        """)
        font_text(back_button,8,False,False,True)

        # Connect the event for the back button
        back_button.clicked.connect(lambda: switchPage(0, file_path="/var/log/GateKeepr.log", clear_file_flag=True))



        # Add suppress button
        suppress_button = QPushButton("Nettoyer", self)
        suppress_button.setObjectName("pushButton1")
        suppress_button.setGeometry(QRect(300,140,80,50))
        suppress_button.setStyleSheet("""
                    QPushButton#pushButton1{
                        background-color:rgba(0,255,255);
                        border-radius : 5px;
                    }

                    QPushButton#pushButton1:hover{
                        background-color:rgba(32,220,220);                    
                    } 

        """)


        font_text(suppress_button,8,False,False,True)
        # Connect the event for the back button
        suppress_button.clicked.connect( lambda : affichage.suppress_files(text_label_3))



        # Add quarantine button
        quarantine_button = QPushButton("Quarantaine", self)
        quarantine_button.setObjectName("pushButton2")
        quarantine_button.setGeometry(QRect(400,140,120,50))
        quarantine_button.setStyleSheet("""
                    QPushButton#pushButton2{
                        background-color:rgba(0,255,255);
                        border-radius : 5px;
                    }

                    QPushButton#pushButton2:hover{
                        background-color:rgba(32,220,220);                    
                    } 

        """)


        font_text(quarantine_button,8,False,False,True)
        # Connect the event for the back button
        quarantine_button.clicked.connect( lambda : affichage.quarantine_files(text_label_3,"/var/GateKeepr/quarantine"))


        logo_label.raise_()
        text_label_3.raise_()
        suppress_button.raise_()
        quarantine_button.raise_()



class SecondPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 800, 480)

      # Set background image with an animated gif
        background_label = QLabel(self)
        background_label.setGeometry(QRect(0, 0, 800, 480))
        background_label.resize(800,480)
        bg_pixmap = QPixmap("/var/GateKeepr/Interface/background_interface.png")        
        background_label.setPixmap(bg_pixmap)
        background_label.resize(bg_pixmap.width(),bg_pixmap.height())

        # Add logo
        logo_label = QLabel(self)
        logo_label.setGeometry(QRect(260,10,300,120))
        logo_pixmap = QPixmap("/var/GateKeepr/Interface/logo_2.png")
        logo_pixmap2 = logo_pixmap.scaled(300,120)
        logo_label.setPixmap(logo_pixmap2)
        


        #Add the background behind the logo
        bg_label = QLabel(self)
        bg_label.setGeometry(QRect(255, 15, 300, 100))
        bg_label.setStyleSheet(""" 
            background-color:rgba(0, 0, 0, 200);
            border-radius : 20px 
        """)

        # Add text label
        global text_label_2 
        text_label_2= QLabel(self)
        text_label_2.setGeometry(QRect(105,130,590,320))
        text_label_2.setAlignment(Qt.AlignCenter)
        font_text(text_label_2,15,True,False,True)
        text_label_2.setStyleSheet("""
                color: white;
        """)

        #Add the background behind the text
        bg_text = QLabel(self)
        bg_text.setGeometry(QRect(98, 130, 600, 320))
        bg_text.setStyleSheet(""" 
            background-color:rgba(0, 0, 0, 200);
            border-radius : 20px 
        """)
        
        
        # Add loading animation only if usb key inserted
        usb_boolean = affichage.read_last_line()
        global loading_label
        loading_label = QLabel(self)
        loading_label.setGeometry(QRect(85,320,500,200))
        loading_label.resize(500,200)
        movie = QMovie("/var/GateKeepr/Interface/animation-waiting.gif")
        loading_label.setMovie(movie)
        movie.start()
        hide_show_gif(loading_label, False)

        # Add back button
        back_button = QPushButton("Retour", self)
        back_button.setObjectName("pushButton")
        back_button.setGeometry(QRect(15,15,55,35))
        back_button.setStyleSheet("""
                    QPushButton#pushButton{
                        background-color:rgba(0,255,255);
                        border-radius : 5px;
                    }

                    QPushButton#pushButton:hover{
                        background-color:rgba(32,220,220);                    
                    } 

        """)
        font_text(back_button,8,False,False,True)

        # Connect the event for the back button
        back_button.clicked.connect(lambda: switchPage(0, file_path="/var/log/GateKeepr.log", clear_file_flag=True))



        logo_label.raise_()
        text_label_2.raise_()
        if usb_boolean == "2":
            loading_label.raise_()


class FourthPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 800, 480)

      # Set background image with an animated gif
        background_label = QLabel(self)
        background_label.setGeometry(QRect(0, 0, 800, 480))
        background_label.resize(800,480)
        bg_pixmap = QPixmap("/var/GateKeepr/Interface/background_interface.png")        
        background_label.setPixmap(bg_pixmap)
        background_label.resize(bg_pixmap.width(),bg_pixmap.height())

        # Add logo
        logo_label = QLabel(self)
        logo_label.setGeometry(QRect(260,10,300,120))
        logo_pixmap = QPixmap("/var/GateKeepr/Interface/logo_2.png")
        logo_pixmap2 = logo_pixmap.scaled(300,120)
        logo_label.setPixmap(logo_pixmap2)
        


        #Add the background behind the logo
        bg_label = QLabel(self)
        bg_label.setGeometry(QRect(255, 15, 300, 100))
        bg_label.setStyleSheet(""" 
            background-color:rgba(0, 0, 0, 200);
            border-radius : 20px 
        """)

        # Add text label
        global text_label_4 
        text_label_4= QLabel(self)
        text_label_4.setGeometry(QRect(105,130,590,320))
        text_label_4.setAlignment(Qt.AlignCenter)
        font_text(text_label_4,15,True,False,True)
        text_label_4.setStyleSheet("""
                color: white;
        """)

        #Add the background behind the text
        bg_text = QLabel(self)
        bg_text.setGeometry(QRect(98, 130, 600, 320))
        bg_text.setStyleSheet(""" 
            background-color:rgba(0, 0, 0, 200);
            border-radius : 20px 
        """)



        # Add back button
        back_button = QPushButton("Retour", self)
        back_button.setObjectName("pushButton")
        back_button.setGeometry(QRect(15,15,55,35))
        back_button.setStyleSheet("""
                    QPushButton#pushButton{
                        background-color:rgba(0,255,255);
                        border-radius : 5px;
                    }

                    QPushButton#pushButton:hover{
                        background-color:rgba(32,220,220);                    
                    } 

        """)
        font_text(back_button,8,False,False,True)

        # Connect the event for the back button
        back_button.clicked.connect(lambda: switchPage(0, file_path="/var/log/GateKeepr.log", clear_file_flag=True))



        logo_label.raise_()
        text_label_4.raise_()



        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #Add the size and the possibilty not to change it
        global keylogger 
        keylogger=False
        self.setGeometry(0, 0, 800, 480)
        self.setMaximumSize(QSize(800, 480))
        self.setMinimumSize(QSize(800, 480))
        
        #Name of the window
        self.setWindowTitle("GateKeepr")


        # Hide the taskbar
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda : self.updateCounter())
        self.timer.start(1000)  # Trigger every 1 second (1000 milliseconds)


        # Create a stacked widget to manage multiple pages
        global stacked_widget 
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # Create the home page and add it to the stacked widget
        home_page = HomePage()
        self.stacked_widget.addWidget(home_page)

        # Create the second page and add it to the stacked widget
        second_page = SecondPage()
        self.stacked_widget.addWidget(second_page)

        # Create the second page and add it to the stacked widget
        third_page = ThirdPage()
        self.stacked_widget.addWidget(third_page)
        
        # Create the second page and add it to the stacked widget
        Fourth_page = FourthPage()
        self.stacked_widget.addWidget(Fourth_page)

        # Show the home page by default
        self.stacked_widget.setCurrentIndex(0)
        #Index classification
        # index 0 = homepage
        # index 1 = secondpage (display usbguard)
        # index 2 = thirdpage (result clamAV scan)
        # index 3 = fourthpage (keylogger)


    def switchPage(self, pageIndex):
        self.stacked_widget.setCurrentIndex(pageIndex)


    def updateCounter(self):
        #match the correct next page depending on the next step GateKeepr will do
        current_index = self.stacked_widget.currentIndex()
        if current_index == 0:
            file_watcher.fileChanged.connect(lambda : self.switchPage(1))
            hide_show_gif(loading_label, False)
            self.stacked_widget.currentChanged.connect(lambda: text_label_2.setText(affichage.process_log_file()))
            current_index = self.stacked_widget.currentIndex()
        elif current_index == 1:
            USB_type = affichage.read_last_line()
            if USB_type == "2":
                if not is_file_connected(eject_watcher,"/var/log/eject.log"):
                    eject_watcher.addPath("/var/log/eject.log")
                hide_show_gif(loading_label, True)
                eject_watcher.fileChanged.connect(lambda: pid_liste())
                file_watcher.fileChanged.connect(lambda : switchPage(2))
                self.stacked_widget.currentChanged.connect(lambda: affichage.parse_scan_result(file_path, text_label_3))
                current_index = self.stacked_widget.currentIndex()
            elif USB_type=="3":
                if not is_file_connected(eject_watcher,"/var/log/eject.log"):
                    eject_watcher.addPath("/var/log/eject.log")
                hide_show_gif(loading_label, False)
                eject_watcher.fileChanged.connect(lambda: pid_liste())
                file_watcher.fileChanged.connect(lambda : switchPage(3))
                self.stacked_widget.currentChanged.connect(lambda : text_label_4.setText(affichage.process_log_file()))
                current_index=self.stacked_widget.currentIndex()
            else:
                #eject_watcher.fileChanged.connect(lambda: pid_liste())	
                eject_watcher.removePath("/var/log/eject.log")
                file_watcher.fileChanged.connect(lambda: text_label_2.setText(affichage.process_log_file()))
                hide_show_gif(loading_label, False)
                #self.stacked_widget.currentChanged.connect(lambda: text_label_4.setText(affichage.process_log_file()))
                current_index = self.stacked_widget.currentIndex()
        elif current_index == 2:
            if not is_file_connected(eject_watcher,"/var/log/eject.log"):
            	eject_watcher.addPath("/var/log/eject.log")
            hide_show_gif(loading_label, False)
            eject_watcher.fileChanged.connect(lambda:self.switchPage(0))
            file_watcher.fileChanged.connect(lambda:self.switchPage(0))
            current_index = self.stacked_widget.currentIndex()
        elif current_index == 3:
            keylogger=True
            if not is_file_connected(eject_watcher,"/var/log/eject.log"):
            	eject_watcher.addPath("/var/log/eject.log")
            eject_watcher.fileChanged.connect(lambda:self.switchPage(0))
            if keylogger==False:
            	file_watcher.fileChanged.connect(lambda:self.switchPage(0))
            hide_show_gif(loading_label, False)
            current_index = self.stacked_widget.currentIndex()
 


       

#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
#                                          MAIN
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":

    app = QApplication(sys.argv)
    global window 
    window = MainWindow()
    window.show()
    #To hide the cursor
    window.setCursor(QCursor(Qt.BlankCursor))

    # Start monitoring the file for changes
    file_path = "/var/log/GateKeepr.log" 
    eject_path = "/var/log/eject.log"
    
    global file_watcher,eject_watcher 
    file_watcher = QFileSystemWatcher([file_path])
    eject_watcher = QFileSystemWatcher([eject_path])

    WritePID()


    
    # if stacked_widget.currentIndex()==0:
    #     stacked_widget.currentChanged.connect(lambda : affichage.parse_scan_result(file_path,text_label))

    sys.exit(app.exec_())
