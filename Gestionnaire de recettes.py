import sqlite3 , os , sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QWidget , QApplication , QFrame , QPushButton

def database():
    ma_base = sqlite3.connect(r"C:\Users\detal\Desktop\Recettes\database_recettes.db")
    interact = ma_base.cursor()
    interact.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='recettes'")
    table_exist = interact.fetchone() #vérifie si existe , sinon = None
    
    if not table_exist:
        interact.execute('CREATE TABLE recettes(id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, ingredients TEXT, instructions TEXT)')
        ma_base.commit() #enregistre les données
    ma_base.close()

def ajout_database(nom,ingredients,instructions):
    ma_base = sqlite3.connect(r"C:\Users\detal\Desktop\Recettes\database_recettes.db")
    interact = ma_base.cursor()
    interact.execute("INSERT INTO recettes (nom, ingredients, instructions) VALUES (?, ?, ?)", (nom, ingredients, instructions))
    ma_base.commit()
    ma_base.close()

def lire_database():
    ma_base = sqlite3.connect(r"C:\Users\detal\Desktop\Recettes\database_recettes.db")
    interact = ma_base.cursor()
    interact.execute("SELECT * FROM recettes")
    affichage = interact.fetchall() #affecte le résultat de l'execute
    ma_base.close()
    return affichage

#os.remove(r"C:\Users\detal\Desktop\Recettes\database_recettes.db") #à dégager une fois fini

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.MainInterface()
        database()
  
    def MainInterface(self):
        self.resize(1920,1080)
        self.move(0,0)
        self.setWindowTitle("Gestionnaire de recettes")
        
        fond = QFrame(self)
        fond.setStyleSheet("background-color: #212121;")
        fond.resize(1920, 1080)

        envoie_button = QPushButton(self)
        envoie_button.setFixedSize(300,40)
        envoie_button.move(800,400)
        envoie_button.clicked.connect(self.ajout)
    
    def ajout(self):
        ajout_database("ChesseCake", "Oeuf,sucre,farine", "Mélange 30 minutes et fais préchauffer")

def main():
    app = QApplication(sys.argv) #gestion des arguments d'execution
    windows = MainWindow()
    windows.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()



