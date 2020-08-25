# Progetto basi di dati 2020 - Tema Cinema
# Gruppo: ArceCity
# Membri: Casarotti Giulio, Ferrari Simone, Trolese Gulio

# File: app.py
# Descrizione: File contenente tutte le route accessibili da un amministratore
#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
# Moduli importati
from flask import Flask, render_template, url_for, redirect, request, session, flash, abort
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.sql import func
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import json
from PIL import Image

#from user_route import user_app
#from admin_route import admin_app


#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
# Configurazione APP

app = Flask(__name__)
#app.register_blueprint(user_app)
#app.register_blueprint(admin_app)
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

#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#

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

def generate_proiezioni_valide_dict():
    return None

def errore_admin():
    return redirect(url_for('login', errore = True, messaggio="Attenzione, solo gli amministratori sono autorizzati ad accedere a questa pagina."))


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
    return redirect(url_for('login', errore = True, messaggio="Attenzione, non sei autorizzato ad accedere a questa pagina. Accedi con le giuste credenziali")) #TODO: dare un messaggio di errore


@app.route('/login/<errore>/<messaggio>', methods=['GET', 'POST'])
def login(errore, messaggio):
    if request.method == 'POST': #gestione del form
        #prendiamo i dati dal form
        email_form = request.form["email"]
        password = request.form["psw"]
        #carichiamo l'utente
        utente = load_user(email_form)
        if utente != None and bcrypt.check_password_hash(utente.password, password) == True: #se la password salvata nel database e quella inserita nel form coincidono
            login_user(utente) #loggo l'utente
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login', errore = True, messaggio="Attenzione, mail o password errate."))
    else:
        return render_template('login.html', error = errore, error_message = messaggio)
#--------------------------------------------------------------------------------------------#
# Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#

#--------------------------------------------------------------------------------------------#
# HOME PER LA GESTIONE DATABASE
@app.route('/home_gestione_sito')
@login_required
def home_gestione_sito():
    if(current_user.is_admin == True):
        return render_template('AdminTemplate/home_gestione_sito.html')
    else:
        return errore_admin()


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
            return render_template('AdminTemplate/aggiungi_persona.html')
    else:
        return errore_admin()
#--------------------------------------------------------------------------------------------#
# Inserimento di un film
@app.route('/aggiungi_film', methods=['GET', 'POST'])
@login_required
def aggiungi_film():
    if(current_user.is_admin == True):
        dict_p = generate_persone_dict()
        dict_g = generate_generi_dict()
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


            list_attori = []
            list_registi = []
            list_generi = []

            for elem in request.form:
                # se è un attore
                if "attori" in str(elem):
                    id_attore = request.form[str(elem)]
                    if id_attore in list_attori:
                        return render_template('aggiungi_film.html',  errore = True, error_message="Attenzione, hai scelto lo stesso attore più di una volta.", persone_dict=json.dumps(dict_p), generi_dict=json.dumps(dict_g))
                    list_attori.append(id_attore)
                # se è un regista
                elif "registi" in str(elem):
                    id_regista = request.form[str(elem)]
                    if id_regista in list_registi:
                        return render_template('AdminTemplate/aggiungi_film.html',  errore = True, error_message="Attenzione, hai scelto lo stesso regista più di una volta.", persone_dict=json.dumps(dict_p), generi_dict=json.dumps(dict_g))
                    list_registi.append(id_regista)
                # se è un genere
                elif "generi" in str(elem):
                    tipo_genere = request.form[str(elem)]
                    if tipo_genere in list_generi:
                        return render_template('AdminTemplate/aggiungi_film.html', errore = True, error_message="Attenzione, hai scelto lo stesso genere più di una volta.", persone_dict=json.dumps(dict_p), generi_dict=json.dumps(dict_g))
                    list_generi.append(tipo_genere)

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
            conn.close()
            return redirect(url_for('aggiungi_film'))
        else:
            return render_template('AdminTemplate/aggiungi_film.html', errore = False, error_message="", persone_dict=json.dumps(dict_p), generi_dict=json.dumps(dict_g))
    else:
        return errore_admin()
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

            utenti = meta.tables['utenti']
            s = select([utenti]).where(
                utenti.c.email == email
            )
            conn = anonim_engine.connect()
            result = conn.execute(s)
            conn.close()

            if result.rowcount > 0:
                return render_template('AdminTemplate/aggiungi_admin.html', errore = True, error_message="Attenzione, email già in uso. Inserire una email non in uso")

            hashed_psw = bcrypt.generate_password_hash(psw).decode('utf-8')  # cripto la password

            # se le due password non corrispondono
            if(psw != conferma):
                return render_template('AdminTemplate/aggiungi_admin.html', errore=True, error_message = "Attenzione, le due password non combaciano.")
            else:
                # prendiamo la tabella utenti dal metadata tramite reflection
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
                return redirect(url_for('login', errore = False, messaggio = "None"))  # return
        else:
            return render_template('AdminTemplate/aggiungi_admin.html', errore=False)
    else:
        return errore_admin()
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
            return render_template('AdminTemplate/riepilogo_sale.html', sale=generate_sale_list())
    else:
        return errore_admin()
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
            return render_template('AdminTemplate/aggiungi_proiezione.html', film_dict=generate_film_dict(), sale=json.dumps(generate_sale_list()))
    else:
        return errore_admin()

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

            s = select([genere]).where(
                genere.c.tipo == tipo
            )
            conn = anonim_engine.connect()
            result = conn.execute(s)
            conn.close()

            if result.rowcount > 0:
                return render_template("AdminTemplate/aggiungi_genere.html", errore = True, error_message="Attenzione, genere già inserito.")

            ins = genere.insert()  # prendo la insert
            values = {  # dizionario per i valori
                'tipo': tipo
            }
            conn = admin_engine.connect()  # mi connetto
            conn.execute(ins, values)  # eseguo l'inserimento con i valori
            conn.close()
            return redirect(url_for('aggiungi_film'))  # return
        else:
            return render_template('AdminTemplate/aggiungi_genere.html', errore = False)
    else:
        return errore_admin()

@app.route('/rimuovi_film', methods=['GET', 'POST'])
@login_required
def rimuovi_film():
    if(current_user.is_admin == True):
        if request.method == 'POST':
            if "film" in request.form:
                # prendiamo i dati dal form
                id_film = request.form["film"]

                film = meta.tables["film"]  # prendo la tabella

                rem = film.delete().where(film.c.id_film == id_film)
                conn = admin_engine.connect()  # mi connetto
                conn.execute(rem)  # eseguo l'inserimento con i valori
                conn.close()
                return render_template('AdminTemplate/rimuovi_film.html', film_dict = generate_film_dict(), errore = False)
            else:
                return render_template('AdminTemplate/rimuovi_film.html', errore = True, error_message="Errore, stai provando a rimuovere una proiezione che non esiste", film_dict = generate_film_dict())
        else:
            return render_template('AdminTemplate/rimuovi_film.html', film_dict = generate_film_dict(), errore = False)
    else:
        return errore_admin()

@app.route('/rimuovi_proiezione', methods=['GET', 'POST'])
@login_required
def rimuovi_proiezione():
    if(current_user.is_admin == True):
        if request.method == 'POST':
            if "film" in request.form:
                # prendiamo i dati dal form
                id_film = request.form["film"]

                film = meta.tables["film"]  # prendo la tabella

                rem = film.delete().where(film.c.id_film == id_film)
                conn = admin_engine.connect()  # mi connetto
                conn.execute(rem)  # eseguo l'inserimento con i valori
                conn.close()
                return render_template('AdminTemplate/rimuovi_film.html', film_dict = generate_film_dict(), errore = False)
            else:
                return render_template('AdminTemplate/rimuovi_film.html', errore = True, error_message="Errore, stai provando a rimuovere un film che non esiste", film_dict = generate_film_dict())
        else:
            return render_template('AdminTemplate/rimuovi_film.html', film_dict = generate_film_dict(), errore = False)
    else:
        return errore_admin()



#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#

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

        utenti = meta.tables['utenti']
        s = select([utenti]).where(
            utenti.c.email == email
        )
        conn = anonim_engine.connect()
        result = conn.execute(s)
        if result.rowcount > 0: #se non è presente l'utente cercato
            conn.close()
            return render_template('registrazione.html', errore=True, error_message="Attenzione, email già in uso. Inserire un'altra email")

        hashed_psw = bcrypt.generate_password_hash(psw).decode('utf-8')  # cripto la password

        # se le due password non corrispondono
        if(psw != conferma):
            conn.close()
            return render_template('registrazione.html', errore=True, error_message="Attenzione, le due password non combaciano. Prego reinserire correttamente i dati")
        else:
            # prendiamo la tabella utenti dal metadata tramite reflection
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
            conn.execute(ins, values)  # eseguo l'inserimento con i valori
            conn.close()
            return redirect(url_for('login', errore = False, messaggio = "None"))  # return
    else:
        return render_template('registrazione.html', errore=False)

#--------------------------------------------------------------------------------------------#
#Visualizzaizone saldo e ricarica protafoglio
@app.route('/dashboard_account')
@login_required
def dashboard_account():

         utenti = meta.tables['utenti']
         s = select([utenti]).where(utenti.c.email == current_user.email)

         conn = clienti_engine.connect()
         result = conn.execute(s)
         row = result.fetchone()

         portafoglio = row["saldo"]
         name = row["nome"].capitalize()
         surname = row["cognome"].capitalize()
         email = row["email"]


         conn.close()
         return render_template('UserTemplate/dashboard_account.html', saldo = portafoglio, nome = name, cognome = surname, email = email)

#--------------------------------------------------------------------------------------------#
#modifica dei dati
@app.route('/cambia_password', methods=['GET', 'POST'])
@login_required
def cambia_password():
    if request.method == "POST":

        old_psw = request.form["old_psw"]
        psw = request.form["psw"]
        conferma = request.form["conferma_password"]

        utenti = meta.tables["utenti"]
        #s = select([utenti]).where(utenti.c.email == current_user.email)

        conn = clienti_engine.connect()
        #result = conn.execute(s)
        #vecchia = result.fetchone()

        #psw_new_raw = meta.tables["psw"]
        psw_ceck = bcrypt.check_password_hash(current_user.password, old_psw)

        if psw_ceck == False:
           return render_template('UserTemplate/cambia_password.html', errore=True, error_message="Errore: password vecchia errata!")  #Messaggio di errore da inviare all'utente
        elif psw != conferma:
           conn.close()
           return render_template('UserTemplate/cambia_password.html', errore=True, error_message="Attenzione, le due nuove password non combaciano. Prego reinserire correttamente i dati")
        elif old_psw == psw:
           conn.close()
           return render_template('UserTemplate/cambia_password.html', errore=True, error_message="Attenzione, le la vecchia e la nuova password combaciano. Prego reinserire password diverse")
        else:
           psw_new_hash = bcrypt.generate_password_hash(psw).decode('utf-8')
           ins = utenti.update().where(utenti.c.email == current_user.email)
           values = {
               'password' : psw_new_hash
           }

           conn.execute(ins, values)
           conn.close()
           return redirect(url_for('dashboard_account'))
    else:
           return render_template('UserTemplate/cambia_password.html', errore = False)

#--------------------------------------------------------------------------------------------#
@app.route('/ricarica_saldo', methods=['GET', 'POST'])
@login_required
def ricarica_saldo():
    utenti = meta.tables['utenti']
    s = select([utenti]).where(utenti.c.email == current_user.email)
    conn = clienti_engine.connect()
    result = conn.execute(s)
    saldo = result.fetchone()["saldo"]

    if request.method == "POST":
        taglio = request.form["taglio"]
        ins = utenti.update().where(utenti.c.email == current_user.email);
        values = {
            'saldo' : saldo + float(taglio)
        }

        conn.execute(ins,values)
        conn.close()
        return redirect(url_for('dashboard_account'))

    else:
        return render_template('UserTemplate/ricarica_saldo.html', saldo = saldo)

#--------------------------------------------------------------------------------------------#
@app.route('/prenota_biglietto', methods=['GET', 'POST'])
@login_required
def prenota_biglietto():
    return render_template('UserTemplate/prenota_biglietto.html')

#--------------------------------------------------------------------------------------------#
@app.route('/tutti_i_film')
@login_required
def tutti_i_film():
    dict_f = generate_film_dict()
    dict_p = generate_prox_proiection_dict()
    return render_template('UserTemplate/tutti_i_film.html', film_dict=dict_f, proiezioni_dict=dict_p)

#--------------------------------------------------------------------------------------------#
@app.route('/tutte_le_proiezioni')
@login_required
def tutte_le_proiezioni():
    dict = generate_film_dict()
    return render_template('UserTemplate/tutte_le_proiezioni.html', film_dict=dict)

#--------------------------------------------------------------------------------------------#
@app.route('/le_mie_prenotazioni')
@login_required
def le_mie_prenotazioni():
    dict = generate_film_dict()
    return render_template('UserTemplate/le_mie_prenotazioni.html', film_dict=dict)

#--------------------------------------------------------------------------------------------#
