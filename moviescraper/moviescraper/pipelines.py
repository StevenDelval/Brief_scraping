# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import datetime
import locale
import re
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

def convertion_duree(str):
    # Diviser la chaîne de caractères en une liste d'éléments séparés par des espaces
    split_liste = re.split("\s", str)
    
    # Initialiser la variable 'duree' à 0, qui contiendra la durée totale en minutes
    duree = 0
    
    # Parcourir chaque élément de la liste résultante
    for elt in split_liste:
        # Si l'élément contient un "h", cela indique des heures
        if "h" in elt:
            # Diviser l'élément par "h" et prendre la partie avant "h" (nombre d'heures)
            # Convertir ce nombre en entier et le multiplier par 60 pour obtenir des minutes
            # Ajouter ces minutes à 'duree'
            duree = int(re.split("h", elt)[0]) * 60 + duree
        # Si l'élément contient "min", cela indique des minutes
        elif "min" in elt:
            # Diviser l'élément par "m" et prendre la partie avant "min" (nombre de minutes)
            # Convertir ce nombre en entier et l'ajouter à 'duree'
            duree = int(re.split("m", elt)[0]) + duree
    
    # Retourner la durée totale en minutes
    return duree

def convert_date(date_str):
    # Convertir la chaîne de caractères en objet datetime
    date_obj = datetime.datetime.strptime(date_str, "%d %B %Y")
    # Formater l'objet datetime en chaîne de caractères au format dd/mm/yyyy
    formatted_date = date_obj.strftime("%d/%m/%Y")
    return formatted_date

class MoviescraperPipeline:

    def clean_text(self,item,list_col):
        adapter = ItemAdapter(item)
        for currency_col in list_col:
            currency_str = adapter.get(currency_col)
            if currency_str is not None:
                currency_str = currency_str.replace('\n', '')
                currency_str = currency_str.replace('\t', '')
                adapter[currency_col] = currency_str
        return item
    
    def clean_score(self,item):
        adapter = ItemAdapter(item)
        currency_str = adapter.get("score")
        if currency_str is not None:
            adapter["score"] = float(currency_str.replace(',', '.'))

        return item
    
    def clean_duree(self,item):
        adapter = ItemAdapter(item)
        currency_str = adapter.get("duree")
        if currency_str is not None:
            adapter["duree"] = convertion_duree(currency_str)
        return item
    
    def clean_date(self,item):
        
        adapter = ItemAdapter(item)
        currency_str = adapter.get("date")
        if currency_str is not None:
            adapter["date"] = convert_date(currency_str)
        return item

    def process_item(self, item, spider):

        list_col_text= item.keys()
        item = self.clean_text(item,list_col_text)
        item = self.clean_score(item)
        item = self.clean_duree(item)
        item = self.clean_date(item)

        return item


# class DataBasePipeline:
    
#     def open_spider(self, spider):
#         try:
#             self.connection = pymysql.connect(
#                 host="localhost",
#                 user="root",
#                 password=PASSWORD,
#                 database="BooksScrapy" 
#             )
#         except pymysql.err.OperationalError as e:
#             if e.args[0] == 1049:
#                 raise Exception("Erreur : La base de données 'BooksScrapy' n'existe pas.")
#             elif e.args[0] == 1045:
#                 raise Exception("Erreur : Accès refusé pour l'utilisateur 'root'@'localhost' (mot de passe incorrect).")
#             else:
#                 raise Exception(f"Erreur de connexion : {e}")
 
#         try:
#             self.cursor = self.connection.cursor()
#             self.cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS books (
#                     id SERIAL PRIMARY KEY,
#                     title TEXT,
#                     image TEXT,
#                     description TEXT,
#                     UPC TEXT,
#                     product_type TEXT,
#                     price FLOAT,
#                     price_tax FLOAT,
#                     tax FLOAT,
#                     availability INTEGER,
#                     number_of_reviews INTEGER
#                 );
#             """)
#             self.connection.commit()
#         except Exception as e:
#             self.connection.close()
#             raise Exception(f"Erreur lors de la création de la table : {e}")



#     def process_item(self, item, spider):
#         self.cursor.execute("""
#             INSERT INTO books (title, image, description, UPC, product_type, price, price_tax, tax, availability, number_of_reviews)
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
#         """, (
#             item['title'],
#             item['image'],
#             item['description'],
#             item['UPC'],
#             item['product_type'],
#             item['price'],
#             item['price_tax'],
#             item['tax'],
#             item['availability'],
#             item['number_of_reviews']
#         ))
#         self.connection.commit()
#         return item

#     def close_spider(self, spider):
#         self.cursor.close()
#         self.connection.close()