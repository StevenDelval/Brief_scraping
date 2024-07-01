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
from sqlalchemy.exc import IntegrityError
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
        self.Session = sessionmaker(bind=engine,autoflush=False)

    def process_item(self, item, spider):
        session = self.Session()
        try:
            # Check if film already exists
            existing_film = session.query(Film).filter_by(
                titre=item['titre'],
                date=item['date'],
                realisateur=item['realisateur']
            ).first()

            if existing_film:
                film = existing_film
            else:
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

            # Add actors
            acteur_list = []
            for acteur_item in item["acteurs"].split(", "):
                acteur_item_split = acteur_item.split(" ")
                acteur_first_name = " ".join(acteur_item_split[:-1])
                acteur_last_name = acteur_item_split[-1]

                acteur = session.query(Acteur).filter_by(
                    acteur_first_name=acteur_first_name,
                    acteur_last_name=acteur_last_name
                ).first()

                if not acteur:
                    acteur = Acteur(
                        acteur_first_name=acteur_first_name,
                        acteur_last_name=acteur_last_name
                    )
                    session.add(acteur)
                    session.commit()

                acteur_list.append(acteur)
            
            # Add genres
            genre_list = []
            for genre_item in item["genre"].split(", "):
                genre = session.query(Genre).filter_by(genre_name=genre_item).first()
                
                if not genre:
                    genre = Genre(genre_name=genre_item)
                    session.add(genre)
                    session.commit()
                
                genre_list.append(genre)

            # Add languages
            langue_list = []
            for langue_item in item["langue"].split(", "):
                langue = session.query(Langue).filter_by(langue_name=langue_item).first()
                
                if not langue:
                    langue = Langue(langue_name=langue_item)
                    session.add(langue)
                    session.commit()
                
                langue_list.append(langue)

            # Add relations

            film.genres = genre_list
            film.langues = langue_list
            film.acteurs = acteur_list

            session.add(film)
            session.commit()

        except IntegrityError as e:
            session.rollback()
            print(f"Error saving item due to integrity error: {e}")
            raise DropItem(f"Error saving item due to integrity error: {e}")
        except Exception as e:
            session.rollback()
            print(f"Error processing item: {e}")
            raise DropItem(f"Error processing item: {e}")
        finally:
            session.close()

        return item
