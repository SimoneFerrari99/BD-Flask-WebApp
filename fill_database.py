from create_database import clienti, film, persone, sale, proiezioni, posti, attori, registi
from sqlalchemy import create_engine

engine = create_engine("postgres+psycopg2://giulio:Giulio99:)@/progettobd")

conn = engine.connect()


#ins = clienti.insert()
#conn.execute(ins, [
#     {'nome': 'Simone', 'cognome': 'Ferrari', 'sesso': 'M', 'data_nascita': '09/06/1999', 'provincia': 'VE', 'comune': 'Venezia', 'cap': '30121', 'email': 'simone@gmail.com', 'password': '12345', 'saldo': '0.0'},

#])


ins = film.insert()
conn.execute(ins, [
         {'id_film': 1, 'titolo': 'Titanic', 'durata': 120, 'descrizione': 'Nave che affonda'},
         {'id_film': 2, 'titolo': 'B', 'durata': 120, 'descrizione': 'Nave che affonda'},
         {'id_film': 3, 'titolo': 'C', 'durata': 120, 'descrizione': 'Nave che affonda'},
         {'id_film': 4, 'titolo': 'D', 'durata': 120, 'descrizione': 'Nave che affonda'},
         {'id_film': 5, 'titolo': 'E', 'durata': 120, 'descrizione': 'Nave che affonda'},
         {'id_film': 6, 'titolo': 'F', 'durata': 120, 'descrizione': 'Nave che affonda'},
         {'id_film': 7, 'titolo': 'G', 'durata': 120, 'descrizione': 'Nave che affonda'},
])


ins = persone.insert()
conn.execute(ins, [
])


ins = sale.insert()
conn.execute(ins, [
])


ins = proiezioni.insert()
conn.execute(ins, [
])


ins = attori.insert()
conn.execute(ins, [
])

ins = registi.insert()
conn.execute(ins, [
])
