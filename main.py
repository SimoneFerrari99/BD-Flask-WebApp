# Progetto basi di dati 2020 - Tema Cinema
# Gruppo: ArceCity
# Membri: Casarotti Giulio, Ferrari Simone, Trolese Gulio

# File: app.py
# Descrizione: applicazione principale
#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
# Moduli importati
from flask import Flask, render_template, url_for, redirect, request, session, flash, abort
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.sql import func
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import json
from PIL import Image

from user_route import user_app
from admin_route import admin_app

#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
# Configurazione APP

app = Flask(__name__)
app.register_blueprint(user_app)
app.register_blueprint(admin_app)
bcrypt = Bcrypt(app)  # inizializzo il bycript della app

#settiamo la secret_key per flask login... settata come consigliato nella documentazione di flask_login
#Configuriamo flask login
app.secret_key = b'f^iz\x05~\x1b\xaat\xf7\x00\xb4Lf7\xa0'
login_manager = LoginManager()
login_manager.init_app(app)

# apriamo l'engine creato in precedenza in fase di creazione del database (file create_database.py)
# engine = create_engine("postgres+psycopg2://postgres:ciao@serversrv.ddns.net:2345/progetto2020")
anonim_engine = create_engine("postgres+psycopg2://anonim:passwordanonim@localhost/progettobd")
clienti_engine = create_engine("postgres+psycopg2://cliente:passwordcliente@localhost/progettobd")
admin_engine = create_engine("postgres+psycopg2://admin:passwordadmin@localhost/progettobd")
#engine = create_engine("postgres+psycopg2://postgres:simone@localhost/progettobd")

# prendiamo i metadata dell'engine
meta = MetaData(admin_engine)
meta.reflect()

#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
# Funioni utili


def generate_persone_dict():  # generatore di un dizionario per le persone
    persone = meta.tables['persone']
    s = select([persone])
    conn = anonim_engine.connect()
    result = conn.execute(s)
    dict_persone = dict()
    for row in result:
        dict_persone[row['id_persona']] = str(row['nome'])+' '+str(row['cognome'])
    conn.close()
    return dict_persone


def generate_film_dict():  # generatore di un dizionario per i film
    film = meta.tables['film']
    s = select([film])
    conn = anonim_engine.connect()
    result = conn.execute(s)
    dict_film = dict()
    for row in result:
        dict_film[row['id_film']] = [
            row['titolo'], row['durata'], row['descrizione']]
    conn.close()
    return dict_film


def generate_generi_dict():  # generatore di un dizionario per i generi
    genere = meta.tables['genere']
    s = select([genere])
    conn = anonim_engine.connect()
    result = conn.execute(s)
    dict_generi = dict()
    for row in result:
        dict_generi[row['tipo']] = [
            row['tipo']]
    conn.close()
    return dict_generi


def generate_sale_list():  # generatore di un dizionario per le sale
    sale = meta.tables['sale']
    s = select([sale])
    conn = anonim_engine.connect()
    result = conn.execute(s)
    list_sale = []
    for row in result:
        list_sale.append(row['n_sala'])
    conn.close()
    return list_sale


#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
# Route principale: Home

@app.route('/')
def home():
    dict = generate_film_dict()
    if(current_user.is_anonymous == False and current_user.is_admin == True):
        admin = True
    else:
        admin = False
    return render_template('home.html', film_dict=dict, is_admin = admin)

#--------------------------------------------------------------------------------------------#
# Login

#classe che rappresenta un nostro utente
class Utente(UserMixin):
    def __init__(self, email, password, is_admin): #costruttore
        self.email = email
        self.password = password
        self.is_admin = is_admin
        #if is_admin == True:
        #    self.engine = admin_engine
        #else:
        #    self.engine = clienti_engine

    def get_id(self): #metodo che restituisce l'id (in questo caso, la email)
        return self.email


@login_manager.user_loader
def load_user(user_email): #funzione che restituisce l'utente associato alla user_email
    utenti = meta.tables['utenti']
    s = select([utenti]).where(
        utenti.c.email == user_email
    )
    conn = anonim_engine.connect()
    result = conn.execute(s)
    if result.rowcount == 0: #se non è presente l'utente cercato
        return None
    user = result.fetchone()
    conn.close()
    return Utente(user.email, user.password, user.is_admin) #ritorna un Utente


@login_manager.unauthorized_handler #Quando il login è richiesto, e non sei loggato, vieni rimandato al login
def unauthorized():
    return redirect(url_for('login')) #TODO: dare un messaggio di errore


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': #gestione del form
        #prendiamo i dati dal form
        email_form = request.form["email"]
        password = request.form["psw"]
        #carichiamo l'utente
        utente = load_user(email_form)
        if bcrypt.check_password_hash(utente.password, password) == True and utente != None: #se la password salvata nel database e quella inserita nel form coincidono
            login_user(utente) #loggo l'utente
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    else:
        return render_template('login.html')
#--------------------------------------------------------------------------------------------#
# Logout


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

#--------------------------------------------------------------------------------------------#
# Registrazione di un nuovo utente


@app.route('/registrazione', methods=['GET', 'POST'])
def registrazione():
    if request.method == 'POST':
        # prendiamo i dati dal form
        nome = request.form["nome"]
        cognome = request.form["cognome"]
        data_nascita = str(request.form["data_nascita"])
        email = request.form["email"]
        psw = request.form["psw"]
        conferma = request.form["conferma_password"]

        hashed_psw = bcrypt.generate_password_hash(psw).decode('utf-8')  # cripto la password

        # se le due password non corrispondono
        if(psw != conferma):
            return render_template('registrazione.html', errore=True)
        else:
            # prendiamo la tabella utenti dal metadata tramite reflection
            utenti = meta.tables['utenti']  # prendo la tabella
            ins = utenti.insert()  # prendo la insert
            values = {  # dizionario per i valori
                'nome': nome,
                'cognome': cognome,
                'data_nascita': data_nascita,
                'email': email,
                'password': hashed_psw,
                'is_admin': False,
                'saldo': 0.0
            }
            conn = anonim_engine.connect()  # mi connetto
            conn.execute(ins, values)  # eseguo l'inserimento con i valori
            conn.close()
            return redirect(url_for('login'))  # return
    else:
        return render_template('registrazione.html', errore=False)

#--------------------------------------------------------------------------------------------#
# Inseriemnto di una persona


@app.route('/aggiungi_persona', methods=['GET', 'POST'])
@login_required
def aggiungi_persona():
    if(current_user.is_admin == True):
        if request.method == 'POST':
            # prendiamo i dati dal form
            nome = request.form["nome"]
            cognome = request.form["cognome"]

            persone = meta.tables['persone']  # prendo la tabella
            ins = persone.insert()  # prendo la insert
            values = {  # dizionario per i valori
                'nome': nome,
                'cognome': cognome,
            }
            conn = admin_engine.connect()  # mi connetto
            conn.execute(ins, values)  # eseguo l'inserimento con i valori
            conn.close()
            if request.form["Submit"] == "Film": #abbiamo due diversi bottoni di sumbit
                return redirect(url_for('aggiungi_film'))  # return
            else:
                return redirect(url_for('aggiungi_persona'))
        else:
            return render_template('aggiungi_persona.html')
    else:
        return redirect(url_for('login')) # TODO: inserire messaggio di errore

#--------------------------------------------------------------------------------------------#
# Inserimento di un film

@app.route('/aggiungi_film', methods=['GET', 'POST'])
@login_required
def aggiungi_film():
    if(current_user.is_admin == True):
        if request.method == 'POST':
            # prendiamo i dati dal form
            titolo = request.form["titolo"]
            durata = request.form["durata"]
            descrizione = request.form["descrizione"]

            film = meta.tables["film"]  # prendo la tabella
            ins = film.insert()  # prendo la insert
            values = {  # dizionario per i valori
                'titolo': titolo,
                'durata': durata,
                'descrizione': descrizione
            }

            id_film = 0

            # transazione per prendere l'id dell'ultimo film inserito (Ovvero quello che stiamo per inserire)
            # Questa transazione serve perchè, una voltas inserito il film, abbiamo bisogno
            # di prenderci il suo id... ma dobbiamo essere sicuri che nel mentre nessuno
            # aggiunga altri film: l'id preso risulterebbe quindi sbagliato.
            # Questo id poi ci serve per collegarlo agli attori e ai registi che recitano/dirigono il film inserito
            with admin_engine.connect().execution_options(isolation_level="SERIALIZABLE") as conn:
                trans = conn.begin()
                try:
                    conn.execute(ins, values)
                    sel = select([func.max(film.c.id_film).label('latest_film')])
                    result = conn.execute(sel)
                    id_film = result.fetchone()['latest_film']
                    trans.commit()
                except:
                    trans.rollback()
                finally:
                    conn.close()

            copertina = request.files["copertina"]

            copertina.save("./static/copertine/" + str(id_film) + ".jpg")

            conn = admin_engine.connect()
            # prendo le tre tabelle
            attori = meta.tables["attori"]
            registi = meta.tables["registi"]
            genere_film = meta.tables["genere_film"]


            # per ogni elemento del form (non so quanti siano di preciso...)
            for elem in request.form:
                # se è un attore
                if "attori" in str(elem):
                    id_attore = request.form[str(elem)]
                    ins_attori = attori.insert()
                    attori_values = {
                        "id_film": id_film,
                        "id_persona": id_attore
                    }

                    # aggiungo i dati alla tabella attori
                    conn.execute(ins_attori, attori_values)
                # se è un regista
                elif "registi" in str(elem):
                    id_regista = request.form[str(elem)]
                    ins_regista = registi.insert()
                    regista_values = {
                        "id_film": id_film,
                        "id_persona": id_regista
                    }
                    # aggiungo i dati alla tabella registi
                    conn.execute(ins_regista, regista_values)
                # se è un genere
                elif "generi" in str(elem):
                    tipo_genere = request.form[str(elem)]
                    ins_genere = genere_film.insert()
                    genere_values = {
                        "id_film": id_film,
                        "tipo_genere": tipo_genere
                    }
                    # aggiungo i dati alla tabella generi
                    conn.execute(ins_genere, genere_values)
                # TODO: togliere possibilità di selezione multipla da attori e registi
            conn.close()
            return redirect(url_for('aggiungi_film'))
        else:
            dict_p = generate_persone_dict()
            dict_g = generate_generi_dict()
            return render_template('aggiungi_film.html', persone_dict=json.dumps(dict_p), generi_dict=json.dumps(dict_g))
    else:
        return redirect(url_for('login')) # TODO: inserire messaggio di errore

#--------------------------------------------------------------------------------------------#
# Inseriemnto di un amministratore (da parte di un amministratore)

@app.route('/aggiungi_admin', methods=['GET', 'POST'])
@login_required
def aggiungi_admin():
    if(current_user.is_admin == True):
        if request.method == 'POST':

            # prendiamo i dati dal form
            nome = request.form["nome"]
            cognome = request.form["cognome"]
            data_nascita = str(request.form["data_nascita"])
            email = request.form["email"]
            psw = request.form["psw"]
            conferma = request.form["conferma_password"]

            hashed_psw = bcrypt.generate_password_hash(psw).decode('utf-8')  # cripto la password

            # se le due password non corrispondono
            if(psw != conferma):
                return render_template('aggiungi_admin.html', errore=True)
            else:
                # prendiamo la tabella utenti dal metadata tramite reflection
                utenti = meta.tables['utenti']  # prendo la tabella
                ins = utenti.insert()  # prendo la insert
                values = {  # dizionario per i valori
                    'nome': nome,
                    'cognome': cognome,
                    'data_nascita': data_nascita,
                    'email': email,
                    'password': hashed_psw,
                    'is_admin': True,
                    'saldo': 0.0
                }
                conn = admin_engine.connect()  # mi connetto
                conn.execute(ins, values)  # eseguo l'inserimento con i valori
                conn.close()
                return redirect(url_for('login'))  # return
        else:
            return render_template('aggiungi_admin.html', errore=False)
    else:
        return redirect(url_for('login')) # TODO: inserire messaggio di errore

#--------------------------------------------------------------------------------------------#
# Inseriemnto di una sala


@app.route('/riepilogo_sale', methods=['GET', 'POST'])
@login_required
def riepilogo_sale():
    if(current_user.is_admin == True):
        if request.method == 'POST':
            n_posti = 150  # per semplicità, tutte le nostre sale hanno 150 posti

            sale = meta.tables['sale']  # prendo la tabella
            ins = sale.insert()  # prendo la insert
            values = {  # dizionario per i valori
                'n_posti': n_posti,
            }
            conn = admin_engine.connect()  # mi connetto
            conn.execute(ins, values)  # eseguo l'inserimento con i valori
            conn.close()
            return redirect(url_for('riepilogo_sale'))  # return
        else:
            return render_template('riepilogo_sale.html', sale=generate_sale_list())
    else:
        return redirect(url_for('login')) # TODO: inserire messaggio di errore
#--------------------------------------------------------------------------------------------#
# Inseriemnto di una proiezione


@app.route('/aggiungi_proiezione', methods=['GET', 'POST'])
@login_required
def aggiungi_proiezione():
    if(current_user.is_admin == True):
        if request.method == 'POST':
            film = request.form["film"]
            proiezioni = meta.tables['proiezioni']
            ins = proiezioni.insert()
            conn = admin_engine.connect()
            row = dict()
            i = 0
            for elem in request.form:
                if "data" in str(elem):
                    row["data"] = request.form[str(elem)]
                    i += 1
                elif "ora" in str(elem):
                    row["ora_inizio"] = request.form[str(elem)]
                    i += 1
                elif "sala" in str(elem):
                    row["sala"] = request.form[str(elem)]
                    i += 1
                row["film"] = film
                if i == 3:
                    i = 0
                    conn.execute(ins, row)
            conn.close()
            return redirect(url_for('aggiungi_proiezione'))
        else:
            return render_template('aggiungi_proiezione.html', film_dict=generate_film_dict(), sale=json.dumps(generate_sale_list()))
    else:
        return redirect(url_for('login')) # TODO: inserire messaggio di errore
#--------------------------------------------------------------------------------------------#
# Inserimento di un genere


@app.route('/aggiungi_genere', methods=['GET', 'POST'])
@login_required
def aggiungi_genere():
    if(current_user.is_admin == True):
        if request.method == 'POST':
            # prendiamo i dati dal form
            tipo = request.form["tipo"]

            genere = meta.tables['genere']  # prendo la tabella
            ins = genere.insert()  # prendo la insert
            values = {  # dizionario per i valori
                'tipo': tipo
            }
            conn = admin_engine.connect()  # mi connetto
            conn.execute(ins, values)  # eseguo l'inserimento con i valori
            conn.close()
            return redirect(url_for('aggiungi_film'))  # return
        else:
            return render_template('aggiungi_genere.html')
    else:
        return redirect(url_for('login')) # TODO: inserire messaggio di errore

#--------------------------------------------------------------------------------------------#
# HOME PER LA GESTIONE DATABASE


@app.route('/home_gestione_database')
@login_required
def home_gestione_database():
    if(current_user.is_admin == True):
        return render_template('home_gestione_database.html')
    else:
        return redirect(url_for('login'))


#--------------------------------------------------------------------------------------------#

@app.route('/aggiungi_visualizza_saldo', methods=['GET', 'POST'])
@login_required
def aggiungi_visualizza_saldo():
     if request.method == "POST":

         taglio = request.form["taglio"]
         saldo = meta.tables['saldo']
         ins = genere.insert();
         values = {
             'taglio' : taglio
         }

         conn = clienti_engine.connect()
         conn.execute(ins,values)
         conn.close()
         return redirect(url_for('aggiungi_visualizza_saldo'))
     else:
         utenti = request.tables['utenti']
         s = select([utenti.c.email, utenti.c.saldo]).where(utenti.c.email == current_user.email)

         conn = clienti_engine.connect()
         conn.execute(s)
         patrimonio = result.fetchone()
         conn.close()
         return render_template('dashboard_account.html', saldo = patrimonio)

#--------------------------------------------------------------------------------------------#

#@app.route('modifica_sicurezza', methods=['GET', 'POST'])
#@login_required
#def sicurezza():
#    if request.method == "POST":
#
#        nome = meta.tables['utenti']
#        email = meta.tables['utenti']
#        #MANCA
#
#    else:

if __name__ == "__main__":
    app.run()
