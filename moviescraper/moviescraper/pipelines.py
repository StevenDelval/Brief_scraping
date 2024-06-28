# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import datetime
import locale
import re
from itemadapter import ItemAdapter
from sqlalchemy.orm import sessionmaker
from .models import Film, Acteur, Genre, Langue, engine, film_acteur, film_genre, film_langue
from scrapy.exceptions import DropItem

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
    date_obj = datetime.strptime(date_str, "%d %B %Y")
    # Formater l'objet datetime en chaîne de caractères au format dd/mm/yyyy
    formatted_date = date_obj.strftime("%d-%m-%Y")
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

class SQLAlchemyPipeline(object):
    def __init__(self):
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        try:
            film = Film(
                titre=item['titre'],
                titre_original=item['titre_original'],
                score=item['score'],
                date=item['date'],
                duree=item['duree'],
                descriptions=item['descriptions'],
                realisateur=item['realisateur'],
                public=item['public'],
                pays=item['pays'],
                url_image=item['url_image']
            )
            session.add(film)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error saving item: {e}")
            raise DropItem(f"Error saving item: {e}")
        
        for acteur_item in item["acteurs"].split(", "):
            acteur_item_split = acteur_item.split(" ")
            try:
                acteur = Acteur(
                     acteur_first_name=str("".join(acteur_item_split[0:-1])),
                     acteur_last_name=str(acteur_item_split[-1]),
                )
                session.add(acteur)
                session.commit()
            except Exception as e:
                session.rollback()
                print(f"Error saving item: {e}")
                raise DropItem(f"Error saving item: {e}")
            finally:
                continue
            
        for genre_item in item["genre"].split(", "):
            print(genre_item)
            try:
                genre = Genre(
                     genre_name=genre_item,
                )
                session.add(genre)
                session.commit()
            except Exception as e:
                session.rollback()
                print(f"Error saving item: {e}")
                raise DropItem(f"Error saving item: {e}")
            finally:
                continue
        for langue_item in item["langue"].split(", "):
            print(langue_item)
            try:
                langue = Langue(
                     langue_name=langue_item,
                )
                session.add(langue)
                session.commit()
            except Exception as e:
                session.rollback()
                print(f"Error saving item: {e}")
                raise DropItem(f"Error saving item: {e}")
            finally:
                continue
        session.close()
        
        return item