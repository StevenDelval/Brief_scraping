
from sqlalchemy import create_engine, Column, String, Integer, Float, Date, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from dotenv import load_dotenv
load_dotenv()


bdd_path = 'sqlite:///database.db'

Base = declarative_base()

# Define association tables first
film_acteur = Table(
    'film_acteur', Base.metadata,
    Column('film_titre', String, ForeignKey('film.titre')),
    Column('film_date', Date, ForeignKey('film.date')),
    Column('film_realisateur', String, ForeignKey('film.realisateur')),
    Column('acteur_id', Integer, ForeignKey('acteurs.acteur_id'))
)

film_genre = Table(
    'film_genre', Base.metadata,
    Column('film_titre', String, ForeignKey('film.titre')),
    Column('film_date', Date, ForeignKey('film.date')),
    Column('film_realisateur', String, ForeignKey('film.realisateur')),
    Column('genre_id', Integer, ForeignKey('genre.genre_id'))
)

film_langue = Table(
    'film_langue', Base.metadata,
    Column('film_titre', String, ForeignKey('film.titre')),
    Column('film_date', Date, ForeignKey('film.date')),
    Column('film_realisateur', String, ForeignKey('film.realisateur')),
    Column('langue_id', Integer, ForeignKey('langue.langue_id'))
)

# Define your classes
class Film(Base):
    __tablename__ = 'film'

    titre = Column(String, primary_key=True)
    titre_original = Column(String)
    score = Column(Float)
    date = Column(String, primary_key=True)
    duree = Column(Integer)
    descriptions = Column(String)
    realisateur = Column(String, ForeignKey('acteurs.acteur_id'), primary_key=True)
    public = Column(String)
    pays = Column(String)
    url_image = Column(String)

    acteurs = relationship('Acteur', secondary=film_acteur, 
                           primaryjoin="and_(Film.titre == film_acteur.c.film_titre, "
                                       "Film.date == film_acteur.c.film_date, "
                                       "Film.realisateur == film_acteur.c.film_realisateur)",
                           secondaryjoin="film_acteur.c.acteur_id == Acteur.acteur_id",
                           backref='films')
    
    genres = relationship('Genre', secondary=film_genre,
                          primaryjoin="and_(Film.titre == film_genre.c.film_titre, "
                                      "Film.date == film_genre.c.film_date, "
                                      "Film.realisateur == film_genre.c.film_realisateur)",
                          secondaryjoin="film_genre.c.genre_id == Genre.genre_id",
                          backref='films')

    langues = relationship('Langue', secondary=film_langue,
                           primaryjoin="and_(Film.titre == film_langue.c.film_titre, "
                                       "Film.date == film_langue.c.film_date, "
                                       "Film.realisateur == film_langue.c.film_realisateur)",
                           secondaryjoin="film_langue.c.langue_id == Langue.langue_id",
                           backref='films')

class Acteur(Base):
    __tablename__ = 'acteurs'

    acteur_id = Column(Integer,default=0, autoincrement=True)
    acteur_first_name = Column(String, primary_key=True)
    acteur_last_name = Column(String, primary_key=True)

class Genre(Base):
    __tablename__ = 'genre'

    genre_id = Column(Integer,default=0, autoincrement=True)
    genre_name = Column(String, primary_key=True)

class Langue(Base):
    __tablename__ = 'langue'

    langue_id = Column(Integer,default=0, autoincrement=True)
    langue_name = Column(String, primary_key=True)

# Configuration de la base de données (remplacez 'sqlite:///database.db' par votre base de données)
engine = create_engine(bdd_path)
Base.metadata.create_all(engine)

# Création d'une session
Session = sessionmaker(bind=engine)
session = Session()