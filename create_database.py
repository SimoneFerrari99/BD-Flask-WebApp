# Progetto basi di dati 2020 - Tema Cinema
#Gruppo: ArceCity
# Membri: Casarotti Giulio, Ferrari Simone, Trolese Gulio

#File: create_database.py
# Descrizione: Creazione del database

#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, Time, Float, Boolean, Text, ForeignKey, PrimaryKeyConstraint
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy.dialects.postgresql import ENUM

#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
# postgre dialect doc https://docs.sqlalchemy.org/en/13/dialects/postgresql.html

# usiamo le dbapi psycopg2
# api url: https://docs.sqlalchemy.org/en/13/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg2
#e ngine = create_engine("postgres+psycopg2://postgres:ciao@109.115.89.210:2345/progettobd")
# engine = create_engine("postgres+psycopg2://giulio:Giulio99:)@/progettobd")
engine = create_engine("postgres+psycopg2://postgres:simone@localhost:5433/progettobd")

# engine = create_engine("postgres+psycopg2://NOMEUTENTE:PASSWORD@localhost/progettobd") da mettere in riga 20 #modifica qui le tue credenziali


# funzione di sqlalchemy_utils che, se non esiste l'url del database, lo crea
if database_exists(engine.url):  # elimina se esiste e lo ricrea
    drop_database(engine.url)
if not database_exists(engine.url):
    create_database(engine.url)

metadata = MetaData()  # oggetto su cui vengono salvate le tabelle


#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
utenti = Table('utenti', metadata,
               Column('nome', String(255), nullable = False),
               Column('cognome', String(255), nullable = False),
               Column('data_nascita', Date),
               # String(320) perchè lo standard prevede 64 per il nome utente, @, 255 caratteri per il dominio
               Column('email', String(320), primary_key=True),
               # la nostra password verrà criptata tramite flask-bcrypt, 60 è una lunghezza di default di bycript
               Column('password', String(60), nullable=False),
               Column('is_admin', Boolean),
               Column('is_manager', Boolean),
               Column('saldo', Float)
               )

film = Table('film', metadata,
             Column('id_film', Integer, primary_key=True),
             Column('titolo', String(255), nullable = False),
             Column('durata', Integer),
             Column('descrizione', Text),
             )

genere = Table('genere', metadata,
               Column('tipo', String(255), primary_key=True)
               )

persone = Table('persone', metadata,
                Column('id_persona', Integer, primary_key=True),
                Column('nome', String(255), nullable = False),
                Column('cognome', String(255))
                )

sale = Table('sale', metadata,
             Column('n_sala', Integer, primary_key=True),
             Column('n_posti', Integer)
             )

genere_film = Table('genere_film', metadata,
                    Column('id_film', Integer, ForeignKey(
                        "film.id_film", onupdate="CASCADE", ondelete="CASCADE"), nullable=False),
                    Column('tipo_genere', String(255), ForeignKey(
                        "genere.tipo", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
                    )

proiezioni = Table('proiezioni', metadata,
                   Column('id_proiezione', Integer, primary_key=True),
                   Column('data', Date),
                   Column('ora_inizio', Time),
                   Column('sala', Integer, ForeignKey(
                       "sale.n_sala", onupdate="CASCADE", ondelete="CASCADE"), nullable=False),
                   Column('film', Integer, ForeignKey(
                       "film.id_film", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
                   )

posti = Table('posti', metadata,
              Column('id_posto', Integer, nullable=False),
              Column('prezzo', Float),
              Column('prenotato', String(320), ForeignKey(
                  "utenti.email", onupdate="CASCADE", ondelete="SET NULL")),
              Column('id_proiezione', Integer, ForeignKey(
                  "proiezioni.id_proiezione", onupdate="CASCADE", ondelete="CASCADE"), nullable=False),
              PrimaryKeyConstraint('id_posto', 'id_proiezione', name='posti_pk')
              )

attori = Table('attori', metadata,
               Column('id_persona', Integer, ForeignKey(
                   "persone.id_persona", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
               Column('id_film', Integer, ForeignKey(
                   "film.id_film", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
               )

registi = Table('registi', metadata,
                Column('id_persona', Integer, ForeignKey(
                    "persone.id_persona", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
                Column('id_film', Integer, ForeignKey(
                    "film.id_film", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
                )

metadata.create_all(engine)

#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
# Creazione ruoli e assegnazione permessi
conn = engine.connect()

conn.execute("DROP USER IF EXISTS admin")
conn.execute('DROP USER IF EXISTS manager')
conn.execute("DROP USER IF EXISTS cliente")
conn.execute("DROP USER IF EXISTS anonim")

conn.execute("CREATE USER admin WITH PASSWORD 'passwordadmin'")
conn.execute("CREATE USER manager WITH PASSWORD 'passwordmanager'")
conn.execute("CREATE USER cliente WITH PASSWORD 'passwordcliente'")
conn.execute("CREATE USER anonim WITH PASSWORD 'passwordanonim'")

conn.execute("DROP ROLE IF EXISTS superuser")
conn.execute("DROP ROLE IF EXISTS managers")
conn.execute("DROP ROLE IF EXISTS clienti")
conn.execute("DROP ROLE IF EXISTS anonimous")

conn.execute("CREATE ROLE superuser WITH SUPERUSER CREATEDB CREATEROLE LOGIN")
conn.execute("CREATE ROLE managers WITH SUPERUSER LOGIN")
conn.execute("CREATE ROLE clienti WITH LOGIN")
conn.execute("CREATE ROLE anonimous WITH LOGIN")

conn.execute("GRANT SELECT ON ALL TABLES IN SCHEMA public TO clienti")
conn.execute("GRANT UPDATE ON utenti TO clienti")
conn.execute("GRANT INSERT ON posti TO clienti")

conn.execute("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO superuser")
conn.execute("GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO superuser")

conn.execute("GRANT SELECT ON ALL TABLES IN SCHEMA public TO managers")
conn.execute("GRANT UPDATE ON ALL TABLES IN SCHEMA public TO managers")
conn.execute("GRANT INSERT ON ALL TABLES IN SCHEMA public TO managers")
conn.execute("GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO managers")

conn.execute("GRANT SELECT ON ALL TABLES IN SCHEMA public TO anonimous")
conn.execute("GRANT INSERT ON utenti TO anonimous")

conn.execute("GRANT superuser TO admin")
conn.execute("GRANT managers TO manager")
conn.execute("GRANT clienti TO cliente")
conn.execute("GRANT anonimous TO anonim")

#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
# Definizione dei TRIGGER

conn.execute('''create or replace function refund() returns trigger as $refund$
               BEGIN
                   UPDATE utenti
                   SET saldo = sottoquery.vecchio_saldo + sottoquery.da_rimborsare
                   FROM (SELECT u.email, u.saldo as vecchio_saldo, sum(p.prezzo) as da_rimborsare
                         FROM utenti u JOIN posti p ON (u.email = p.prenotato)
                         WHERE p.id_proiezione = OLD.id_proiezione
                         GROUP BY u.email, u.saldo) AS sottoquery
                   WHERE utenti.email = sottoquery.email;
                   RETURN OLD;
               END;
               $refund$ LANGUAGE plpgsql;''')

conn.execute('''CREATE TRIGGER refund
               BEFORE DELETE ON proiezioni
               FOR EACH ROW
               WHEN (OLD.data > current_date OR (OLD.data = current_date AND OLD.ora_inizio > current_time))
               EXECUTE PROCEDURE refund()''')
