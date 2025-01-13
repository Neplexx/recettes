import sys , sqlite3
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from mainWindow_ui import *
from QuantitéDialog_ui import *
from RecetteDialog_ui import *
from sql import Base_donnée
from functools import partial

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(1080, 800)

        self.oldPos = None
        self.ui.closeButon.clicked.connect(self.exit)
        self.ui.minimizeButon.clicked.connect(self.minimize)
        self.ui.fullscreenButon.clicked.connect(self.fullscreen)
        self.plein_ecran = False

        self.ui.stackedWidget.setCurrentWidget(self.ui.recettePage)
        self.ui.recetteButon.clicked.connect(self.recettePage)
        self.ui.ajoutButon.clicked.connect(self.ajoutPage)

        self.recetteSelected = QIcon("assets/recetteSelected")
        self.recetteNotSelected = QIcon("assets/recetteNotSelected")
        self.ajoutSelected = QIcon("assets/addSelected")
        self.ajoutNotSelected = QIcon("assets/addNotSelected")

        self.ui.ingredientBox.clear()

        self.maBD = Base_donnée("recettes",{"ingredients":"DICT","instructions":"DICT","personne":"INT"})
        self.maBD.database()

        self.ajoutBack()
    
    def ajoutBack(self):
        self.fruits = ['Abricots', 'Ananas', 'Avocats', 'Bananes', 'Cassis', 'Cerises', 'Citrons', 'Cranberry', 'Dattes', 'Figues', 'Fraises', 'Framboises', 'Fruit de la passion', 'Grenade', 'Groseilles', 'Kiwis', 'Litchi', 'Mandarines', 'Mangues', 'Melons', 'Mirabelles', 'Myrtilles', 'Mûres', 'Noix de coco', 'Oranges', 'Pamplemousses', 'Pastèques', 'Poires', 'Pommes', 'Prunes', 'Pêches', 'Quetsches', 'Raisins', 'Tomates', 'Tomates cerises']
        self.viande_poissons = ["Boeuf","Porc","Poulet","Veau","Canard","Dinde","Sanglier","Saumon","Thon","Moules","Sardines"]
        self.patisserie = ["Sucre","Levure","Farine","Beurre","Yaourt","Fromage","Crème fraiche","Oeufs","Chocolat","Vanille","Miel","Pâte feuilletée","Pâte brisée","Pâte sablée","Pâte à pizza","Sel","Sucre vanillé"]
        self.instructions = ["Faire préchauffer","Mélanger","Enfourner","Faire fondre","Battre","Ajouter","Verser","Laisser refroidir","Démouler","Tapisser"]

        self.ui.ingredientBox.addItem("")
        self.ui.instructionBox.addItem("")
        for ele in self.fruits+self.viande_poissons+self.patisserie:
            self.ui.ingredientBox.addItem(ele)
        for ele in self.instructions:
            self.ui.instructionBox.addItem(ele)           
        self.ui.ingredientBox.currentIndexChanged.connect(self.quantité_dialog)
        self.ui.instructionBox.currentIndexChanged.connect(self.instructions_dialog)

        self.dico_ingredients = {}
        self.dico_instructions = {}

        self.ui.envoieRecetteButon.clicked.connect(self.connection_BD)

        self.recetteButonsList()

    def recetteButonsList(self):
        """permet l'ajout et actualisation des boutons de la liste principale"""
        for recette in self.maBD.lire_database():
            button_recette = QPushButton(recette[1])
            button_recette.setFixedSize(200,50)
            button_recette.setStyleSheet("QPushButton{ border-width:2px; border-radius:10px; border-style:solid; border-color:#ff978d;color:#837d99;}QPushButton::hover{ background-color:#fbc4b7;}")
            button_recette.clicked.connect(partial(self.recette_dialog,recette))    #permet l'argument changeant à chaque entrée
            font = QFont("Arial",15)
            button_recette.setFont(font)
            self.ui.LayoutVbutons.addWidget(button_recette)
            self.ui.LayoutVbutons.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

    def connection_BD(self):
        """relier au bouton ajouter , permet l'envoie vers la BD et appelle à l'actualisation/nettoyage"""
        nom = self.ui.nomAjout.toPlainText()
        ingredients = f"{self.dico_ingredients}"
        instructions = f"{self.dico_instructions}"
        personne = self.ui.personneSpinBox.value()
        if not nom == "" or ingredients == {} or instructions == {}:
            self.maBD.ajout_database(liste=(nom,ingredients,instructions,personne))
            self.ui.nomAjout.clear()
            self.ui.ingredientTextEdit.clear()
            self.ui.instructionTextEdit.clear()
            self.dico_ingredients = {}
            self.dico_instructions = {}

        self.clear_layout(self.ui.LayoutVbutons) #retire tous les boutons avant de remettre à jour avec les nouveaux
        self.recetteButonsList()
    
    def clear_layout(self,layout):
        """récupère à chaque fois le premier élément puis le supprime , permet de supprimer tous les widgets d'un layout"""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget != None:
                widget.deleteLater()
    
    def quantité_dialog(self):
        selected_item = self.ui.ingredientBox.currentText()
        if self.ui.ingredientBox.currentText() != "": #permet de retourner sur la case vide sans activer le QDialog
            dialog = QuantitéDialog("Quantité :")
            result = dialog.exec()
            if result == QDialog.Accepted:
                quantité = dialog.get_info()
                self.ui.ingredientBox.setCurrentIndex(0)
                self.dico_ingredients[selected_item] = quantité
                txt = ""
                for ingredient , combien in self.dico_ingredients.items():
                    txt += f"- {ingredient} : {combien}\n\n"
                self.ui.ingredientTextEdit.setText(txt)
                self.ui.instructionBox.setCurrentIndex(0)
    
    def instructions_dialog(self):
        selected_item = self.ui.instructionBox.currentText()
        if self.ui.instructionBox.currentText() != "":
            dialog = QuantitéDialog("Durée ou Instruction supplémentaire :")
            result = dialog.exec()
            if result == QDialog.Accepted:
                instruction = dialog.get_info()
                self.dico_instructions[selected_item] = instruction
                txt = ""
                for choix_instruction , durée in self.dico_instructions.items():
                    txt += f"- {choix_instruction} : {durée}\n\n"
                self.ui.instructionTextEdit.setText(txt)
                self.ui.instructionBox.setCurrentIndex(0)
    
    def recette_dialog(self,recette):
        recetteDialog = RecetteDialog()
        nom = recette[1]
        ingredients_dico = eval(recette[2])
        ingredients_txt = ""
        for ingredient , combien in ingredients_dico.items():
            ingredients_txt += f"- {ingredient} : {combien}\n\n"

        instructions_dico = eval(recette[3])
        instructions_txt = ""
        for choix_instruction , durée in instructions_dico.items():
            instructions_txt += f"- {choix_instruction} : {durée}\n\n"       
        personne = str(recette[4])

        recetteDialog.affiche_recette(nom,ingredients_txt,instructions_txt,personne)
        result = recetteDialog.exec()
        if result == QDialog.Rejected:
            self.maBD.supprimer_ele_database(recette[0]) # = id
            self.clear_layout(self.ui.LayoutVbutons)
            self.recetteButonsList()
  
    def ajoutPage(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.AjoutPage)
        
        self.ui.ajoutButon.setStyleSheet("background-color:#e66558; border-radius:10px; border:10px")
        self.ui.recetteButon.setStyleSheet("QPushButton{ border-width:2px; border-radius:10px; border-style:solid; border-color:#ff978d;}QPushButton::hover{background-color:#fbc4b7;}")

        self.ui.ajoutButon.setIcon(self.ajoutSelected)
        self.ui.recetteButon.setIcon(self.recetteNotSelected)

    def recettePage(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.recettePage)

        self.ui.ajoutButon.setStyleSheet("QPushButton{ border-width:2px; border-radius:10px; border-style:solid; border-color:#ff978d;}QPushButton::hover{background-color:#fbc4b7;}")
        self.ui.recetteButon.setStyleSheet("background-color:#e66558; border-radius:10px; border:10px")

        self.ui.ajoutButon.setIcon(self.ajoutNotSelected)
        self.ui.recetteButon.setIcon(self.recetteSelected)
        
    def minimize(self):
        """
        minimise la fenetre
        """
        self.showMinimized()
    
    def exit(self):
        """
        ferme l'application proprement
        """
        QApplication.quit()
    
    def fullscreen(self):
        """
        vérifie si la fenetre est en fullscreen : si oui , la rapticie et si non , la met en plein écran 
        """
        if not self.plein_ecran:
            self.showMaximized()
            self.plein_ecran = True
        else:
            self.showNormal()
            self.plein_ecran = False
    
    def mousePressEvent(self, event):
        """
        récupère la position de la souris et vérifie si elle est dans le QFrame qui représente la hotbar
        """
        pos = event.position()
        qpoint = QPoint(int(pos.x()), int(pos.y())) #convertit QPointF en QPoint et met les coordonées en entier

        if self.ui.hotbar_mouv.geometry().contains(qpoint):  # Vérifie si la position du clic est dans le QFrame
            self.oldPos = event.globalPosition() #postion global de la souris

    def mouseMoveEvent(self, event):
        """
        si oldPos existe (ce qui veut dire que la fonction mousePressEvent a été un succès) récupère les déplacements de la souris et bouge la fenetre en conséquence
        """
        if self.oldPos:
            if self.plein_ecran:
                self.showNormal()
                self.plein_ecran = False

            delta = event.globalPosition() - self.oldPos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPosition()

    def mouseReleaseEvent(self, event):
        self.oldPos = None

class QuantitéDialog(QDialog):
    def __init__(self,texte):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(400,200)

        self.ui.quantiteLineEdit.setPlaceholderText(texte)
        self.ui.validerButton.clicked.connect(self.validerEvent)
        self.ui.closeButton.clicked.connect(self.close)
        self.ui.quantiteLineEdit.returnPressed.connect(self.validerEvent)

    def get_info(self):
        return self.ui.quantiteLineEdit.text()
    
    def validerEvent(self):
        self.accept()
    
    def close(self):
        self.reject()

class RecetteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog2()
        self.ui.setupUi(self)
        self.setWindowTitle("Détails de la Recette")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(460, 131, 1000, 800)
        self.oldPos = None

        self.ui.ingredientAjout.setReadOnly(True)
        self.ui.ingredientAjout.setStyleSheet("QTextEdit {border-width:2px;border-radius:10px;border-style:solid;border-color:#ff978d;color: #635f72;background-color:#fbc4b7;}")
            
        self.ui.instructionAjout.setReadOnly(True)
        self.ui.instructionAjout.setStyleSheet("QTextEdit {border-width:2px;border-radius:10px;border-style:solid;border-color:#ff978d;color: #635f72;background-color:#fbc4b7;}")

        self.ui.closeButton.clicked.connect(self.close)
        self.ui.poubelleButon.clicked.connect(self.delete)
    
    def affiche_recette(self,name,ingrédients,instructions,personne):
        self.ui.recipe_name_label.setText(f"{name}")
        self.ui.ingredientAjout.setText(f"{ingrédients}")
        self.ui.instructionAjout.setText(f"{instructions}")
        self.ui.lineEdit.setText(personne)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.accept() 
    
    def delete(self):
        self.reject()
    
    def validerEvent(self):
        self.accept()
    
    def close(self):
        self.accept()
    
    def mousePressEvent(self, event):
        """
        récupère la position de la souris et vérifie si elle est dans le QFrame qui représente la hotbar
        """
        pos = event.position()
        qpoint = QPoint(int(pos.x()), int(pos.y())) #convertit QPointF en QPoint et met les coordonées en entier

        if self.ui.hotbar_mouv.geometry().contains(qpoint):  # Vérifie si la position du clic est dans le QFrame
            self.oldPos = event.globalPosition() #postion global de la souris

    def mouseMoveEvent(self, event):
        """
        si oldPos existe (ce qui veut dire que la fonction mousePressEvent a été un succès) récupère les déplacements de la souris et bouge la fenetre en conséquence
        """
        if self.oldPos:
            delta = event.globalPosition() - self.oldPos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPosition()

    def mouseReleaseEvent(self, event):
        self.oldPos = None

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

main()