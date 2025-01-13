import sqlite3

class Base_donnée:
    def __init__(self,name,dict):
        self.name = name
        self.dict = dict
    
    def database(self):
        ma_base = sqlite3.connect(f"database_{self.name}.db")
        interact = ma_base.cursor()
        interact.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.name}'")
        table_exist = interact.fetchone()  # vérifie si existe , sinon = None

        if not table_exist:
            items = []
            for key,type_key in self.dict.items():
                items.append(f"{key} {type_key}")
            txt = ", ".join(items)

            interact.execute(f'CREATE TABLE {self.name} (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, {txt})')
            ma_base.commit()  # enregistre les données
        ma_base.close()
    
    def lire_database(self):
        ma_base = sqlite3.connect(f"database_{self.name}.db")
        interact = ma_base.cursor()
        interact.execute(f"SELECT * FROM {self.name}")
        affichage = interact.fetchall()  # affecte le résultat de l'execute
        ma_base.close()
        return affichage

    def ajout_database(self,liste):
        ma_base = sqlite3.connect("database_recettes.db")
        interact = ma_base.cursor()
        
        keys = ", ".join(self.dict.keys())
        Interrogation = ", ".join("?" * len(self.dict))

        interact.execute(f"INSERT INTO recettes (name, {keys}) VALUES (?, {Interrogation})", (liste))   
        ma_base.commit()
        ma_base.close()
        return True

    def supprimer_ele_database(self,id):
        ma_base = sqlite3.connect("database_recettes.db")
        interact = ma_base.cursor()
        interact.execute("DELETE FROM recettes WHERE id = ?", (id,))
        ma_base.commit()
        ma_base.close()
"""
maBD = Base_donnée("recettes",{"ingredients":"DICT","instructions":"DICT"})
maBD.database()
print(maBD.lire_database())

maBD.ajout_database(liste = ('brownie','{"oeufs":2}','{"mélanger":10}'))

test = '{"oeufs":2}'

print(eval(test)) #convertis en dico
"""
