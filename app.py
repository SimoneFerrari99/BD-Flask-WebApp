# Progetto basi di dati 2020 - Tema Cinema
# Gruppo: ArceCity
# Membri: Casarotti Giulio, Ferrari Simone, Trolese Gulio

# File: app.py
# Descrizione: File contenente tutte le route accessibili da un amministratore
#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
# Moduli importati
from flask import Flask, render_template, url_for, redirect, request, session, flash, abort, make_response
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.sql import func, and_, or_, not_
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import json
from PIL import Image

# from user_route import user_app
# from admin_route import admin_app


#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
# Configurazione APP

app = Flask(__name__)
# app.register_blueprint(user_app)
# app.register_blueprint(admin_app)
bcrypt = Bcrypt(app)  # inizializzo il bycript della app


# settiamo la secret_key per flask login... settata come consigliato nella documentazione di flask_login
# Configuriamo flask login
app.secret_key = b'f^iz\x05~\x1b\xaat\xf7\x00\xb4Lf7\xa0'
login_manager = LoginManager()
login_manager.init_app(app)

# apriamo l'engine creato in precedenza in fase di creazione del database (file create_database.py)
# engine = create_engine("postgres+psycopg2://postgres:ciao@serversrv.ddns.net:2345/progetto2020")
anonim_engine = create_engine("postgres+psycopg2://anonim:passwordanonim@localhost/progettobd")
clienti_engine = create_engine("postgres+psycopg2://cliente:passwordcliente@localhost/progettobd")
admin_engine = create_engine("postgres+psycopg2://admin:passwordadmin@localhost/progettobd")
# engine = create_engine("postgres+psycopg2://postgres:simone@localhost/progettobd")

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
# generatore di un dizionario per le persone
def generate_persone_dict():
    persone = meta.tables['persone']
    s = select([persone])
    conn = anonim_engine.connect()
    result = conn.execute(s)
    dict_persone = dict()
    for row in result:
        dict_persone[row['id_persona']] = str(row['nome'])+' '+str(row['cognome'])
    conn.close()
    return dict_persone

 # generatore di un dizionario per i film
def generate_film_dict():
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

# generatore di un dizionario per i generi
def generate_generi_dict():
    genere = meta.tables['genere']
    s = select([genere])
    conn = anonim_engine.connect()
    result = conn.execute(s)
    dict_generi = dict()
    for row in result:
        dict_generi[row['tipo']] = [row['tipo']]
    conn.close()
    return dict_generi

# generatore di un dizionario per le sale
def generate_sale_list():
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
    return redirect(url_for('login', errore=True, messaggio="Attenzione, solo gli amministratori sono autorizzati ad accedere a questa pagina."))

# Genera una lista contenente tutte le mie proiezioni
def generate_my_projection_dict():
    # SELECT f.titolo, pr.data, pr.ora_inizio, pr.sala, COUNT(*) as NumBiglietti
    # FROM posti po JOIN proiezioni pr ON po.id_proiezione = pr.id_proiezione JOIN film f ON pr.film = f.id_film
    # WHERE po.prenotato = current_user.email AND pr.data >= current_date AND pr.ora_inizio >= current_time
    # GROUP BY pr.id_proiezione

    posti = meta.tables['posti']
    proiezioni = meta.tables['proiezioni']
    film = meta.tables['film']

    j = posti.join(proiezioni.join(film, proiezioni.c.film == film.c.id_film),
                   posti.c.id_proiezione == proiezioni.c.id_proiezione)
    s = select([proiezioni.c.id_proiezione, film.c.id_film, film.c.titolo, film.c.durata, film.c.descrizione, proiezioni.c.data, proiezioni.c.ora_inizio, proiezioni.c.sala, func.count().label('num_biglietti')]).\
        select_from(j).\
        where(and_(
            posti.c.prenotato == current_user.email,
            or_(
                proiezioni.c.data > func.current_date(),
                and_(
                    proiezioni.c.data == func.current_date(),
                    proiezioni.c.ora_inizio >= func.current_time()
                    )
               )
        )).\
        group_by(proiezioni.c.id_proiezione, film.c.id_film, film.c.titolo, film.c.durata, film.c.descrizione, proiezioni.c.id_proiezione)

    conn = clienti_engine.connect()
    result = conn.execute(s)

    list_all_projection = []

    for row in result:  # lista di dizionari
        dict_projection = dict()
        dict_projection["id_film"] = row['id_film']
        dict_projection["id_proiezione"] = row['id_proiezione']
        dict_projection["titolo"] = row['titolo']
        dict_projection["durata"] = row['durata']
        dict_projection["descrizione"] = row['descrizione']
        dict_projection["data"] = row['data']
        dict_projection["ora_inizio"] = row['ora_inizio']
        dict_projection["sala"] = row['sala']
        dict_projection["num_biglietti"] = row['num_biglietti']
        list_all_projection.append(dict_projection)

    conn.close()
    return list_all_projection

# genera una lista contenente la propiezione più recente per ogni film
def generate_all_film_next_projection():
    #select film, "data" ,min(ora_inizio )
    #from proiezioni pr
    #where pr.data = (select min("data" )
    #                  from proiezioni
    #                  where ("data" > current_date or ("data" == current_date and pr.ora_inizio >= current_time)) and film = pr.film )
    #group by (film , "data" )

    proiezioni = meta.tables['proiezioni']
    pr = meta.tables['proiezioni']
    film = meta.tables['film']

    j = film.join(proiezioni, proiezioni.c.film == film.c.id_film)

    s1 = select([film.c.titolo, film.c.durata, pr.c.sala, pr.c.film, pr.c.data, func.min(pr.c.ora_inizio).label("prox_proiezione")]).\
        select_from(j).\
        where(pr.c.data == (select([func.min(proiezioni.c.data)]).\
                            where(
                                and_(
                                    or_(
                                        proiezioni.c.data > func.current_date(),
                                        and_(
                                            proiezioni.c.data == func.current_date(),
                                            proiezioni.c.ora_inizio >= func.current_time()
                                            )
                                        ),
                                     proiezioni.c.film == pr.c.film
                                    )
                                 )
                            )
        ).\
        group_by(film.c.titolo, pr.c.film, pr.c.data, film.c.durata, pr.c.sala)

    s = '''
        select f.titolo, f.descrizione, f.durata, pr.id_proiezione, pr.sala, pr.film, pr."data" , min(pr.ora_inizio ) as "prox_proiezione"
        from proiezioni pr join film f on pr.film = f.id_film
        where pr.data = (select min("data" )
                     from proiezioni
                     where ("data" > current_date or ("data" = current_date and ora_inizio >= current_time)) and film = pr.film )
        group by (f.titolo, f.descrizione, pr.film, pr.id_proiezione, pr."data", f.durata, pr.sala)
    '''

    conn = anonim_engine.connect()
    result = conn.execute(s)

    list_next_projection = []

    for row in result:  # lista di dizionari
        dict_next_projection = dict()
        dict_next_projection["id_proiezione"] = int(row["id_proiezione"])
        dict_next_projection["id_film"] = row['film']
        dict_next_projection["titolo"] = row['titolo']
        dict_next_projection["descrizione"] = row["descrizione"]
        dict_next_projection["ora_inizio"] = str(row['prox_proiezione'])
        dict_next_projection["durata"] = row['durata']
        dict_next_projection["data"] = str(row['data'])
        dict_next_projection["sala"] = row['sala']
        list_next_projection.append(dict_next_projection)

    conn.close()
    return list_next_projection


# genera tutte le proiezioni previste per un determinato film
def generate_all_projection_film(id):
    film = meta.tables['film']
    proiezioni = meta.tables['proiezioni']
    j = film.join(proiezioni, film.c.id_film == proiezioni.c.film)  # JOIN
    s = select([film, proiezioni]).\
        select_from(j).\
        where(and_(or_(
                proiezioni.c.data > func.current_date(),
                and_(
                    proiezioni.c.data == func.current_date(),
                    proiezioni.c.ora_inizio >= func.current_time()
                    )
                ), film.c.id_film == id)
            )
    conn = clienti_engine.connect()
    result = conn.execute(s)

    list_all_projection = []
    for row in result:
        dict_projection = dict()
        dict_projection["id_proiezione"] = row["id_proiezione"]
        dict_projection["descrizione"] = row["descrizione"]
        dict_projection["durata"] = row["durata"]
        dict_projection["id_film"] = row["id_film"]
        dict_projection["titolo"] = row["titolo"]
        dict_projection["data"] = row["data"]
        dict_projection["ora_inizio"] = row["ora_inizio"]
        dict_projection["sala"] = row["sala"]
        list_all_projection.append(dict_projection)
    conn.close()
    return list_all_projection

# genera tutte le proiezioni future per tutti i film
def generate_all_projection():
    film = meta.tables['film']
    proiezioni = meta.tables['proiezioni']
    j = film.join(proiezioni, film.c.id_film == proiezioni.c.film)  # JOIN
    s = select([film, proiezioni]).\
        select_from(j).\
        where(or_(
                proiezioni.c.data > func.current_date(),
                and_(
                    proiezioni.c.data == func.current_date(),
                    proiezioni.c.ora_inizio >= func.current_time()
                    )
                )
            )
    conn = clienti_engine.connect()
    result = conn.execute(s)

    list_all_projection = []
    for row in result:
        dict_projection = dict()
        dict_projection["id_proiezione"] = row["id_proiezione"]
        dict_projection["titolo"] = row["titolo"]
        dict_projection["id_film"] = row["id_film"]
        dict_projection["data"] = str(row["data"])
        dict_projection["ora_inizio"] = str(row["ora_inizio"])
        dict_projection["sala"] = row["sala"]
        list_all_projection.append(dict_projection)
    conn.close()
    return list_all_projection


#---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---@---#
# Route principale: Home
@ app.route('/')
def home():
    if(current_user.is_anonymous == False and current_user.is_admin == True):
        admin = True
    else:
        admin = False
    proj_list = generate_all_film_next_projection()
    ordered_list = sorted(proj_list, key = lambda i: (i['data'], i['ora_inizio']))
    ordered_list = ordered_list[:5]
    return render_template('home.html', proj_list=ordered_list, is_admin=admin)

#--------------------------------------------------------------------------------------------#
# Login
# classe che rappresenta un nostro utente
class Utente(UserMixin):
    def __init__(self, email, password, is_admin):  # costruttore
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def get_id(self):  # metodo che restituisce l'id (in questo caso, la email)
        return self.email


@ login_manager.user_loader
def load_user(user_email):  # funzione che restituisce l'utente associato alla user_email
    utenti = meta.tables['utenti']
    s = select([utenti]).where(utenti.c.email == user_email)
    conn = anonim_engine.connect()
    result = conn.execute(s)
    if result.rowcount == 0:  # se non è presente l'utente cercato
        return None
    user = result.fetchone()
    conn.close()
    # ritorna un Utente
    return Utente(user.email, user.password, user.is_admin)


# Quando il login è richiesto, e non sei loggato, vieni rimandato al login
@ login_manager.unauthorized_handler
def unauthorized():
    # TODO: dare un messaggio di errore
    return redirect(url_for('login', errore=True, messaggio="Attenzione, non sei autorizzato ad accedere a questa pagina. Accedi con le giuste credenziali"))


@ app.route('/login/<errore>/<messaggio>', methods=['GET', 'POST'])
def login(errore, messaggio):
    if request.method == 'POST':  # gestione del form
        # prendiamo i dati dal form
        email_form = request.form["email"]
        password = request.form["psw"]
        # carichiamo l'utente
        utente = load_user(email_form)
        # se la password salvata nel database e quella inserita nel form coincidono
        if utente != None and bcrypt.check_password_hash(utente.password, password) == True:
            login_user(utente)  # loggo l'utente
            resp = make_response(redirect(url_for('home')))
            resp.set_cookie("userEmail", current_user.email)
            return resp
        else:
            return redirect(url_for('login', errore=True, messaggio="Attenzione, mail o password errate."))
    else:
        return render_template('login.html', error=errore, error_message=messaggio)
#--------------------------------------------------------------------------------------------#
# Logout
@ app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie("userEmail", "", max_age=0)
    logout_user()
    return resp


#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#

#--------------------------------------------------------------------------------------------#
# HOME PER LA GESTIONE DATABASE
@ app.route('/home_gestione_sito')
@ login_required
def home_gestione_sito():
    if(current_user.is_admin == True):
        return render_template('AdminTemplate/home_gestione_sito.html')
    else:
        return errore_admin()


#--------------------------------------------------------------------------------------------#
# Inseriemnto di una persona
@ app.route('/aggiungi_persona', methods=['GET', 'POST'])
@ login_required
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
            # abbiamo due diversi bottoni di sumbit
            if request.form["Submit"] == "Film":
                return redirect(url_for('aggiungi_film'))  # return
            else:
                return redirect(url_for('aggiungi_persona'))
        else:
            return render_template('AdminTemplate/aggiungi_persona.html')
    else:
        return errore_admin()
#--------------------------------------------------------------------------------------------#
# Inserimento di un film
@ app.route('/aggiungi_film', methods=['GET', 'POST'])
@ login_required
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
                        return render_template('aggiungi_film.html',  errore=True, error_message="Attenzione, hai scelto lo stesso attore più di una volta.", persone_dict=json.dumps(dict_p), generi_dict=json.dumps(dict_g))
                    list_attori.append(id_attore)
                # se è un regista
                elif "registi" in str(elem):
                    id_regista = request.form[str(elem)]
                    if id_regista in list_registi:
                        return render_template('AdminTemplate/aggiungi_film.html',  errore=True, error_message="Attenzione, hai scelto lo stesso regista più di una volta.", persone_dict=json.dumps(dict_p), generi_dict=json.dumps(dict_g))
                    list_registi.append(id_regista)
                # se è un genere
                elif "generi" in str(elem):
                    tipo_genere = request.form[str(elem)]
                    if tipo_genere in list_generi:
                        return render_template('AdminTemplate/aggiungi_film.html', errore=True, error_message="Attenzione, hai scelto lo stesso genere più di una volta.", persone_dict=json.dumps(dict_p), generi_dict=json.dumps(dict_g))
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
            return render_template('AdminTemplate/aggiungi_film.html', errore=False, error_message="", persone_dict=json.dumps(dict_p), generi_dict=json.dumps(dict_g))
    else:
        return errore_admin()
#--------------------------------------------------------------------------------------------#
# Inseriemnto di un amministratore (da parte di un amministratore)
@ app.route('/aggiungi_admin', methods=['GET', 'POST'])
@ login_required
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
                return render_template('AdminTemplate/aggiungi_admin.html', errore=True, error_message="Attenzione, email già in uso. Inserire una email non in uso")

            hashed_psw = bcrypt.generate_password_hash(psw).decode('utf-8')  # cripto la password

            # se le due password non corrispondono
            if(psw != conferma):
                return render_template('AdminTemplate/aggiungi_admin.html', errore=True, error_message="Attenzione, le due password non combaciano.")
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
                # return
                return redirect(url_for('login', errore=False, messaggio="None"))
        else:
            return render_template('AdminTemplate/aggiungi_admin.html', errore=False)
    else:
        return errore_admin()
#--------------------------------------------------------------------------------------------#
# Inseriemnto di una sala
@ app.route('/riepilogo_sale', methods=['GET', 'POST'])
@ login_required
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
@ app.route('/aggiungi_proiezione', methods=['GET', 'POST'])
@ login_required
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
@ app.route('/aggiungi_genere', methods=['GET', 'POST'])
@ login_required
def aggiungi_genere():
    if(current_user.is_admin == True):
        if request.method == 'POST':
            # prendiamo i dati dal form
            tipo = request.form["tipo"]

            genere = meta.tables['genere']  # prendo la tabella

            s = select([genere]).where(genere.c.tipo == tipo)
            conn = anonim_engine.connect()
            result = conn.execute(s)
            conn.close()

            if result.rowcount > 0:
                return render_template("AdminTemplate/aggiungi_genere.html", errore=True, error_message="Attenzione, genere già inserito.")

            ins = genere.insert()  # prendo la insert
            values = {  # dizionario per i valori
                'tipo': tipo
            }
            conn = admin_engine.connect()  # mi connetto
            conn.execute(ins, values)  # eseguo l'inserimento con i valori
            conn.close()
            return redirect(url_for('aggiungi_film'))  # return
        else:
            return render_template('AdminTemplate/aggiungi_genere.html', errore=False)
    else:
        return errore_admin()

#--------------------------------------------------------------------------------------------#
# Rimozione di un film
@ app.route('/rimuovi_film', methods=['GET', 'POST'])
@ login_required
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
                return render_template('AdminTemplate/rimuovi_film.html', film_dict=generate_film_dict(), errore=False)
            else:
                return render_template('AdminTemplate/rimuovi_film.html', errore=True, error_message="Errore, stai provando a rimuovere una proiezione che non esiste", film_dict=generate_film_dict())
        else:
            return render_template('AdminTemplate/rimuovi_film.html', film_dict=generate_film_dict(), errore=False)
    else:
        return errore_admin()

#--------------------------------------------------------------------------------------------#
# Rimozione di una proiezione
@ app.route('/rimuovi_proiezione', methods=['GET', 'POST'])
@ login_required
def rimuovi_proiezione():
    if(current_user.is_admin == True):
        if request.method == 'POST':
            if "film" and "proiezione" in request.form:
                # prendiamo i dati dal form
                id_pr = request.form["proiezione"]

                proiezioni = meta.tables["proiezioni"]  # prendo la tabella

                rem = proiezioni.delete().where(proiezioni.c.id_proiezione == id_pr)
                conn = admin_engine.connect()  # mi connetto
                conn.execute(rem)  # eseguo l'inserimento con i valori
                conn.close()
                return render_template('AdminTemplate/rimuovi_proiezioni.html', film_dict=generate_film_dict(), proiezioni=json.dumps(generate_all_projection()), errore=False)
            else:
                return render_template('AdminTemplate/rimuovi_proiezioni.html', errore=True, error_message="Errore, stai provando a rimuovere una proiezione che non esiste", film_dict=generate_film_dict(), proiezioni=json.dumps(generate_all_projection()))
        else:

            return render_template('AdminTemplate/rimuovi_proiezioni.html', film_dict=generate_film_dict(), proiezioni=json.dumps(generate_all_projection()), errore=False)
    else:
        return errore_admin()


#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#

#--------------------------------------------------------------------------------------------#
# Registrazione di un nuovo utente
@ app.route('/registrazione', methods=['GET', 'POST'])
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
        if result.rowcount > 0:  # se non è presente l'utente cercato
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
            # return
            return redirect(url_for('login', errore=False, messaggio="None"))
    else:
        return render_template('registrazione.html', errore=False)

#--------------------------------------------------------------------------------------------#
# Visualizzaizone saldo e ricarica protafoglio
@ app.route('/dashboard_account')
@ login_required
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
    return render_template('UserTemplate/dashboard_account.html', saldo=portafoglio, nome=name, cognome=surname, email=email)

#--------------------------------------------------------------------------------------------#
# modifica dei dati
@ app.route('/cambia_password', methods=['GET', 'POST'])
@ login_required
def cambia_password():
    if request.method == "POST":

        old_psw = request.form["old_psw"]
        psw = request.form["psw"]
        conferma = request.form["conferma_password"]

        utenti = meta.tables["utenti"]
        conn = clienti_engine.connect()

        psw_ceck = bcrypt.check_password_hash(current_user.password, old_psw)

        if psw_ceck == False:
            # Messaggio di errore da inviare all'utente
            return render_template('UserTemplate/cambia_password.html', errore=True, error_message="Errore: password vecchia errata!")
        elif psw != conferma:
            conn.close()
            return render_template('UserTemplate/cambia_password.html', errore=True, error_message="Attenzione, le due nuove password non combaciano. Prego reinserire correttamente i dati")
        elif old_psw == psw:
            conn.close()
            return render_template('UserTemplate/cambia_password.html', errore=True, error_message="Attenzione, la vecchia e la nuova password combaciano. Prego reinserire password diverse")
        else:
            psw_new_hash = bcrypt.generate_password_hash(psw).decode('utf-8')
            ins = utenti.update().where(utenti.c.email == current_user.email)
            values = {
                'password': psw_new_hash
            }

            conn.execute(ins, values)
            conn.close()
            return redirect(url_for('dashboard_account'))
    else:
        return render_template('UserTemplate/cambia_password.html', errore=False)

#--------------------------------------------------------------------------------------------#
@ app.route('/ricarica_saldo', methods=['GET', 'POST'])
@ login_required
def ricarica_saldo():
    utenti = meta.tables['utenti']
    s = select([utenti]).where(utenti.c.email == current_user.email)
    conn = clienti_engine.connect()
    result = conn.execute(s)
    saldo = result.fetchone()["saldo"]

    if request.method == "POST":
        taglio = request.form["taglio"]
        ins = utenti.update().where(utenti.c.email == current_user.email)
        values = {
            'saldo': saldo + float(taglio)
        }

        conn.execute(ins, values)
        conn.close()
        return redirect(url_for('dashboard_account'))

    else:
        return render_template('UserTemplate/ricarica_saldo.html', saldo=saldo)

#--------------------------------------------------------------------------------------------#


@ app.route('/prenota_biglietto/<id_pr>', methods=['GET', 'POST'])
@ login_required
def prenota_biglietto(id_pr):
    if request.method == "POST":
        scelti = request.json["posti"]
        totale = float(request.json["totale"])
        posti = meta.tables["posti"]
        utenti = meta.tables["utenti"]
        ins = posti.insert()

        with clienti_engine.connect().execution_options(isolation_level="REPEATABLE READ") as conn:
            trans = conn.begin()
            try:
                sel = select([utenti.c.saldo]).\
                      where(utenti.c.email == current_user.email)
                result = conn.execute(sel)
                row = result.fetchone()
                if row["saldo"] >= totale:
                    for posto in scelti:
                        values = {
                            "id_posto": posto,
                            "prezzo": 5.0,
                            "prenotato": current_user.email,
                            "id_proiezione": id_pr
                        }
                        conn.execute(ins, values)
                    up = utenti.update().where(utenti.c.email == current_user.email)
                    values = {
                        "saldo": row["saldo"] - totale
                    }
                    conn.execute(up, values)
                    trans.commit()
                else:
                    trans.rollback()
                    return "Conflict", 409
            except:
                trans.rollback()
                return "Conflict", 409
            finally:
                conn.close()
        return 'OK', 200
    else:
        film = meta.tables['film']
        proiezioni = meta.tables['proiezioni']
        j = film.join(proiezioni, film.c.id_film == proiezioni.c.film)  # JOIN
        s = select([film, proiezioni]).\
            select_from(j).\
            where(proiezioni.c.id_proiezione == id_pr)
        conn = clienti_engine.connect()
        proiezione = conn.execute(s)
        row = proiezione.fetchone()
        posti = meta.tables["posti"]
        s = select([posti.c.id_posto]).\
            where(posti.c.id_proiezione == id_pr)
        result = conn.execute(s)
        occupati = []
        for elem in result:
            occupati.append(elem[0])
        return render_template('UserTemplate/prenota_biglietto.html', rossi = occupati, titolo=row["titolo"], data=row["data"], ora=row["ora_inizio"], sala=row["sala"], id=id_pr)
#--------------------------------------------------------------------------------------------#
# visualizziamo tutti i film con la prossima proiezione in programma
@ app.route('/tutti_i_film')
def tutti_i_film():
    proj_list = generate_all_film_next_projection()
    ordered_list = sorted(proj_list, key = lambda i: (i['titolo']))
    return render_template('UserTemplate/tutti_i_film.html', proj_list=ordered_list)

#--------------------------------------------------------------------------------------------#
# visualizziamo tutte le proiezioni in programma per un determinato film
@app.route('/altre_date_film/<id_film>', methods=['GET', 'POST'])
def altre_date_film(id_film):
    dict = generate_all_projection_film(id_film)
    string = "{{url_for('static', filename='copertine/" + id_film + ".jpg')}}"
    return render_template('UserTemplate/altre_date_film.html', copertina = string, dict_film = dict )

#--------------------------------------------------------------------------------------------#
# visualizziamo tutte le mie prenotazioni
@ app.route('/le_mie_prenotazioni')
@ login_required
def le_mie_prenotazioni():
    dict = generate_my_projection_dict()
    ordered_list = sorted(dict, key = lambda i: (i['data'], i['ora_inizio']))
    return render_template('UserTemplate/le_mie_prenotazioni.html', projection_dict=ordered_list)

#--------------------------------------------------------------------------------------------#
