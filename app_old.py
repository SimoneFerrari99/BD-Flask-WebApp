# Progetto basi di dati 2020 - Tema Cinema
# Gruppo: ArceCity
# Membri: Casarotti Giulio, Ferrari Simone, Trolese Gulio

# File: app.py
# Descrizione: applicazione principale
#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
# Moduli importati
from flask import Flask, render_template, url_for, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.sql import func
from classes import province
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
import json
from PIL import Image


#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
# Configurazione APP

app = Flask(__name__)
bcrypt = Bcrypt(app)  # inizializzo il bycript della app

app.secret_key = b'f^iz\x05~\x1b\xaat\xf7\x00\xb4Lf7\xa0'
login_manager = LoginManager()
login_manager.init_app(app)

# apriamo l'engine creato in precedenza in fase di creazione del database (file create_database.py)
# engine = create_engine("postgres+psycopg2://postgres:ciao@serversrv.ddns.net:2345/progetto2020")
engine = create_engine("postgres+psycopg2://giulio:Giulio99:)@/progettobd")
# engine = create_engine(
# "postgres+psycopg2://postgres:simone@localhost/progettoBD2020")

# prendiamo i metadata dell'engine
meta = MetaData(engine)
meta.reflect()

#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
# Funioni utili


def generate_persone_dict():  # generatore di un dizionario per le persone
    persone = meta.tables['persone']
    s = select([persone])
    conn = engine.connect()
    result = conn.execute(s)
    dict_persone = dict()
    for row in result:
        dict_persone[row['id_persona']] = str(
            row['nome'])+' '+str(row['cognome'])
    return dict_persone


def generate_film_dict():  # generatore di un dizionario per i film
    film = meta.tables['film']
    s = select([film])
    conn = engine.connect()
    result = conn.execute(s)
    dict_film = dict()
    for row in result:
        dict_film[row['id_film']] = [
            row['titolo'], row['durata'], row['descrizione']]
    return dict_film


def generate_generi_dict():  # generatore di un dizionario per i generi
    genere = meta.tables['genere']
    s = select([genere])
    conn = engine.connect()
    result = conn.execute(s)
    dict_generi = dict()
    for row in result:
        dict_generi[row['tipo']] = [
            row['tipo']]
    return dict_generi


def generate_sale_list():  # generatore di un dizionario per le sale
    sale = meta.tables['sale']
    s = select([sale])
    conn = engine.connect()
    result = conn.execute(s)
    list_sale = []
    for row in result:
        list_sale.append(row['n_sala'])
    return list_sale


#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
# Route principale: Home

@app.route('/')
def home():
    dict = generate_film_dict()
    return render_template('home.html', film_dict=dict)

#--------------------------------------------------------------------------------------------#
# Login


class Utente(UserMixin):
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def get_id(self):
        return self.email


@login_manager.user_loader
def load_user(user_email):
    clienti = meta.tables['clienti']
    s = select([clienti]).where(
        clienti.c.email == user_email
    )
    conn = engine.connect()
    result = conn.execute(s)
    if result.rowcount == 0:
        return None
    user = result.fetchone()
    conn.close()
    return Utente(user.email, user.password)


@login_manager.unauthorized_handler
def unauthorized():
    flash('Per accedere a questa pagina è necessario accedere')
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login/inserimento_dati', methods=['GET', 'POST'])
def login_inserimento_dati():
    email_form = request.form["email"]
    password = request.form["psw"]
    # clienti = meta.tables['clienti']
    # s = select([clienti.password]).\
    #    where(
    #        email == email_form
    #    )
    # conn = engine.connect()
    # result = conn.execute(s)
    # real_password = result.fetchone()['password']
    # conn.close()
    utente = load_user(email_form)
    if bcrypt.check_password_hash(utente.password, password) == True:
        user = load_user(email_form)
        login_user(user)
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

#--------------------------------------------------------------------------------------------#
# Logout


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

#--------------------------------------------------------------------------------------------#
# Registrazione di un nuovo utente


@app.route('/registrazione')
def registrazione():
    return render_template('registrazione.html', errore=False)


@app.route('/registrazione/inserimento_utente', methods=['GET', 'POST'])
def sign_up():
    # prendiamo i dati dal form
    nome = request.form["nome"]
    cognome = request.form["cognome"]
    data_nascita = str(request.form["data_nascita"])
    email = request.form["email"]
    psw = request.form["psw"]
    conferma = request.form["conferma_password"]

    hashed_psw = bcrypt.generate_password_hash(
        psw).decode('utf-8')  # cripto la password

    # se le due password non corrispondono
    if(psw != conferma):
        return render_template('registrazione.html', errore=True)
    else:
        # prendiamo la tabella clienti dal metadata tramite reflection
        clienti = meta.tables['clienti']  # prendo la tabella
        ins = clienti.insert()  # prendo la insert
        values = {  # dizionario per i valori
            'nome': nome,
            'cognome': cognome,
            'data_nascita': data_nascita,
            'email': email,
            'password': hashed_psw,
            'saldo': 0.0
        }
        conn = engine.connect()  # mi connetto
        conn.execute(ins, values)  # eseguo l'inserimento con i valori
        return redirect(url_for('login'))  # return

#--------------------------------------------------------------------------------------------#
# Inseriemnto di una persona


@app.route('/aggiungi_persona')
@login_required
def aggiungi_persona():
    return render_template('aggiungi_persona.html')


@app.route('/aggiungi_persona/inserimento_persona', methods=['GET', 'POST'])
@login_required
def inserimento_persona():
    # prendiamo i dati dal form
    nome = request.form["nome"]
    cognome = request.form["cognome"]

    persone = meta.tables['persone']  # prendo la tabella
    ins = persone.insert()  # prendo la insert
    values = {  # dizionario per i valori
        'nome': nome,
        'cognome': cognome,
    }
    conn = engine.connect()  # mi connetto
    conn.execute(ins, values)  # eseguo l'inserimento con i valori
    if request.form["Submit"] == "Film":
        return redirect(url_for('aggiungi_film'))  # return
    else:
        return redirect(url_for('aggiungi_persona'))

#--------------------------------------------------------------------------------------------#
# Inserimento di un film


@app.route('/aggiungi_film')
@login_required
def aggiungi_film():
    dict_p = generate_persone_dict()
    dict_g = generate_generi_dict()
    return render_template('aggiungi_film.html', persone_dict=json.dumps(dict_p), generi_dict=json.dumps(dict_g))


@app.route('/aggiungi_film/inserimento_film', methods=['GET', 'POST'])
@login_required
def inserimento_film():
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
    with engine.connect().execution_options(isolation_level="SERIALIZABLE") as conn:
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

    conn = engine.connect()
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

# TODO:
#       fare una route "aggiungi_admin"

#--------------------------------------------------------------------------------------------#
# Inseriemnto di una sala


@app.route('/riepilogo_sale')
@login_required
def riepilogo_sale():
    return render_template('riepilogo_sale.html', sale=generate_sale_list())


@app.route('/riepilogo_sale/inserimento_sala', methods=['GET', 'POST'])
@login_required
def inserimento_sala():
    n_posti = 150  # per semplicità, tutte le nostre sale hanno 150 posti

    sale = meta.tables['sale']  # prendo la tabella
    ins = sale.insert()  # prendo la insert
    values = {  # dizionario per i valori
        'n_posti': n_posti,
    }
    conn = engine.connect()  # mi connetto
    conn.execute(ins, values)  # eseguo l'inserimento con i valori
    return redirect(url_for('riepilogo_sale'))  # return

#--------------------------------------------------------------------------------------------#
# Inseriemnto di una proiezione


@app.route('/aggiungi_proiezione')
@login_required
def aggiungi_proiezioni():
    return render_template('aggiungi_proiezione.html', film_dict=generate_film_dict(), sale=json.dumps(generate_sale_list()))


@app.route('/aggiungi_proiezione/inserimento_proiezione', methods=['GET', 'POST'])
@login_required
def inserimento_proiezione():
    film = request.form["film"]
    proiezioni = meta.tables['proiezioni']
    ins = proiezioni.insert()
    conn = engine.connect()
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

    return redirect(url_for('aggiungi_proiezioni'))

#--------------------------------------------------------------------------------------------#
# Inserimento di un genere


@app.route('/aggiungi_genere')
@login_required
def aggiungi_genere():
    return render_template('aggiungi_genere.html')


@app.route('/aggiungi_genere/inserimento_genere', methods=['GET', 'POST'])
@login_required
def inserimento_genere():
    # prendiamo i dati dal form
    tipo = request.form["tipo"]

    genere = meta.tables['genere']  # prendo la tabella
    ins = genere.insert()  # prendo la insert
    values = {  # dizionario per i valori
        'tipo': tipo
    }
    conn = engine.connect()  # mi connetto
    conn.execute(ins, values)  # eseguo l'inserimento con i valori
    return redirect(url_for('aggiungi_film'))  # return

#--------------------------------------------------------------------------------------------#

# @app.ruote('/visualizza_saldo')
# def visualizza_saldo():
    # clienti = request.tables['clienti']
    # s = select([clienti.c.email, clienti.c.saldo]).where( clienti.c.email == ipotetica email)

    # conn = engine.connect()
    # result = conn.execute(s)

    # patrimonio = result.fetchone()
    # return render template('visualizza_saldo.html', saldo = patrimonio)

# @app.route('/visualizza saldo/aggiungi_saldo', methods=['GET', 'POST'])
# def aggiungi_saldo():
#    taglio = request.form["taglio"]

#    saldo = meta.tables['saldo']
#    ins = genere.insert();
#    values = {
#        'taglio' : taglio
#    }

#    conn = engine.connect()
#    conn.execute(ins,values)
#    return redirect(url_for('visualizza_saldo'))

#--------------------------------------------------------------------------------------------#
