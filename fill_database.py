# Progetto basi di dati 2020 - Tema Cinema
#Gruppo: ArceCity
# Membri: Casarotti Giulio, Ferrari Simone, Trolese Gulio

#File: fill_database.py
# Descrizione: Riempimento del database con dati di prova

#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#

from create_database import utenti, film, genere, persone, sale, genere_film, proiezioni, posti, attori, registi
from sqlalchemy import create_engine
from flask_bcrypt import Bcrypt

#engine = create_engine("postgres+psycopg2://admin:passwordadmin@localhost/progettobd")
#engine = create_engine("postgres+psycopg2://giulio:Giulio99:)@/progettobd")
engine = create_engine("postgres+psycopg2://postgres:simone@localhost/progettobd")


conn = engine.connect()


ins = utenti.insert()
conn.execute(ins, [
     {'nome': 'Simone', 'cognome': 'Ferrari', 'data_nascita': '1999-06-09', 'email': 'simoneferrari@gmail.com', 'password': '$2b$12$fGMFScRQsoWzitWPUcI8guvAfwUQMeg3AzlO.wetVD1toMEuDQWcG', 'is_admin': True, 'is_manager': True, 'saldo': '100.0'},
     {'nome': 'Giulio', 'cognome': 'Trolese', 'data_nascita': '1999-04-20', 'email': 'giuliotrolese@gmail.com', 'password': '$2b$12$fGMFScRQsoWzitWPUcI8guvAfwUQMeg3AzlO.wetVD1toMEuDQWcG', 'is_admin': False, 'is_manager': True, 'saldo': '0.0'},
     {'nome': 'Giulio', 'cognome': 'Casarotti', 'data_nascita': '1998-12-14', 'email': 'giuliocasarotti@gmail.com', 'password': '$2b$12$fGMFScRQsoWzitWPUcI8guvAfwUQMeg3AzlO.wetVD1toMEuDQWcG', 'is_admin': False, 'is_manager': False, 'saldo': '0.0'},

     {'nome': 'Irene', 'cognome': 'Bianchi', 'data_nascita': '1952-01-15', 'email': 'irenebianchi@gmail.com', 'password': '$2b$12$m9JHWemug09LRHexku4ofOxpE4mAOg..2RJrUuYfh7StQ4Tf3zSvW', 'is_admin': False, 'is_manager': False, 'saldo': '15.0'},
     {'nome': 'Alessandro', 'cognome': 'Pagnotto', 'data_nascita': '1982-02-23', 'email': 'alessandropagnotto@gmail.com', 'password': '$2b$12$m9JHWemug09LRHexku4ofOxpE4mAOg..2RJrUuYfh7StQ4Tf3zSvW', 'is_admin': False, 'is_manager': False, 'saldo': '30.0'},
     {'nome': 'Nicola', 'cognome': 'Pugliesi', 'data_nascita': '1998-01-08', 'email': 'nicolapugliesi@gmail.com', 'password': '$2b$12$m9JHWemug09LRHexku4ofOxpE4mAOg..2RJrUuYfh7StQ4Tf3zSvW', 'is_admin': False, 'is_manager': False, 'saldo': '10.0'},

])

ins = film.insert()
conn.execute(ins, [
    {'titolo': 'Titanic', 'durata': 195, 'descrizione': 'Titanic è un film del 1997 co-montato, co-prodotto, scritto e diretto da James Cameron.'},
    {'titolo': 'The Wolf of Wall Street', 'durata': 180, 'descrizione': 'The Wolf of Wall Street è un film del 2013 diretto e prodotto da Martin Scorsese.'},
    {'titolo': 'La Fabbrica di cioccolato', 'durata': 115, 'descrizione': 'La fabbrica di cioccolato (Charlie and the Chocolate Factory) è un film del 2005 diretto da Tim Burton'},
    {'titolo': 'Troy', 'durata': 162, 'descrizione': 'Troy è un film del 2004 diretto da Wolfgang Petersen.'},
    {'titolo': 'Top Gun', 'durata': 110, 'descrizione': 'Top Gun è un film d\'azione del 1986, diretto da Tony Scott '},
    {'titolo': 'Mission: Impossible - Fallout', 'durata': 147, 'descrizione': 'Mission: Impossible - Fallout è un film del 2018 scritto e diretto da Christopher McQuarrie.'},
    {'titolo': 'Skyfall', 'durata': 143, 'descrizione': 'Skyfall è un film del 2012 diretto da Sam Mendes.'},
    {'titolo': 'The imitation game', 'durata': 113, 'descrizione': 'The Imitation Game è un film del 2014 diretto da Morten Tyldum.'},
    {'titolo': 'Dunkirk', 'durata': 106, 'descrizione': 'Dunkirk è un film del 2017 co-prodotto, scritto e diretto da Christopher Nolan.'},
    {'titolo': 'Interstellar', 'durata': 169, 'descrizione': 'Interstellar è un film del 2014 diretto da Christopher Nolan.'},
    {'titolo': 'Film Esempio #1', 'durata': 120, 'descrizione': 'Descrizione del film esempio #1'},
    {'titolo': 'Film Esempio #2', 'durata': 146, 'descrizione': 'Descrizione del film esempio #2'},
    {'titolo': 'Film Esempio #3', 'durata': 113, 'descrizione': 'Descrizione del film esempio #3'},
    {'titolo': 'Film Esempio #4', 'durata': 98, 'descrizione': 'Descrizione del film esempio #4'},
    {'titolo': 'Film Esempio #5', 'durata': 168, 'descrizione': 'Descrizione del film esempio #5'},
])

ins = genere.insert()
conn.execute(ins, [
    {'tipo': 'Animazione'},
    {'tipo': 'Avventura'},
    {'tipo': 'Azione'},
    {'tipo': 'Commedia'},
    {'tipo': 'Drammatico'},
    {'tipo': 'Fantascienza'},
    {'tipo': 'Guerra'},
    {'tipo': 'Horror'},
    {'tipo': 'Musical'},
    {'tipo': 'Spionaggio'},
    {'tipo': 'Storico'},
    {'tipo': 'Thriller'}
])


ins = persone.insert()
conn.execute(ins, [
    {'nome': 'Leonardo', 'cognome': 'Di Caprio'},
    {'nome': 'Jonny', 'cognome': 'Depp'},
    {'nome': 'Brad', 'cognome': 'Pitt'},
    {'nome': 'George', 'cognome': 'Clooney'},
    {'nome': 'Tom', 'cognome': 'Cruise'},
    {'nome': 'Dwayne', 'cognome': 'Johnson'},
    {'nome': 'Tom', 'cognome': 'Hanks'},
    {'nome': 'Badley', 'cognome': 'Cooper'},
    {'nome': 'Jonny', 'cognome': 'Downey JR'},
    {'nome': 'Merly', 'cognome': 'Streep'},
    {'nome': 'Daniel', 'cognome': 'Craig'},
    {'nome': 'Benedict', 'cognome': 'Cumberbatch'},
    {'nome': 'James', 'cognome': 'Cameron'},
    {'nome': 'Martin', 'cognome': 'Scorsese'},
    {'nome': 'Tim', 'cognome': 'Burton'},
    {'nome': 'Wolfgang', 'cognome': 'Patersen'},
    {'nome': 'Tony', 'cognome': 'Scott'},
    {'nome': 'Christopher', 'cognome': 'McQuarrie'},
    {'nome': 'Sam', 'cognome': 'Mendes'},
    {'nome': 'Morten', 'cognome': 'Tyldum'},
    {'nome': 'Fionn', 'cognome': 'Whitehead'},
    {'nome': 'Tom', 'cognome': 'Glynn-Carney'},
    {'nome': 'Jack', 'cognome': 'Lowden'},
    {'nome': 'Matthew', 'cognome': 'McConaughey'},
    {'nome': 'Cristopher', 'cognome': 'Nolan'}
])


ins = sale.insert()
conn.execute(ins, [
    {'n_posti': 150},
    {'n_posti': 150},
    {'n_posti': 150}
])


ins = genere_film.insert()
conn.execute(ins, [
    {'id_film': 1, 'tipo_genere': 'Drammatico'},
    {'id_film': 1, 'tipo_genere': 'Storico'},
    {'id_film': 2, 'tipo_genere': 'Commedia'},
    {'id_film': 2, 'tipo_genere': 'Drammatico'},
    {'id_film': 3, 'tipo_genere': 'Commedia'},
    {'id_film': 3, 'tipo_genere': 'Musical'},
    {'id_film': 4, 'tipo_genere': 'Azione'},
    {'id_film': 4, 'tipo_genere': 'Guerra'},
    {'id_film': 4, 'tipo_genere': 'Storico'},
    {'id_film': 5, 'tipo_genere': 'Azione'},
    {'id_film': 5, 'tipo_genere': 'Guerra'},
    {'id_film': 6, 'tipo_genere': 'Azione'},
    {'id_film': 6, 'tipo_genere': 'Spionaggio'},
    {'id_film': 7, 'tipo_genere': 'Azione'},
    {'id_film': 7, 'tipo_genere': 'Spionaggio'},
    {'id_film': 8, 'tipo_genere': 'Guerra'},
    {'id_film': 8, 'tipo_genere': 'Storico'},
    {'id_film': 9, 'tipo_genere': 'Drammatico'},
    {'id_film': 9, 'tipo_genere': 'Guerra'},
    {'id_film': 9, 'tipo_genere': 'Storico'},
    {'id_film': 10, 'tipo_genere': 'Avventura'},
    {'id_film': 10, 'tipo_genere': 'Drammatico'},
    {'id_film': 10, 'tipo_genere': 'Fantascienza'},
    {'id_film': 11, 'tipo_genere': 'Horror'},
    {'id_film': 12, 'tipo_genere': 'Commedia'},
    {'id_film': 12, 'tipo_genere': 'Drammatico'},
    {'id_film': 13, 'tipo_genere': 'Azione'},
    {'id_film': 13, 'tipo_genere': 'Thriller'},
    {'id_film': 14, 'tipo_genere': 'Fantascienza'},
    {'id_film': 14, 'tipo_genere': 'Guerra'},
    {'id_film': 15, 'tipo_genere': 'Spionaggio'},
    {'id_film': 15, 'tipo_genere': 'Storico'}
])


ins = proiezioni.insert()
conn.execute(ins, [
    {'data': '2020-08-30', 'ora_inizio': '16:00', 'sala': 1, 'film': 1},
    {'data': '2020-08-30', 'ora_inizio': '16:30', 'sala': 2, 'film': 3},
    {'data': '2020-08-30', 'ora_inizio': '21:00', 'sala': 1, 'film': 2},
    {'data': '2020-08-30', 'ora_inizio': '21:30', 'sala': 2, 'film': 5},

    {'data': '2020-08-31', 'ora_inizio': '17:00', 'sala': 1, 'film': 13},
    {'data': '2020-08-31', 'ora_inizio': '19:45', 'sala': 2, 'film': 12},
    {'data': '2020-08-31', 'ora_inizio': '16:00', 'sala': 3, 'film': 5},
    {'data': '2020-08-31', 'ora_inizio': '21:45', 'sala': 1, 'film': 4},

    {'data': '2020-09-01', 'ora_inizio': '16:00', 'sala': 1, 'film': 12},
    {'data': '2020-09-01', 'ora_inizio': '16:00', 'sala': 3, 'film': 11},
    {'data': '2020-09-01', 'ora_inizio': '21:00', 'sala': 1, 'film': 7},
    {'data': '2020-09-01', 'ora_inizio': '19:00', 'sala': 3, 'film': 6},

    {'data': '2020-09-02', 'ora_inizio': '15:25', 'sala': 3, 'film': 14},
    {'data': '2020-09-02', 'ora_inizio': '16:00', 'sala': 2, 'film': 13},
    {'data': '2020-09-02', 'ora_inizio': '22:00', 'sala': 2, 'film': 1},
    {'data': '2020-09-02', 'ora_inizio': '19:45', 'sala': 3, 'film': 11},

    {'data': '2020-09-03', 'ora_inizio': '19:45', 'sala': 3, 'film': 7},
    {'data': '2020-09-03', 'ora_inizio': '15:45', 'sala': 3, 'film': 10},
    {'data': '2020-09-03', 'ora_inizio': '21:45', 'sala': 1, 'film': 4},
    {'data': '2020-09-03', 'ora_inizio': '23:45', 'sala': 2, 'film': 6},

    {'data': '2020-09-04', 'ora_inizio': '19:45', 'sala': 1, 'film': 9},
    {'data': '2020-09-04', 'ora_inizio': '21:20', 'sala': 2, 'film': 3},
    {'data': '2020-09-04', 'ora_inizio': '19:10', 'sala': 3, 'film': 5},
    {'data': '2020-09-04', 'ora_inizio': '22:10', 'sala': 3, 'film': 2},

    {'data': '2020-09-05', 'ora_inizio': '19:00', 'sala': 3, 'film': 3},
    {'data': '2020-09-05', 'ora_inizio': '19:10', 'sala': 2, 'film': 14},
    {'data': '2020-09-05', 'ora_inizio': '15:00', 'sala': 1, 'film': 3},
    {'data': '2020-09-05', 'ora_inizio': '15:10', 'sala': 2, 'film': 14},

    {'data': '2020-09-06', 'ora_inizio': '19:00', 'sala': 2, 'film': 4},
    {'data': '2020-09-06', 'ora_inizio': '14:00', 'sala': 1, 'film': 2},
    {'data': '2020-09-06', 'ora_inizio': '16:20', 'sala': 3, 'film': 1},
    {'data': '2020-09-06', 'ora_inizio': '23:30', 'sala': 3, 'film': 6},

    {'data': '2020-09-07', 'ora_inizio': '19:00', 'sala': 3, 'film': 10},
    {'data': '2020-09-07', 'ora_inizio': '19:45', 'sala': 2, 'film': 8},
    {'data': '2020-09-07', 'ora_inizio': '15:00', 'sala': 1, 'film': 9},
    {'data': '2020-09-07', 'ora_inizio': '19:45', 'sala': 1, 'film': 15},

    {'data': '2020-09-08', 'ora_inizio': '15:30', 'sala': 1, 'film': 15},
    {'data': '2020-09-08', 'ora_inizio': '17:20', 'sala': 2, 'film': 15},
    {'data': '2020-09-08', 'ora_inizio': '19:40', 'sala': 3, 'film': 9},
    {'data': '2020-09-08', 'ora_inizio': '23:45', 'sala': 1, 'film': 9},

    {'data': '2020-09-09', 'ora_inizio': '18:00', 'sala': 1, 'film': 7},
    {'data': '2020-09-09', 'ora_inizio': '19:00', 'sala': 2, 'film': 6},
    {'data': '2020-09-09', 'ora_inizio': '20:00', 'sala': 3, 'film': 3},
    {'data': '2020-09-09', 'ora_inizio': '22:45', 'sala': 1, 'film': 12},

    {'data': '2020-09-10', 'ora_inizio': '15:10', 'sala': 1, 'film': 4},
    {'data': '2020-09-10', 'ora_inizio': '18:00', 'sala': 3, 'film': 6},
    {'data': '2020-09-10', 'ora_inizio': '20:30', 'sala': 1, 'film': 13},
    {'data': '2020-09-10', 'ora_inizio': '16:00', 'sala': 2, 'film': 11},

    {'data': '2020-09-11', 'ora_inizio': '16:00', 'sala': 1, 'film': 10},
    {'data': '2020-09-11', 'ora_inizio': '17:10', 'sala': 2, 'film': 13},
    {'data': '2020-09-11', 'ora_inizio': '18:20', 'sala': 3, 'film': 7},
    {'data': '2020-09-11', 'ora_inizio': '19:30', 'sala': 1, 'film': 1},

    {'data': '2020-09-12', 'ora_inizio': '15:30', 'sala': 1, 'film': 2},
    {'data': '2020-09-12', 'ora_inizio': '15:45', 'sala': 2, 'film': 12},
    {'data': '2020-09-12', 'ora_inizio': '19:30', 'sala': 1, 'film': 15},
    {'data': '2020-09-12', 'ora_inizio': '19:15', 'sala': 3, 'film': 8},

    {'data': '2020-09-13', 'ora_inizio': '17:30', 'sala': 1, 'film': 4},
    {'data': '2020-09-13', 'ora_inizio': '20:15', 'sala': 1, 'film': 3},
    {'data': '2020-09-13', 'ora_inizio': '21:10', 'sala': 1, 'film': 1},
    {'data': '2020-09-13', 'ora_inizio': '23:50', 'sala': 1, 'film': 14},

])


#ins = posti.insert()
#conn.execute(ins, [
#        {'id_posto': 44, 'prezzo': 5, 'prenotato': 'simoneferrari@gmail.com', 'proiezioni': 25},
#        {'id_posto': 45, 'prezzo': 5, 'prenotato': 'simoneferrari@gmail.com', 'proiezioni': 25},
#        {'id_posto': 46, 'prezzo': 5, 'prenotato': 'simoneferrari@gmail.com', 'proiezioni': 25},
#        {'id_posto': 60, 'prezzo': 5, 'prenotato': 'giuliotrolese@gmail.com', 'proiezioni': 25},
#        {'id_posto': 61, 'prezzo': 5, 'prenotato': 'giuliotrolese@gmail.com', 'proiezioni': 25},
#        {'id_posto': 62, 'prezzo': 5, 'prenotato': 'giuliotrolese@gmail.com', 'proiezioni': 25},
#        {'id_posto': 63, 'prezzo': 5, 'prenotato': 'giuliotrolese@gmail.com', 'proiezioni': 25},
#        {'id_posto': 21, 'prezzo': 5, 'prenotato': 'giuliocasarotti@gmail.com', 'proiezioni': 25},
#        {'id_posto': 22, 'prezzo': 5, 'prenotato': 'giuliocasarotti@gmail.com', 'proiezioni': 25},

#])


ins = attori.insert()
conn.execute(ins, [
    {'id_persona': 1, 'id_film': 1},
    {'id_persona': 1, 'id_film': 2},
    {'id_persona': 2, 'id_film': 3},
    {'id_persona': 3, 'id_film': 4},
    {'id_persona': 5, 'id_film': 5},
    {'id_persona': 5, 'id_film': 6},
    {'id_persona': 11, 'id_film': 7},
    {'id_persona': 12, 'id_film': 8},
    {'id_persona': 21, 'id_film': 9},
    {'id_persona': 22, 'id_film': 9},
    {'id_persona': 23, 'id_film': 9},
    {'id_persona': 24, 'id_film': 10},
    {'id_persona': 23, 'id_film': 11},
    {'id_persona': 19, 'id_film': 11},
    {'id_persona': 7, 'id_film': 12},
    {'id_persona': 12, 'id_film': 12},
    {'id_persona': 20, 'id_film': 13},
    {'id_persona': 25, 'id_film': 13},
    {'id_persona': 24, 'id_film': 14},
    {'id_persona': 11, 'id_film': 14},
    {'id_persona': 10, 'id_film': 14},
    {'id_persona': 3, 'id_film': 15},
    {'id_persona': 4, 'id_film': 15},
    {'id_persona': 8, 'id_film': 15},
    {'id_persona': 16, 'id_film': 15}
])


ins = registi.insert()
conn.execute(ins, [
    {'id_persona': 13, 'id_film': 1},
    {'id_persona': 14, 'id_film': 2},
    {'id_persona': 15, 'id_film': 3},
    {'id_persona': 16, 'id_film': 4},
    {'id_persona': 17, 'id_film': 5},
    {'id_persona': 18, 'id_film': 6},
    {'id_persona': 19, 'id_film': 7},
    {'id_persona': 20, 'id_film': 8},
    {'id_persona': 25, 'id_film': 9},
    {'id_persona': 25, 'id_film': 10},
    {'id_persona': 17, 'id_film': 11},
    {'id_persona': 21, 'id_film': 12},
    {'id_persona': 20, 'id_film': 13},
    {'id_persona': 7, 'id_film': 13},
    {'id_persona': 24, 'id_film': 14},
    {'id_persona': 12, 'id_film': 14},
    {'id_persona': 18, 'id_film': 14},
    {'id_persona': 1, 'id_film': 15},
    {'id_persona': 3, 'id_film': 15},
    {'id_persona': 13, 'id_film': 15}
])
