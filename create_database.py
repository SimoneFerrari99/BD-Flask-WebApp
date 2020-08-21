#Progetto basi di dati 2020 - Tema Cinema
#Gruppo: ArceCity
#Membri: Casarotti Giulio, Ferrari Simone, Trolese Gulio

#File: create_database.py
#Descrizione: Creazione del database

#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, Time, Float, Boolean, Text, ForeignKey
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy.dialects.postgresql import ENUM

#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
# postgre dialect doc https://docs.sqlalchemy.org/en/13/dialects/postgresql.html
# usiamo le dbapi psycopg2
# api url: https://docs.sqlalchemy.org/en/13/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg2
# engine = create_engine(
# "postgres+psycopg2://postgres:ciao@serversrv.ddns.net:2345/progetto2020")
engine = create_engine("postgres+psycopg2://giulio:Giulio99:)@/progettobd")
#engine = create_engine("postgres+psycopg2://postgres:simone@localhost/progettoBD2020")

# funzione di sqlalchemy_utils che, se non esiste l'url del database, lo crea
if database_exists(engine.url): #elimina se esiste e lo ricrea
    drop_database(engine.url)
if not database_exists(engine.url):
    create_database(engine.url)

metadata = MetaData()  # oggetto su cui vengono salvate le tabelle


#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#

utenti = Table('utenti', metadata,
                Column('nome', String(255)),
                Column('cognome', String(255)),
                Column('data_nascita', Date),
                # String(320) perchè lo standard prevede 64 per il nome utente, @, 255 caratteri per il dominio
                Column('email', String(320), primary_key=True),
                # la nostra password verrà criptata tramite flask-bcrypt, 60 è una lunghezza di default di bycript
                Column('password', String(60), nullable=False),
                Column('is_admin', Boolean),
                Column('saldo', Float)
                )

film = Table('film', metadata,
             Column('id_film', Integer, primary_key=True),
             Column('titolo', String(255)),
             Column('durata', Integer),
             Column('descrizione', Text),
             )

genere = Table('genere', metadata,
             Column('tipo', String(255), primary_key=True)
             )

persone = Table('persone', metadata,
                Column('id_persona', Integer, primary_key=True),
                Column('nome', String(255)),
                Column('cognome', String(255))
                )

sale = Table('sale', metadata,
             Column('n_sala', Integer, primary_key=True),
             Column('n_posti', Integer)
             )

genere_film = Table('genere_film', metadata,
                   Column('id_film', Integer, ForeignKey(
                       "film.id_film"), nullable=False),
                   Column('tipo_genere', String(255), ForeignKey(
                       "genere.tipo"), nullable=False)
                   )

proiezioni = Table('proiezioni', metadata,
                   Column('id_proiezione', Integer, primary_key=True),
                   Column('data', Date),
                   Column('ora_inizio', Time),
                   Column('sala', Integer, ForeignKey(
                       "sale.n_sala"), nullable=False),
                   Column('film', Integer, ForeignKey(
                       "film.id_film"), nullable=False)
                   )

posti = Table('posti', metadata,
              Column('id_posto', Integer, primary_key=True),
              Column('prezzo', Float),
              Column('prenotato', String(320), ForeignKey("utenti.email")),
              Column('proiezioni', Integer, ForeignKey(
                  "proiezioni.id_proiezione"), nullable=False)
              )

attori = Table('attori', metadata,
               Column('id_persona', Integer, ForeignKey(
                   "persone.id_persona"), primary_key=True),
               Column('id_film', Integer, ForeignKey(
                   "film.id_film"), primary_key=True)
               )

registi = Table('registi', metadata,
                Column('id_persona', Integer, ForeignKey(
                    "persone.id_persona"), primary_key=True),
                Column('id_film', Integer, ForeignKey(
                    "film.id_film"), primary_key=True)
                )

metadata.create_all(engine)

#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#

# TODO:

#       1) Creare un utente nel db per ogni utente del nostro sito, identificato da un nome utente (email) e Password (password)
#       2) Definiamo due ruoli: admin con tutti i permessi e cliente con permessi limitati
#       3) Diamo il ruolo giusto ad ogni utente

conn = engine.connect()


conn.execute("DROP USER IF EXISTS cliente")
conn.execute("DROP USER IF EXISTS admin")

conn.execute("CREATE USER cliente WITH PASSWORD 'passwordcliente'")
conn.execute("CREATE USER admin WITH PASSWORD 'passwordadmin'")

conn.execute("DROP ROLE IF EXISTS clienti")
conn.execute("DROP ROLE IF EXISTS superuser")

conn.execute("CREATE ROLE clienti")
conn.execute("CREATE ROLE superuser SUPERUSER")

conn.execute("GRANT SELECT ON ALL TABLES IN SCHEMA public TO clienti")

conn.execute("GRANT clienti TO cliente")
conn.execute("GRANT superuser TO admin")



#conn.execute([{"CREATE ROLE admin"}
#              {"CREATE ROLE customer"}])

#conn.execute()


#GRANT ALL PRIVILEGES ON DATABASE progettobd TO admin;
