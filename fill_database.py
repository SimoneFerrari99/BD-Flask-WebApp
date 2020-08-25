from create_database import utenti, film, genere, persone, sale, genere_film, proiezioni, posti, attori, registi
from sqlalchemy import create_engine
from flask_bcrypt import Bcrypt

engine = create_engine("postgres+psycopg2://postgres:simone@localhost/progettobd")

conn = engine.connect()


#ins = utenti.insert()
#conn.execute(ins, [
#     {'nome': 'Simone', 'cognome': 'Ferrari', 'email': 'simone@gmail.com', 'password': '12345', 'saldo': '0.0'},
#
#])

ins = film.insert()
conn.execute(ins, [
         {'titolo': 'Titanic', 'durata': 195, 'descrizione': 'Titanic è un film del 1997 co-montato, co-prodotto, scritto e diretto da James Cameron.'},
         {'titolo': 'The Wolf of Wall Street', 'durata': 180, 'descrizione': 'The Wolf of Wall Street è un film del 2013 diretto e prodotto da Martin Scorsese.'},
         {'titolo': 'La Fabbrica di cioccolato', 'durata': 115, 'descrizione': 'La fabbrica di cioccolato (Charlie and the Chocolate Factory) è un film del 2005 diretto da Tim Burton'},
         {'titolo': 'Troy', 'durata': 162, 'descrizione': 'Troy è un film del 2004 diretto da Wolfgang Petersen.'},
         {'titolo': 'Top Gun', 'durata': 110, 'descrizione': 'Top Gun è un film d\'azione del 1986, diretto da Tony Scott '},
         {'titolo': 'Mission: Impossible - Fallout', 'durata': 147, 'descrizione': 'Mission: Impossible - Fallout è un film del 2018 scritto e diretto da Christopher McQuarrie.'},
         {'titolo': 'Skyfall', 'durata': 143, 'descrizione': 'Skyfall è un film del 2012 diretto da Sam Mendes.'},
         {'titolo': 'The imitation game', 'durata': 113, 'descrizione': 'The Imitation Game è un film del 2014 diretto da Morten Tyldum.'}
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
         {'id_film': 8, 'tipo_genere': 'Storico'}
])


ins = proiezioni.insert()
conn.execute(ins, [
         {'data': '2020-08-01', 'ora_inizio': '16:00', 'sala': 1, 'film': 1},
         {'data': '2020-08-01', 'ora_inizio': '16:30', 'sala': 2, 'film': 2},
         {'data': '2020-08-02', 'ora_inizio': '19:00', 'sala': 1, 'film': 3},
         {'data': '2020-08-02', 'ora_inizio': '19:00', 'sala': 2, 'film': 4},
         {'data': '2020-08-03', 'ora_inizio': '16:00', 'sala': 1, 'film': 1},
         {'data': '2020-08-03', 'ora_inizio': '17:00', 'sala': 2, 'film': 5},
         {'data': '2020-08-03', 'ora_inizio': '17:30', 'sala': 3, 'film': 6},
         {'data': '2020-08-04', 'ora_inizio': '21:00', 'sala': 1, 'film': 1},
         {'data': '2020-08-04', 'ora_inizio': '21:00', 'sala': 2, 'film': 8},
         {'data': '2020-08-05', 'ora_inizio': '16:00', 'sala': 1, 'film': 7},
         {'data': '2020-08-05', 'ora_inizio': '17:00', 'sala': 2, 'film': 5},
         {'data': '2020-08-05', 'ora_inizio': '19:00', 'sala': 3, 'film': 4},
         {'data': '2020-08-06', 'ora_inizio': '22:00', 'sala': 1, 'film': 2},
         {'data': '2020-08-07', 'ora_inizio': '18:00', 'sala': 1, 'film': 3},
         {'data': '2020-08-07', 'ora_inizio': '22:00', 'sala': 1, 'film': 3},
         {'data': '2020-08-07', 'ora_inizio': '16:00', 'sala': 2, 'film': 8},
         {'data': '2020-08-07', 'ora_inizio': '21:00', 'sala': 2, 'film': 8},
])


#ins = posti.insert()
#conn.execute(ins, [
#         {'id_posto': 1, 'prezzo': , 'prenotato': '', 'proiezioni': },
#
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
         {'id_persona': 12, 'id_film': 8}

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
         {'id_persona': 20, 'id_film': 8}
])
